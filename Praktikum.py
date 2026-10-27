import tkinter as tk
import sqlite3
import tkinter.messagebox as msg

def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_db()

def predict(inggris, biologi, fisika):
    if inggris > biologi and inggris > fisika:
        return "Bahasa"
    elif biologi > inggris and biologi > fisika:
        return "Kedokteran"
    elif fisika > inggris and fisika > biologi:
        return "Teknik"
    else :
        return "mending ga usah sekolah"

