from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader

import cv2
from pyzbar import pyzbar

Builder.load_file('main.kivy')

class ScrollableWindow(ScrollView):
    image = ObjectProperty(None)
    label = ObjectProperty("")

    def __init__(self, **kwargs):
        super(ScrollableWindow, self).__init__(**kwargs)
        # Запускаем обновление кадра каждые 1/30 секунды
        Clock.schedule_interval(self.update_frame, 1.0/30.0)
        # Список для хранения данных штрих-кодов
        self.barcode_labels = []

    def update_frame(self, dt):
        # Считываем текущий кадр с камеры
        ret, frame = cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 0)

        # Преобразуем кадр в черно-белое изображение
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Распознаем штрих-коды в кадре
        barcodes = pyzbar.decode(gray)

        # Если найден хотя бы один штрих-код, выводим его значение на экран
        if len(barcodes) > 0:
            barcode_value = barcodes[0].data.decode('utf-8')

            add = True

            # Добавляем данные в список и создаем новый Label для отображения данных
            for i in self.barcode_labels:
                if i[0] == barcode_value:
                    add = False

            if add:
                value = [barcode_value,1,10,10,(len(self.barcode_labels)+1)]
                print(value)
                self.barcode_labels.append(value)
                code = f"""
GridLayout:
    cols: 2
    size_hint_x: 1
    size_hint_y: None
    height: 90

    BoxLayout:
        height: self.minimum_height
        orientation: "vertical"
        size_hint_x: 0.8

        Label:
            text: "{value[0]}"
        GridLayout:
            cols: 3

            TextInput:
                text: "{value[1]}"
            Label:
                text: "{value[2]}"
            Label:
                text: "{value[3]}"
    Button:
        text: "{value[4]}"
        size_hint_y: 1
        size_hint_x: 0.2
                """
                
                new_label = Builder.load_string(code)
                App.get_running_app().root.ids.labels_box.add_widget(new_label)
                SoundLoader.load('sound.mp3').play()


        # Преобразуем кадр в формат RGB
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Создаем объект Texture на основе данных изображения
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(frame_rgb.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

        # Отображаем текстуру в виджете Image
        self.image.texture = texture

    def clear_labels(self):
        self.ids.labels_box.children
        print(len(self.ids.labels_box.children))

class MyApp(App):
    def build(self):
        return ScrollableWindow()


if __name__ == '__main__':
    cap = cv2.VideoCapture('http://192.168.43.1:8080/video')
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    MyApp().run()

    cap.release()
