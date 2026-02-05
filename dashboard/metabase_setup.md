# Metabase Dashboard Setup Guide

## 🐳 Setup Metabase dengan Docker

### Prerequisites
- Docker Desktop installed
- Port 3000 available

### Step 1: Pull Metabase Image
```bash
docker pull metabase/metabase:latest
```

### Step 2: Run Metabase Container
```bash
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

### Step 3: Access Metabase
1. Open browser: `http://localhost:3000`
2. Wait for initial setup (2-3 minutes)
3. Create admin account:
   - Email: `root@mail.com`
   - Password: `root123`
   - First Name: Admin
   - Last Name: User

### Step 4: Connect Database

#### Option A: Upload CSV
1. Click "Add Database"
2. Select "Upload CSV"
3. Upload `employee_data.csv`
4. Name: "HR Employee Data"

#### Option B: SQLite (Recommended)
1. Convert CSV to SQLite first:
```python
import pandas as pd
import sqlite3

df = pd.read_csv('employee_data.csv')
conn = sqlite3.connect('hr_data.db')
df.to_sql('employees', conn, if_exists='replace', index=False)
conn.close()
```

2. In Metabase:
   - Click "Add Database"
   - Select "SQLite"
   - Upload `hr_data.db`
   - Name: "HR Database"

## 📊 Creating Dashboards

### Dashboard 1: Executive Summary

**Metrics to Add:**
1. **Total Employees** (Number metric)
   - Query: `COUNT(*) FROM employees`

2. **Attrition Rate** (Percentage)
   - Query: `AVG(Attrition) * 100 FROM employees WHERE Attrition IS NOT NULL`

3. **Attrition Trend** (Line Chart)
   - X-axis: YearsAtCompany
   - Y-axis: AVG(Attrition)
   - Group by: YearsAtCompany

4. **Department Breakdown** (Pie Chart)
   - Dimension: Department
   - Metric: AVG(Attrition) * 100

### Dashboard 2: Demographic Analysis

**Visualizations:**
1. **Age Distribution** (Histogram)
   - Bins: Age
   - Color by: Attrition

2. **Gender Analysis** (Bar Chart)
   - X: Gender
   - Y: Attrition Rate

3. **Marital Status** (Bar Chart)
   - X: MaritalStatus
   - Y: Attrition Rate

### Dashboard 3: Job & Compensation

**Visualizations:**
1. **Attrition by Department** (Bar Chart)
   - X: Department
   - Y: AVG(Attrition) * 100

2. **Attrition by Job Role** (Horizontal Bar)
   - Y: JobRole
   - X: Attrition Rate

3. **Income Distribution** (Box Plot)
   - Category: Attrition
   - Value: MonthlyIncome

4. **Overtime Impact** (Bar Chart)
   - X: OverTime
   - Y: Attrition Rate

### Dashboard 4: Work Environment

**Visualizations:**
1. **Work-Life Balance** (Bar Chart)
   - X: WorkLifeBalance (1-4)
   - Y: Attrition Rate

2. **Job Satisfaction** (Bar Chart)
   - X: JobSatisfaction (1-4)
   - Y: Attrition Rate

3. **Environment Satisfaction** (Heatmap)
   - Rows: EnvironmentSatisfaction
   - Columns: Department
   - Value: Attrition Rate

### Dashboard 5: Career Development

**Visualizations:**
1. **Tenure Distribution** (Histogram)
   - X: YearsAtCompany
   - Color: Attrition

2. **Promotion Gap** (Scatter Plot)
   - X: YearsAtCompany
   - Y: YearsSinceLastPromotion
   - Color: Attrition

3. **Training Impact** (Bar Chart)
   - X: TrainingTimesLastYear
   - Y: Attrition Rate

## 🎨 Dashboard Design Tips

### Color Scheme
- **Attrition = 1 (Left)**: Red (#e74c3c)
- **Attrition = 0 (Stay)**: Green (#2ecc71)
- **Neutral**: Blue (#3498db)

### Layout Best Practices
1. **Top Row**: KPIs (big numbers)
2. **Middle Rows**: Main visualizations
3. **Bottom Row**: Detailed tables
4. **Filters**: Top-right corner

### Filters to Add
- Department (Dropdown)
- Job Role (Dropdown)
- Age Range (Slider)
- Income Range (Slider)
- Years at Company (Slider)

## 📥 Export Dashboard

### Export Metabase Database
```bash
docker cp metabase:/metabase.db/metabase.db.mv.db ./
```

This will create `metabase.db.mv.db` in your current directory.

### Backup Dashboard
1. Go to Settings → Admin → Troubleshooting
2. Click "Download Diagnostic Info"
3. Save the JSON file

## 🔄 Restore Dashboard

### Import Metabase Database
```bash
docker cp metabase.db.mv.db metabase:/metabase.db/
docker restart metabase
```

## 📱 Sharing Dashboard

### Option 1: Public Link
1. Open dashboard
2. Click "Share" icon
3. Enable "Public link"
4. Copy and share URL

### Option 2: Email Subscription
1. Open dashboard
2. Click "Subscribe"
3. Add email addresses
4. Set frequency (daily/weekly)

## 🛠️ Troubleshooting

### Issue: Port 3000 already in use
```bash
docker run -d -p 3001:3000 --name metabase metabase/metabase
```
Then access at `http://localhost:3001`

### Issue: Container won't start
```bash
docker logs metabase
docker rm metabase
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

### Issue: Database connection failed
- Check file path is correct
- Ensure database file has read permissions
- Try re-uploading the database

## 📚 Additional Resources

- [Metabase Documentation](https://www.metabase.com/docs/latest/)
- [SQL Tutorial](https://www.metabase.com/learn/sql-questions/)
- [Dashboard Best Practices](https://www.metabase.com/learn/dashboards/)

---

**Note**: Pastikan untuk menyimpan `metabase.db.mv.db` untuk submission!
