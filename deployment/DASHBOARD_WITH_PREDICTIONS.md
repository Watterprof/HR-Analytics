# Menambahkan Prediksi ML ke Dashboard

Database sudah diupdate dengan hasil prediksi ML. Sekarang Anda bisa membuat visualisasi baru di Metabase.

## Kolom Baru yang Tersedia

Setelah menjalankan `update_database_with_predictions.py`, database memiliki 3 kolom tambahan:

1. **PredictedAttrition**: 0 (Will Stay) atau 1 (Will Leave)
2. **AttritionProbability**: Probabilitas attrition dalam persen (0-100%)
3. **RiskLevel**: Kategori risiko (Low/Medium/High)

## Cara Membuat Visualisasi di Metabase

### 1. Akses Metabase

```bash
# Buka browser dan ketik:
http://localhost:3000

# Login dengan credentials Anda
```

### 2. Buat Dashboard Baru atau Edit yang Sudah Ada

Klik **"New"** → **"Dashboard"** atau edit dashboard "HR Analytics - Executive Summary" yang sudah ada.

### 3. Visualisasi yang Bisa Dibuat

#### A. Risk Level Distribution (Pie Chart)

**SQL Query:**
```sql
SELECT RiskLevel, COUNT(*) as EmployeeCount
FROM employees
GROUP BY RiskLevel
ORDER BY 
  CASE RiskLevel
    WHEN 'High' THEN 1
    WHEN 'Medium' THEN 2
    WHEN 'Low' THEN 3
  END
```

**Visualization**: Pie Chart  
**Title**: "Employee Risk Distribution"

---

#### B. High Risk Employees by Department (Bar Chart)

**SQL Query:**
```sql
SELECT Department, COUNT(*) as HighRiskCount
FROM employees
WHERE RiskLevel = 'High'
GROUP BY Department
ORDER BY HighRiskCount DESC
```

**Visualization**: Bar Chart  
**Title**: "High Risk Employees by Department"

---

#### C. Attrition Probability Distribution (Histogram)

**SQL Query:**
```sql
SELECT 
  CASE 
    WHEN AttritionProbability < 20 THEN '0-20%'
    WHEN AttritionProbability < 40 THEN '20-40%'
    WHEN AttritionProbability < 60 THEN '40-60%'
    WHEN AttritionProbability < 80 THEN '60-80%'
    ELSE '80-100%'
  END as ProbabilityRange,
  COUNT(*) as EmployeeCount
FROM employees
GROUP BY ProbabilityRange
ORDER BY ProbabilityRange
```

**Visualization**: Bar Chart  
**Title**: "Attrition Probability Distribution"

---

#### D. Top 10 High Risk Employees (Table)

**SQL Query:**
```sql
SELECT 
  EmployeeId,
  Department,
  JobRole,
  MonthlyIncome,
  YearsAtCompany,
  AttritionProbability,
  RiskLevel
FROM employees
WHERE RiskLevel = 'High'
ORDER BY AttritionProbability DESC
LIMIT 10
```

**Visualization**: Table  
**Title**: "Top 10 High Risk Employees"

---

#### E. Average Risk by Department (Bar Chart)

**SQL Query:**
```sql
SELECT 
  Department,
  ROUND(AVG(AttritionProbability), 2) as AvgRiskPercent,
  COUNT(*) as TotalEmployees
FROM employees
GROUP BY Department
ORDER BY AvgRiskPercent DESC
```

**Visualization**: Bar Chart  
**Title**: "Average Attrition Risk by Department"

---

#### F. Risk by Job Role (Horizontal Bar)

**SQL Query:**
```sql
SELECT 
  JobRole,
  ROUND(AVG(AttritionProbability), 2) as AvgRisk,
  COUNT(*) as EmployeeCount
FROM employees
GROUP BY JobRole
HAVING EmployeeCount >= 5
ORDER BY AvgRisk DESC
LIMIT 10
```

**Visualization**: Horizontal Bar Chart  
**Title**: "Top 10 Job Roles by Attrition Risk"

---

#### G. Risk Level by Overtime (Stacked Bar)

**SQL Query:**
```sql
SELECT 
  OverTime,
  RiskLevel,
  COUNT(*) as EmployeeCount
FROM employees
GROUP BY OverTime, RiskLevel
ORDER BY OverTime, 
  CASE RiskLevel
    WHEN 'High' THEN 1
    WHEN 'Medium' THEN 2
    WHEN 'Low' THEN 3
  END
```

**Visualization**: Stacked Bar Chart  
**Title**: "Risk Level by Overtime Status"

---

## Langkah-Langkah Menambahkan Visualisasi

### Step 1: Buat Question Baru

1. Di dashboard, klik tombol **"+"** atau **"Add a question"**
2. Pilih **"Native query"** (untuk SQL) atau **"Simple question"** (untuk GUI)
3. Pilih database: **"HR Database"**

### Step 2: Tulis Query

Paste salah satu SQL query di atas

### Step 3: Run dan Visualize

1. Klik **"Run query"** (tombol play)
2. Pilih visualization type (Pie, Bar, Table, dll)
3. Customize settings (colors, labels, dll)

### Step 4: Save dan Add to Dashboard

1. Klik **"Save"**
2. Beri nama sesuai title yang disarankan
3. Pilih **"Add to dashboard"**
4. Pilih dashboard yang ingin ditambahkan

### Step 5: Arrange Dashboard

Drag and drop visualisasi untuk mengatur layout yang rapi.

---

## Recommended Dashboard Layout

```
┌─────────────────────────────────────────────────────┐
│  Total Employees  │  Attrition Rate  │  High Risk   │
│      1,470        │     16.92%       │     633      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Risk Level Distribution (Pie)                     │
│                                                     │
├──────────────────────┬──────────────────────────────┤
│                      │                              │
│  High Risk by Dept   │  Avg Risk by Department     │
│  (Bar Chart)         │  (Bar Chart)                │
│                      │                              │
├──────────────────────┴──────────────────────────────┤
│                                                     │
│  Top 10 High Risk Employees (Table)                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Tips

1. **Color Coding**: 
   - High Risk: Red (#e74c3c)
   - Medium Risk: Orange (#f39c12)
   - Low Risk: Green (#2ecc71)

2. **Filters**: Tambahkan filters untuk:
   - Department
   - Risk Level
   - Job Role

3. **Auto-refresh**: Set dashboard untuk auto-refresh setiap hari

4. **Export**: Setelah selesai, export dashboard:
   ```bash
   docker cp metabase:/metabase.db/metabase.db.mv.db ./metabase_with_predictions.db.mv.db
   ```

---

## Verifikasi

Untuk memastikan data prediksi sudah tersedia:

1. Di Metabase, buka **"Browse Data"**
2. Pilih database **"HR Database"**
3. Pilih table **"employees"**
4. Scroll ke kanan, Anda akan lihat kolom:
   - PredictedAttrition
   - AttritionProbability  
   - RiskLevel

Jika kolom tersebut ada, berarti database sudah berhasil diupdate!

---

**File ini**: `deployment/DASHBOARD_WITH_PREDICTIONS.md`
