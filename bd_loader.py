import sqlite3

def bd_load(barcode, cash):
	bd = sqlite3.connect('bd.bd')

bd_load('6970435714923', 20000)