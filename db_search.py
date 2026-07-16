import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
import json
import os
import re

SETTINGS_FILE = "db_settings.json"

class DBSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DB Şema Arama Motoru")
        self.root.geometry("700x550")
        self.db_schema = {}
        
        # Başlangıçta ayarları yükle
        self.settings = self.ayarlari_yukle()
        
        if self.settings:
            self.verileri_hazirla()
        else:
            self.ayar_ekrani_ac()

    def ayarlari_yukle(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    return json.load(f)
            except:
                return None
        return None

    def ayarlari_kaydet(self, server, db, user, pwd):
        data = {"server": server, "database": db, "user": user, "password": pwd}
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Başarili", "Ayarlar kaydedildi! Veriler çekiliyor...")
        self.settings = data
        self.verileri_hazirla()

    def verileri_hazirla(self):
        """Veritabanina bağlanip verileri çeker ve arayüzü kurar."""
        try:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.settings['server']};"
                f"DATABASE={self.settings['database']};"
                f"UID={self.settings['user']};"
                f"PWD={self.settings['password']};"
            )
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            
            query = "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS ORDER BY TABLE_NAME"
            cursor.execute(query)
            
            self.db_schema = {}
            for row in cursor.fetchall():
                tablo, kolon = row
                if tablo not in self.db_schema:
                    self.db_schema[tablo] = []
                self.db_schema[tablo].append(kolon)
                
            conn.close()
            # Veriler geldiyse ana arama arayüzünü oluştur
            self.arayuz_olustur()
            
        except Exception as e:
            res = messagebox.askretrycancel("Bağlanti Hatasi", f"Veritabanina bağlanilamadi. Bilgileri güncellemek ister misiniz?\n\nHata: {e}")
            if res:
                self.ayar_ekrani_ac()

    def ayar_ekrani_ac(self):
        self.ayar_penceresi = tk.Toplevel(self.root)
        self.ayar_penceresi.title("Bağlanti Ayarlari")
        self.ayar_penceresi.geometry("350x400")
        try:
            self.ayar_penceresi.iconbitmap("db_ikon.ico.ico")
        except:
            pass
        self.ayar_penceresi.grab_set() # Diğer pencereye tıklanmasını engeller

        tk.Label(self.ayar_penceresi, text="SQL Server Bağlanti Bilgileri", font=("Arial", 10, "bold")).pack(pady=10)

        fields = [("Server:", "server"), ("Database:", "database"), ("User:", "user"), ("Password:", "password")]
        self.entries = {}

        for label_text, key in fields:
            tk.Label(self.ayar_penceresi, text=label_text).pack()
            ent = tk.Entry(self.ayar_penceresi, show="*" if key == "password" else "")
            ent.pack(pady=5)
            # Eğer eski ayar varsa içini doldur
            if self.settings and key in self.settings:
                ent.insert(0, self.settings[key])
            self.entries[key] = ent

        tk.Button(self.ayar_penceresi, text="Kaydet ve Bağlan", bg="#4CAF50", fg="white",
                  command=lambda: [self.ayar_penceresi.withdraw(), 
                                   self.ayarlari_kaydet(self.entries['server'].get(), 
                                                       self.entries['database'].get(), 
                                                       self.entries['user'].get(), 
                                                       self.entries['password'].get())]).pack(pady=20)

    def arayuz_olustur(self):
        """Ana arama ekranini temizleyip yeniden kurar."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Üst Panel
        frame_ust = tk.Frame(self.root, padx=20, pady=20)
        frame_ust.pack(fill="x")

        tk.Label(frame_ust, text=f"Bağli DB: {self.settings['database']}", fg="green").pack(anchor="e")
        tk.Label(frame_ust, text="Arama Yap (* kullanabilirsiniz):", font=("Segoe UI", 10)).pack(anchor="w")

        self.entry_arama = tk.Entry(frame_ust, font=("Segoe UI", 12))
        self.entry_arama.pack(fill="x", pady=5)
        self.entry_arama.bind("<Return>", lambda e: self.arama_yap())

        btn_ara = tk.Button(frame_ust, text="Sistemde Ara", bg="#0078D4", fg="white", 
                           font=("Segoe UI", 10, "bold"), command=self.arama_yap, cursor="hand2")
        btn_ara.pack(fill="x", pady=5)

        # Alt Panel (Sonuçlar)
        frame_alt = tk.Frame(self.root)
        frame_alt.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        scrollbar = tk.Scrollbar(frame_alt)
        scrollbar.pack(side="right", fill="y")

        self.listbox_sonuclar = tk.Listbox(frame_alt, font=("Consolas", 10), yscrollcommand=scrollbar.set)
        self.listbox_sonuclar.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox_sonuclar.yview)

        # Ayarları Değiştir Butonu (Küçük, en altta)
        tk.Button(self.root, text="Bağlanti Ayarlarini Güncelle", command=self.ayar_ekrani_ac, font=("Arial", 8)).pack(pady=5)

    def arama_yap(self):
        kelime = self.entry_arama.get().strip()
        if not kelime: return
            
        self.listbox_sonuclar.delete(0, tk.END)
        search_pattern = kelime.replace("*", ".*")
        
        try:
            regex = re.compile(f"^{search_pattern}$", re.IGNORECASE)
        except:
            messagebox.showerror("Hata", "Geçersiz arama karakteri!")
            return

        for tablo, kolonlar in self.db_schema.items():
            if regex.search(tablo):
                self.listbox_sonuclar.insert(tk.END, f"📁 [TABLO] {tablo}")
                for k in kolonlar:
                    self.listbox_sonuclar.insert(tk.END, f"   🔹 {k}")
                self.listbox_sonuclar.insert(tk.END, "-"*40)
            else:
                for kolon in kolonlar:
                    if regex.search(kolon):
                        self.listbox_sonuclar.insert(tk.END, f"   📌 [KOLON] {kolon}  (Tablo: {tablo})")

if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap("db_ikon.ico") 
    except:
        pass
    app = DBSearchApp(root)
    root.mainloop()