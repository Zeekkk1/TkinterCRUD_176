import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "nilai_siswa.db"
selected_id = None



def run_query(sql, params=()):
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:
            return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def init_db():
    run_query("""CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT NOT NULL,
        biologi REAL NOT NULL,
        fisika REAL NOT NULL,
        inggris REAL NOT NULL,
        prediksi_fakultas TEXT NOT NULL)""")


def hitung_prediksi(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Mending gausah sekolah"


def add_siswa(nama, bio, fis, ing):
    pred = hitung_prediksi(bio, fis, ing)
    run_query("""INSERT INTO nilai_siswa
                 (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
                 VALUES (?, ?, ?, ?, ?)""", (nama, bio, fis, ing, pred))
    return pred


def get_siswa():
    return run_query("""SELECT id, nama_siswa, biologi, fisika, inggris,
                        prediksi_fakultas FROM nilai_siswa ORDER BY id DESC""")


def update_siswa(sid, nama, bio, fis, ing):
    pred = hitung_prediksi(bio, fis, ing)
    run_query("""UPDATE nilai_siswa SET nama_siswa = ?, biologi = ?, fisika = ?,
                 inggris = ?, prediksi_fakultas = ? WHERE id = ?""",
              (nama, bio, fis, ing, pred, sid))
    return pred


def delete_siswa(sid):
    run_query("DELETE FROM nilai_siswa WHERE id = ?", (sid,))



init_db()
root = tk.Tk()
root.title("Prediksi Fakultas")

fields = ["Nama", "Biologi", "Fisika", "Inggris"]
entries = {}
for i, field in enumerate(fields):
    tk.Label(root, text=field).grid(row=i, column=0, sticky="w", padx=6)
    entries[field] = tk.Entry(root, width=30)
    entries[field].grid(row=i, column=1, pady=4, padx=6)

cols = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=cols, show="headings", height=8)
for c in cols:
    tree.heading(c, text=c.replace("_", " ").title())
    tree.column(c, width=90 if c != "prediksi_fakultas" else 120)
tree.column("id", width=40)
tree.grid(row=4, column=0, columnspan=2, padx=6, pady=6)


def ke_angka(teks):
    try:
        n = float(teks)
        return n if 0 <= n <= 100 else 0.0
    except ValueError:
        return 0.0


def read_form():
    nama = entries["Nama"].get().strip()
    if not nama:
        messagebox.showwarning("Data kurang", "Nama siswa harus diisi.")
        return None
    bio = ke_angka(entries["Biologi"].get())
    fis = ke_angka(entries["Fisika"].get())
    ing = ke_angka(entries["Inggris"].get())
    return nama, bio, fis, ing


def refresh():
    tree.delete(*tree.get_children())
    for row in get_siswa():
        tree.insert("", tk.END, values=row)


def clear_form():
    global selected_id
    selected_id = None
    for e in entries.values():
        e.delete(0, tk.END)


def on_add():
    data = read_form()
    if data:
        pred = add_siswa(*data)
        messagebox.showinfo("Hasil Prediksi", f"{data[0]} diprediksi masuk: {pred}")
        clear_form()
        refresh()


def on_select(event):
    global selected_id
    sel = tree.selection()
    if not sel:
        return
    sid, nama, bio, fis, ing, _ = tree.item(sel[0], "values")
    clear_form()
    selected_id = int(sid)
    entries["Nama"].insert(0, nama)
    entries["Biologi"].insert(0, bio)
    entries["Fisika"].insert(0, fis)
    entries["Inggris"].insert(0, ing)


tree.bind("<<TreeviewSelect>>", on_select)


def on_update():
    if selected_id is None:
        messagebox.showinfo("Update", "Pilih data siswa dulu.")
        return
    data = read_form()
    if data:
        update_siswa(selected_id, *data)
        clear_form()
        refresh()


def on_delete():
    if selected_id is None:
        messagebox.showinfo("Hapus", "Pilih data siswa dulu.")
        return
    if messagebox.askyesno("Konfirmasi", "Hapus data siswa ini?"):
        delete_siswa(selected_id)
        clear_form()
        refresh()


btns = tk.Frame(root)
btns.grid(row=5, column=0, columnspan=2, pady=6)
for text, cmd in [("Submit", on_add), ("Update", on_update),
                  ("Delete", on_delete), ("Clear", clear_form)]:
    tk.Button(btns, text=text, width=8, command=cmd).pack(side="left", padx=4)

refresh()
root.mainloop()