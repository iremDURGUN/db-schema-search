# 🗂️ DB Schema Search Tool

**TR:** SQL Server veritabanlarındaki tablo ve kolon isimlerini hızlıca aramak için geliştirilmiş masaüstü uygulamasıdır.

**EN:** A desktop application developed to quickly search table and column names in SQL Server databases.

---

##  Özellikler / Features

### ✅ Veritabanı Bağlantısı / Database Connection

**TR:** SQL Server bağlantı bilgileri ilk çalıştırmada kullanıcıdan alınır ve yerel olarak saklanır.

**EN:** SQL Server connection information is requested on first launch and stored locally.

---

### 🔍 Şema Arama / Schema Search

**TR:** `INFORMATION_SCHEMA.COLUMNS` görünümünü kullanarak tüm tablo ve kolon bilgilerini otomatik olarak çeker.

**EN:** Automatically retrieves all table and column information using `INFORMATION_SCHEMA.COLUMNS`.

---

### ⭐ Joker Karakter Desteği / Wildcard Support

**TR:** Aramalarda `*` karakteri kullanılabilir.

Örnek:

```
ST*
*Code
Invoice*
```

**EN:** Supports `*` wildcard searches.

Example:

```
ST*
*Code
Invoice*
```

---

### 📂 Tablo Arama / Table Search

**TR:** Tablo adı bulunduğunda tablo altındaki tüm kolonlar birlikte listelenir.

**EN:** When a table is matched, all of its columns are displayed together.

---

### 📌 Kolon Arama / Column Search

**TR:** Kolon bulunduğunda hangi tabloya ait olduğu gösterilir.

**EN:** When a column is matched, its parent table is displayed.

---

### 💾 Ayarların Kaydedilmesi / Saved Configuration

**TR:** Bağlantı bilgileri `db_settings.json` dosyasında saklanır.

**EN:** Connection settings are stored in the `db_settings.json` file.

---

### 🔄 Bağlantıyı Güncelleme / Update Connection

**TR:** Uygulama içerisinden istenildiğinde bağlantı ayarları değiştirilebilir.

**EN:** Connection settings can be updated at any time from within the application.

---

## 🖥️ Kullanılan Teknolojiler / Technologies

- Python 3
- Tkinter
- pyodbc
- SQL Server
- JSON
- Regular Expressions (Regex)

---

## 📁 Proje Yapısı / Project Structure

```
DB-Schema-Search/
│
├── db_search.py
├── db_settings.json
├── db_ikon.ico
├── README.md
└── requirements.txt
```

## ⚙️ Kurulum ve Çalıştırma / Installation & Running

### 1. Repoyu Klonlayın / Clone the Repository

```bash
git clone https://github.com/iremDURGUN/db-schema-search.git
cd db-schema-search
```

---

### 2. Gereksinimleri Yükleyin / Install Dependencies

```bash
pip install -r requirements.txt
```

**TR:** Sisteminizde **ODBC Driver 17** veya **ODBC Driver 18 for SQL Server** yüklü olmalıdır.

**EN:** **ODBC Driver 17** or **ODBC Driver 18 for SQL Server** must be installed on your system.

---

### 3. Uygulamayı Çalıştırın / Run the Application

```bash
python db_search.py
```

**TR:** İlk çalıştırmada açılan pencereden SQL Server bağlantı bilgilerinizi girin. Bilgiler daha sonraki kullanımlar için **db_settings.json** dosyasına kaydedilecektir.

**EN:** On the first launch, enter your SQL Server connection information in the popup window. The settings will be saved in **db_settings.json** for future use.

---

## ⚠️ Güvenlik Notu / Security Note

**TR:** `db_settings.json` dosyası veritabanı bağlantı bilgilerinizi (kullanıcı adı ve parola) içerdiği için `.gitignore` dosyasına eklenmiştir. Bu dosyayı **asla** herkese açık GitHub depolarına yüklemeyin.

**EN:**  Since the `db_settings.json` file contains your database connection credentials (username and password), it is included in `.gitignore`. **Never** commit or push this file to a public GitHub repository.

---

## 🔎 Arama Örnekleri / Search Examples

| Arama / Search | Açıklama (TR) | Description (EN) |
|----------------|---------------|------------------|
| `Customer` | Customer isimli tablo veya kolonu arar. | Searches for a table or column named Customer. |
| `Cust*` | Cust ile başlayan isimleri bulur. | Finds names starting with Cust. |
| `*Code` | Code ile biten isimleri bulur. | Finds names ending with Code. |
| `*Date*` | İçerisinde Date geçen tüm isimleri bulur. | Finds all names containing Date. |

---

## 📌 Kullanım Senaryoları / Use Cases

**TR**

- ERP projelerinde tablo araştırması
- SQL geliştirme süreçleri
- Veri analizi öncesinde şema inceleme
- Yeni geliştiriciler için veritabanını keşfetme
- Büyük SQL Server veritabanlarında hızlı arama

**EN**

- ERP database exploration
- SQL development
- Database schema analysis
- Learning unfamiliar databases
- Fast lookup in large SQL Server databases

---
