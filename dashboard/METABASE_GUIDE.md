# 🎉 METABASE SUDAH RUNNING!

## ✅ Status: Container Metabase Berhasil Dijalankan

Container ID: `93f3b547d8c3`
Port: `3000`
Status: Running

---

## 🚀 LANGKAH SELANJUTNYA (Ikuti Ini!)

### 1. Buka Browser
Buka browser favorit Anda (Chrome/Edge/Firefox) dan ketik:

```
http://localhost:3000
```

**PENTING**: Tunggu 2-3 menit untuk initial setup Metabase. Halaman akan loading dulu.

---

### 2. Setup Account Metabase

Setelah halaman terbuka, Anda akan lihat "Welcome to Metabase". Klik **"Let's get started"**

Isi form:
- **Email**: `root@mail.com`
- **Password**: `root123`
- **First Name**: Admin
- **Last Name**: User
- **Company**: HR Analytics

Klik **"Next"**

---

### 3. Skip Database Connection (Untuk Sekarang)

Di halaman "Add your data":
- Klik **"I'll add my data later"** (di bagian bawah)

---

### 4. Preferences

Di halaman preferences:
- Allow anonymous usage data: **Pilih sesuai preferensi**
- Klik **"Finish"**

---

### 5. Upload Data Employee

Setelah masuk ke dashboard Metabase:

**Option A: Upload CSV Langsung**
1. Klik icon **"+"** di kanan atas
2. Pilih **"Upload data"**
3. Browse dan pilih file `employee_data.csv`
4. Table name: `employees`
5. Klik **"Upload"**

**Option B: Buat SQLite Database (Recommended)**

Buka terminal/PowerShell dan jalankan:

```python
python -c "import pandas as pd; import sqlite3; df = pd.read_csv('employee_data.csv'); conn = sqlite3.connect('hr_data.db'); df.to_sql('employees', conn, if_exists='replace', index=False); conn.close(); print('Database created!')"
```

Kemudian di Metabase:
1. Klik **"Settings"** (icon gear) → **"Admin settings"**
2. Klik **"Databases"** → **"Add database"**
3. Pilih **"SQLite"**
4. Name: `HR Database`
5. Filename: Browse dan pilih `hr_data.db`
6. Klik **"Save"**

---

### 6. Buat Dashboard Pertama

#### Dashboard 1: Executive Summary

1. Klik **"New"** → **"Dashboard"**
2. Name: `HR Analytics - Executive Summary`
3. Klik **"Create"**

**Tambahkan Visualisasi:**

**Card 1: Total Employees**
- Klik **"Add a question"**
- Pilih **"Simple question"**
- Table: `employees`
- Summarize: **Count**
- Visualization: **Number**
- Title: `Total Employees`
- Save

**Card 2: Attrition Rate**
- Klik **"New question"** → **"Native query"**
- Paste SQL:
```sql
SELECT AVG(Attrition) * 100 as AttritionRate
FROM employees
WHERE Attrition IS NOT NULL
```
- Run query
- Visualization: **Number**
- Settings → Add suffix: `%`
- Title: `Attrition Rate (%)`
- Save

**Card 3: Employees by Department**
- Simple question → `employees` table
- Group by: `Department`
- Summarize: **Count**
- Visualization: **Pie chart**
- Title: `Employees by Department`
- Save

**Card 4: Attrition by Department**
- Native query:
```sql
SELECT Department, AVG(Attrition) * 100 as AttritionRate
FROM employees
WHERE Attrition IS NOT NULL
GROUP BY Department
ORDER BY AttritionRate DESC
```
- Visualization: **Bar chart**
- Title: `Attrition Rate by Department`
- Save

---

### 7. Dashboard Lainnya (Opsional - Untuk Nilai Lebih Tinggi)

Buat 4 dashboard tambahan dengan visualisasi:

**Dashboard 2: Demographics**
- Age distribution
- Gender analysis
- Marital status impact

**Dashboard 3: Job & Compensation**
- Attrition by job role
- Income distribution
- Overtime impact

**Dashboard 4: Work Environment**
- Work-life balance
- Job satisfaction
- Environment satisfaction

**Dashboard 5: Career Development**
- Years at company
- Promotion gap
- Training impact

Lihat detail SQL queries di `dashboard/QUICK_START.md`

---

### 8. Export Dashboard (PENTING!)

Setelah selesai membuat dashboard:

Buka PowerShell/Terminal dan jalankan:

```bash
docker cp metabase:/metabase.db/metabase.db.mv.db ./
```

File `metabase.db.mv.db` akan tersimpan di folder project Anda.

**INI FILE YANG HARUS DI-SUBMIT!**

---

## 📊 Sample SQL Queries

### Overtime Impact
```sql
SELECT 
    OverTime,
    AVG(Attrition) * 100 as AttritionRate,
    COUNT(*) as EmployeeCount
FROM employees
WHERE Attrition IS NOT NULL
GROUP BY OverTime
```

### Income vs Attrition
```sql
SELECT 
    CASE 
        WHEN MonthlyIncome < 3000 THEN 'Low'
        WHEN MonthlyIncome < 6000 THEN 'Medium'
        WHEN MonthlyIncome < 10000 THEN 'High'
        ELSE 'Very High'
    END as IncomeLevel,
    AVG(Attrition) * 100 as AttritionRate,
    COUNT(*) as EmployeeCount
FROM employees
WHERE Attrition IS NOT NULL
GROUP BY IncomeLevel
```

### Work-Life Balance
```sql
SELECT 
    WorkLifeBalance,
    AVG(Attrition) * 100 as AttritionRate,
    COUNT(*) as EmployeeCount
FROM employees
WHERE Attrition IS NOT NULL
GROUP BY WorkLifeBalance
ORDER BY WorkLifeBalance
```

---

## 🎨 Tips Dashboard yang Bagus

### Color Scheme
- **Attrition (Left)**: Red `#e74c3c`
- **Retention (Stay)**: Green `#2ecc71`
- **Info**: Blue `#3498db`

### Layout
```
┌─────────────────────────────────────────┐
│  KPI 1    │  KPI 2    │  KPI 3          │  ← Top: Big numbers
├─────────────────────────────────────────┤
│                                         │
│        Main Chart                       │  ← Middle: Main viz
│                                         │
├─────────────────────────────────────────┤
│  Chart 2          │  Chart 3            │  ← Bottom: Supporting
└─────────────────────────────────────────┘
```

### Filters
Tambahkan filters di dashboard:
- Department (Dropdown)
- Job Role (Dropdown)
- Age Range (Slider)

---

## ✅ Checklist

- [ ] Buka `http://localhost:3000` di browser
- [ ] Setup account (`root@mail.com` / `root123`)
- [ ] Upload `employee_data.csv` atau buat SQLite database
- [ ] Buat Dashboard 1: Executive Summary (minimal 4 visualizations)
- [ ] (Optional) Buat 4 dashboard lainnya
- [ ] Export `metabase.db.mv.db`
- [ ] Pastikan file tersimpan di folder project

---

## ❓ Troubleshooting

**Metabase tidak bisa dibuka?**
```bash
# Cek container running
docker ps

# Restart container jika perlu
docker restart metabase

# Tunggu 2-3 menit, lalu buka http://localhost:3000
```

**Port 3000 sudah dipakai?**
```bash
# Stop container lama
docker stop metabase
docker rm metabase

# Buat dengan port berbeda
docker run -d -p 3001:3000 --name metabase metabase/metabase:latest
# Akses di http://localhost:3001
```

---

**Estimated Time**: 1-2 jam untuk membuat dashboard lengkap

**Need More Help?** Lihat `dashboard/QUICK_START.md` untuk detail lebih lengkap!
