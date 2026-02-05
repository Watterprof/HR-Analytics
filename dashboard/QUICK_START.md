# 🚀 Quick Start Guide - HR Analytics Dashboard

## Langkah Cepat Setup Dashboard (15 menit)

### 1. Install Docker Desktop
- Download: https://www.docker.com/products/docker-desktop
- Install dan restart komputer jika diminta
- Pastikan Docker running (icon di system tray)

### 2. Jalankan Metabase
Buka PowerShell/Terminal dan jalankan:

```bash
docker pull metabase/metabase:latest
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

### 3. Setup Metabase (First Time)
1. Buka browser: `http://localhost:3000`
2. Tunggu 2-3 menit untuk initial setup
3. Klik "Let's get started"
4. Isi form:
   - **Email**: `root@mail.com`
   - **Password**: `root123`
   - **First Name**: Admin
   - **Last Name**: User
5. Klik "Next"

### 4. Connect Database

#### Option A: SQLite (Recommended)
Buat database SQLite terlebih dahulu:

```python
import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv('employee_data.csv')

# Create SQLite database
conn = sqlite3.connect('hr_data.db')
df.to_sql('employees', conn, if_exists='replace', index=False)
conn.close()

print("Database created: hr_data.db")
```

Di Metabase:
1. Klik "Add a database"
2. Pilih "SQLite"
3. **Name**: HR Database
4. **Filename**: Browse dan pilih `hr_data.db`
5. Klik "Save"

#### Option B: Upload CSV (Simple)
1. Klik "Upload data"
2. Pilih `employee_data.csv`
3. **Table name**: employees
4. Klik "Upload"

### 5. Buat Dashboard Pertama

#### Executive Summary Dashboard

**Step 1: Create Dashboard**
1. Klik "New" → "Dashboard"
2. Name: "HR Analytics - Executive Summary"
3. Klik "Create"

**Step 2: Add KPI Cards**

**Card 1: Total Employees**
- Click "Add a question"
- Simple question → employees table
- Summarize: Count
- Visualization: Number
- Title: "Total Employees"

**Card 2: Attrition Rate**
- New question → Custom query:
```sql
SELECT AVG(Attrition) * 100 as AttritionRate
FROM employees
WHERE Attrition IS NOT NULL
```
- Visualization: Number
- Settings → Add "%" suffix
- Title: "Attrition Rate"

**Card 3: Department Breakdown**
- Simple question → employees
- Group by: Department
- Summarize: Count
- Visualization: Pie chart
- Title: "Employees by Department"

**Card 4: Attrition by Department**
- Custom query:
```sql
SELECT Department, AVG(Attrition) * 100 as AttritionRate
FROM employees
WHERE Attrition IS NOT NULL
GROUP BY Department
ORDER BY AttritionRate DESC
```
- Visualization: Bar chart
- Title: "Attrition Rate by Department"

### 6. Buat Dashboard Lainnya

Ulangi proses di atas untuk 4 dashboard lainnya:
- Demographics Analysis
- Job & Compensation
- Work Environment
- Career Development

Lihat detail di `dashboard/metabase_setup.md`

### 7. Export Dashboard

Setelah selesai membuat semua dashboard:

```bash
docker cp metabase:/metabase.db/metabase.db.mv.db ./
```

File `metabase.db.mv.db` akan tersimpan di folder project Anda.

---

## 🎨 Tips Dashboard yang Bagus

### Visualisasi yang Efektif
- ✅ **Bar Chart**: Untuk perbandingan kategori
- ✅ **Line Chart**: Untuk trend over time
- ✅ **Pie Chart**: Untuk proporsi (max 5-6 kategori)
- ✅ **Number**: Untuk KPI penting
- ✅ **Table**: Untuk detail data

### Color Scheme
- **Attrition (Left)**: Red (#e74c3c)
- **Retention (Stay)**: Green (#2ecc71)
- **Neutral/Info**: Blue (#3498db)

### Layout Best Practices
```
┌─────────────────────────────────────────┐
│  KPI 1    │  KPI 2    │  KPI 3    │     │  ← Top: Big numbers
├─────────────────────────────────────────┤
│                                         │
│        Main Visualization 1             │  ← Middle: Main charts
│                                         │
├─────────────────────────────────────────┤
│  Chart 2          │  Chart 3            │  ← Bottom: Supporting
└─────────────────────────────────────────┘
```

### Filters to Add
- Department (Dropdown)
- Job Role (Dropdown)
- Age Range (Slider)
- Income Range (Slider)

---

## ❓ Troubleshooting

### Docker tidak bisa start
```bash
# Check Docker status
docker ps

# Restart Docker Desktop
# Right-click Docker icon → Restart

# Try again
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

### Port 3000 sudah dipakai
```bash
# Use different port
docker run -d -p 3001:3000 --name metabase metabase/metabase
# Access at http://localhost:3001
```

### Container sudah ada
```bash
# Remove old container
docker rm -f metabase

# Create new one
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

### Database connection error
- Pastikan path file database benar
- Coba upload CSV langsung sebagai alternatif
- Restart Metabase container

---

## 📊 Sample SQL Queries

### Attrition by Age Group
```sql
SELECT 
    CASE 
        WHEN Age < 30 THEN '<30'
        WHEN Age < 40 THEN '30-40'
        WHEN Age < 50 THEN '40-50'
        ELSE '50+'
    END as AgeGroup,
    AVG(Attrition) * 100 as AttritionRate,
    COUNT(*) as EmployeeCount
FROM employees
WHERE Attrition IS NOT NULL
GROUP BY AgeGroup
ORDER BY AgeGroup
```

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
ORDER BY 
    CASE IncomeLevel
        WHEN 'Low' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'High' THEN 3
        ELSE 4
    END
```

---

## ✅ Checklist Dashboard

- [ ] Metabase running di `http://localhost:3000`
- [ ] Login dengan `root@mail.com` / `root123`
- [ ] Database connected
- [ ] Dashboard 1: Executive Summary (4+ visualizations)
- [ ] Dashboard 2: Demographics (3+ visualizations)
- [ ] Dashboard 3: Job & Compensation (4+ visualizations)
- [ ] Dashboard 4: Work Environment (3+ visualizations)
- [ ] Dashboard 5: Career Development (3+ visualizations)
- [ ] Filters added (Department, Job Role)
- [ ] Colors consistent (Red for attrition, Green for retention)
- [ ] Dashboard user-friendly dan mudah dipahami
- [ ] Exported `metabase.db.mv.db`

---

**Estimated Time**: 1-2 hours untuk membuat semua dashboard

**Need Help?** Lihat dokumentasi lengkap di `dashboard/metabase_setup.md`
