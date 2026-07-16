import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc
import json
import os
import re

# EN: File to store database connection settings
# TR: Veritabanı bağlantı ayarlarının saklanacağı dosya
SETTINGS_FILE = "db_settings.json"

class DBSearchApp:
    def __init__(self, root):
        # EN: Initialize the main application window
        # TR: Ana uygulama penceresini başlat
        self.root = root
        self.root.title("DB Şema Arama Motoru")
        self.root.geometry("700x550")
        self.db_schema = {}
        
        # EN: Load settings on startup
        # TR: Başlangıçta ayarları yükle
        self.settings = self.load_settings()
        
        # EN: If settings exist, fetch data; otherwise, open settings screen
        # TR: Ayarlar varsa verileri hazırla, yoksa ayar ekranını aç
        if self.settings:
            self.fetch_data()
        else:
            self.open_settings_window()

    def load_settings(self):
        # EN: Check if the settings file exists and load its content
        # TR: Ayar dosyasının var olup olmadığını kontrol et ve içeriğini yükle
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    return json.load(f)
            except:
                return None
        return None

    def save_settings(self, server, db, user, pwd):
        # EN: Save connection settings to a JSON file
        # TR: Bağlantı ayarlarını bir JSON dosyasına kaydet
        data = {"server": server, "database": db, "user": user, "password": pwd}
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Başarili", "Ayarlar kaydedildi! Veriler çekiliyor...")
        self.settings = data
        self.fetch_data()

    def fetch_data(self):
        """
        EN: Connects to the database, fetches schema data, and builds the UI.
        TR: Veritabanina bağlanip verileri çeker ve arayüzü kurar.
        """
        try:
            # EN: Prepare the ODBC connection string for SQL Server
            # TR: SQL Server için ODBC bağlantı dizesini hazırla
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.settings['server']};"
                f"DATABASE={self.settings['database']};"
                f"UID={self.settings['user']};"
                f"PWD={self.settings['password']};"
            )
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            
            # EN: SQL query to get all table and column names
            # TR: Tüm tablo ve kolon adlarını çekmek için SQL sorgusu
            query = "SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS ORDER BY TABLE_NAME"
            cursor.execute(query)
            
            # EN: Parse results into a dictionary grouped by table name
            # TR: Sonuçları tablo adına göre gruplanmış bir sözlüğe dönüştür
            self.db_schema = {}
            for row in cursor.fetchall():
                table, column = row
                if table not in self.db_schema:
                    self.db_schema[table] = []
                self.db_schema[table].append(column)
                
            conn.close()
            
            # EN: Build the main search interface if data is successfully fetched
            # TR: Veriler başarıyla geldiyse ana arama arayüzünü oluştur
            self.build_ui()
            
        except Exception as e:
            # EN: Show error and ask if the user wants to update settings
            # TR: Hata göster ve kullanıcının ayarları güncellemek isteyip istemediğini sor
            res = messagebox.askretrycancel("Bağlanti Hatasi", f"Veritabanina bağlanilamadi. Bilgileri güncellemek ister misiniz?\n\nHata: {e}")
            if res:
                self.open_settings_window()

    def open_settings_window(self):
        # EN: Open a top-level window for database connection settings
        # TR: Veritabanı bağlantı ayarları için yeni bir üst düzey pencere aç
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Bağlanti Ayarlari")
        self.settings_window.geometry("350x400")
        try:
            self.settings_window.iconbitmap("db_ikon.ico")
        except:
            pass
            
        # EN: Prevent interacting with the main window while settings are open
        # TR: Ayarlar açıkken ana pencereye tıklanmasını engeller
        self.settings_window.grab_set() 

        tk.Label(self.settings_window, text="SQL Server Bağlanti Bilgileri", font=("Arial", 10, "bold")).pack(pady=10)

        # EN: Define input fields for the settings window
        # TR: Ayar penceresi için giriş alanlarını tanımla
        fields = [("Server:", "server"), ("Database:", "database"), ("User:", "user"), ("Password:", "password")]
        self.entries = {}

        for label_text, key in fields:
            tk.Label(self.settings_window, text=label_text).pack()
            # EN: Mask password field with asterisks
            # TR: Şifre alanını yıldız karakteriyle gizle
            ent = tk.Entry(self.settings_window, show="*" if key == "password" else "")
            ent.pack(pady=5)
            
            # EN: Fill in the fields if old settings exist
            # TR: Eğer eski ayar varsa giriş alanlarını doldur
            if self.settings and key in self.settings:
                ent.insert(0, self.settings[key])
            self.entries[key] = ent

        # EN: Save button logic to update settings
        # TR: Ayarları güncellemek için kaydet butonu mantığı
        tk.Button(self.settings_window, text="Kaydet ve Bağlan", bg="#4CAF50", fg="white",
                  command=lambda: [self.settings_window.withdraw(), 
                                   self.save_settings(self.entries['server'].get(), 
                                                      self.entries['database'].get(), 
                                                      self.entries['user'].get(), 
                                                      self.entries['password'].get())]).pack(pady=20)

    def build_ui(self):
        """
        EN: Clears the main search screen and rebuilds it.
        TR: Ana arama ekranini temizleyip yeniden kurar.
        """
        # EN: Destroy all existing widgets in the root window
        # TR: Kök penceredeki mevcut tüm widget'ları yok et
        for widget in self.root.winfo_children():
            widget.destroy()

        # EN: Top Panel for Search Input
        # TR: Arama Girişi için Üst Panel
        top_frame = tk.Frame(self.root, padx=20, pady=20)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text=f"Bağli DB: {self.settings['database']}", fg="green").pack(anchor="e")
        tk.Label(top_frame, text="Arama Yap (* kullanabilirsiniz):", font=("Segoe UI", 10)).pack(anchor="w")

        self.search_entry = tk.Entry(top_frame, font=("Segoe UI", 12))
        self.search_entry.pack(fill="x", pady=5)
        # EN: Bind the Enter key to the search function
        # TR: Enter tuşunu arama fonksiyonuna bağla
        self.search_entry.bind("<Return>", lambda e: self.perform_search())

        search_btn = tk.Button(top_frame, text="Sistemde Ara", bg="#0078D4", fg="white", 
                               font=("Segoe UI", 10, "bold"), command=self.perform_search, cursor="hand2")
        search_btn.pack(fill="x", pady=5)

        # EN: Bottom Panel for Results (Listbox & Scrollbar)
        # TR: Sonuçlar için Alt Panel (Liste kutusu ve Kaydırma çubuğu)
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        scrollbar = tk.Scrollbar(bottom_frame)
        scrollbar.pack(side="right", fill="y")

        self.results_listbox = tk.Listbox(bottom_frame, font=("Consolas", 10), yscrollcommand=scrollbar.set)
        self.results_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.results_listbox.yview)

        # EN: Small button at the bottom to update settings
        # TR: Ayarları güncellemek için en altta küçük buton
        tk.Button(self.root, text="Bağlanti Ayarlarini Güncelle", command=self.open_settings_window, font=("Arial", 8)).pack(pady=5)

    def perform_search(self):
        # EN: Get the search keyword and prepare regex pattern
        # TR: Arama kelimesini al ve regex desenini hazırla
        keyword = self.search_entry.get().strip()
        if not keyword: return
            
        self.results_listbox.delete(0, tk.END)
        # EN: Replace '*' with '.*' for regex wildcard search
        # TR: Regex joker karakter araması için '*' karakterini '.*' ile değiştir
        search_pattern = keyword.replace("*", ".*")
        
        try:
            # EN: Compile the regex pattern (case-insensitive)
            # TR: Regex desenini derle (büyük/küçük harf duyarsız)
            regex = re.compile(f"^{search_pattern}$", re.IGNORECASE)
        except:
            messagebox.showerror("Hata", "Geçersiz arama karakteri!")
            return

        # EN: Search through the schema dictionary
        # TR: Şema sözlüğü içerisinde arama yap
        for table, columns in self.db_schema.items():
            if regex.search(table):
                # EN: If table name matches, list the table and all its columns
                # TR: Tablo adı eşleşirse, tabloyu ve tüm kolonlarını listele
                self.results_listbox.insert(tk.END, f"📁 [TABLO] {table}")
                for col in columns:
                    self.results_listbox.insert(tk.END, f"   🔹 {col}")
                self.results_listbox.insert(tk.END, "-"*40)
            else:
                # EN: If table doesn't match, check individual columns
                # TR: Tablo eşleşmezse, kolonları tek tek kontrol et
                for col in columns:
                    if regex.search(col):
                        self.results_listbox.insert(tk.END, f"   📌 [KOLON] {col}  (Tablo: {table})")

if __name__ == "__main__":
    # EN: Create the main window and run the application
    # TR: Ana pencereyi oluştur ve uygulamayı çalıştır
    root = tk.Tk()
    try:
        root.iconbitmap("db_ikon.ico") 
    except:
        pass
    app = DBSearchApp(root)
    root.mainloop()
