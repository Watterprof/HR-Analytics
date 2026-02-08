# Proyek Akhir: Menyelesaikan Permasalahan HR - Employee Attrition

## Business Understanding

Perusahaan menghadapi tantangan dalam mengelola tingkat attrition (karyawan keluar) yang berdampak signifikan terhadap operasional dan biaya. Tingginya tingkat attrition menyebabkan peningkatan biaya rekrutmen, hilangnya produktivitas, dan penurunan moral tim. Proyek ini bertujuan untuk mengidentifikasi faktor-faktor yang mempengaruhi keputusan karyawan untuk keluar dan membangun sistem prediksi untuk intervensi dini.

### Permasalahan Bisnis

1. **Tingkat Attrition yang Tinggi**: Perusahaan mengalami attrition rate sebesar 16.92%, yang mengakibatkan biaya rekrutmen dan training yang signifikan.

2. **Kurangnya Visibilitas**: Tidak ada sistem untuk mengidentifikasi karyawan yang berisiko tinggi keluar sebelum mereka mengundurkan diri.

3. **Biaya Operasional**: Setiap karyawan yang keluar membutuhkan biaya rata-rata $4,000 untuk rekrutmen, onboarding, dan training pengganti.

4. **Hilangnya Produktivitas**: Transisi karyawan menyebabkan penurunan produktivitas tim dan hilangnya knowledge organisasi.

5. **Departemen Tertentu Lebih Rentan**: Sales dan HR department menunjukkan attrition rate tertinggi (19-20%), namun belum ada strategi retensi spesifik.

### Cakupan Proyek

Proyek ini mencakup:

1. **Analisis Data Eksploratif**: Mengidentifikasi pola dan faktor-faktor yang berkorelasi dengan attrition melalui visualisasi dan statistical analysis.

2. **Machine Learning Modeling**: Membangun model prediksi menggunakan tiga algoritma (Logistic Regression, Random Forest, XGBoost) untuk memprediksi karyawan yang berisiko keluar.

3. **Business Dashboard**: Membuat dashboard interaktif menggunakan Metabase untuk monitoring real-time tingkat attrition per departemen dan faktor-faktor kunci.

4. **Deployment System**: Mengembangkan script Python untuk prediksi individual dan batch prediction untuk semua karyawan.

5. **Rekomendasi Strategis**: Menyusun action items yang dapat ditindaklanjuti oleh HR department untuk mengurangi attrition.

### Persiapan

Sumber data: Dataset internal perusahaan berisi informasi 1,470 karyawan dengan 35 variabel meliputi data demografis, pekerjaan, kompensasi, dan kepuasan kerja.

Setup environment:

```bash
# Install dependencies
pip install pandas numpy matplotlib seaborn scikit-learn xgboost joblib

# Jalankan Jupyter Notebook
jupyter notebook

# Atau gunakan VS Code untuk membuka notebook.ipynb
```

## Business Dashboard

Dashboard interaktif telah dibuat menggunakan Metabase dengan 4 visualisasi utama:

1. **Total Employees**: Menampilkan jumlah total karyawan (1,470)
2. **Attrition Rate**: Tingkat attrition keseluruhan perusahaan (16.92%)
3. **Employees by Department**: Distribusi karyawan per departemen dalam bentuk pie chart
4. **Attrition by Department**: Perbandingan tingkat attrition antar departemen dalam bentuk bar chart

### Cara Mengakses Dashboard

Dashboard dapat diakses melalui Metabase dengan langkah berikut:

```bash
# Jalankan Metabase container
docker run -d -p 3000:3000 --name metabase metabase/metabase:latest

# Akses melalui browser
http://localhost:3000
```

Database file `metabase.db.mv.db` sudah tersedia di repository dan dapat di-import untuk melihat dashboard yang telah dibuat.

### Insight dari Dashboard

- Sales department memiliki attrition rate tertinggi (20%)
- Human Resources menunjukkan tingkat attrition 19%
- Research & Development memiliki attrition rate terendah (14%)
- Terdapat korelasi kuat antara overtime, income level, dan work-life balance dengan tingkat attrition

## Menjalankan Sistem Prediksi

### Prediksi Individual

```bash
cd deployment
python predict.py --json_file sample_employee.json
```

### Batch Prediction (Semua Karyawan)

```bash
cd deployment
python batch_predict.py
```

Script ini akan menghasilkan:
- Report lengkap di console
- File CSV `attrition_risk_report.csv` dengan detail semua karyawan
- Daftar high-risk employees dengan rekomendasi spesifik
- Action plan untuk HR department

## Conclusion

Proyek ini berhasil mengidentifikasi 6 faktor utama yang mempengaruhi attrition karyawan:

1. **Overtime**: Karyawan dengan overtime tinggi memiliki risiko 2-3x lebih tinggi
2. **Monthly Income**: Kompensasi di bawah market rate meningkatkan risiko attrition
3. **Work-Life Balance**: Skor rendah berkorelasi kuat dengan keputusan keluar
4. **Years at Company**: Karyawan baru (0-2 tahun) paling berisiko
5. **Job Satisfaction**: Predictor kuat untuk attrition
6. **Department**: Sales dan HR memiliki attrition rate tertinggi

Model machine learning yang dikembangkan menggunakan Random Forest Classifier mencapai performa:
- **Accuracy**: 87% (melebihi target 80%)
- **Precision**: 84%
- **Recall**: 78%
- **ROC-AUC**: 88%

Dengan implementasi sistem prediksi dan rekomendasi yang diberikan, perusahaan dapat:
- Mengidentifikasi karyawan berisiko tinggi secara proaktif
- Melakukan intervensi dini sebelum karyawan memutuskan keluar
- Mengurangi attrition rate sebesar 20-30%
- Menghemat biaya rekrutmen $500,000 - $1,000,000 per tahun

### Rekomendasi Action Items

**Prioritas Tinggi (1-3 Bulan):**

1. **Implementasi Monitoring System**: Deploy batch prediction script untuk dijalankan setiap bulan, mengidentifikasi high-risk employees, dan membuat alert otomatis untuk HR.

2. **Program Intervensi untuk High-Risk Employees**: Conduct stay interviews dengan 633 karyawan yang teridentifikasi high-risk, review kompensasi, dan buat retention plan individual.

3. **Reduksi Overtime**: Kurangi overtime hingga 30% terutama di Sales department dengan menambah resources atau redistribusi workload untuk 176 karyawan yang teridentifikasi.

4. **Review Kompensasi**: Lakukan salary adjustment untuk 211 karyawan dengan income di bawah market rate, terutama di posisi entry-level dan mid-level.

5. **Enhanced Onboarding Program**: Implementasi structured 90-day onboarding dengan buddy system dan weekly check-ins untuk karyawan baru (fokus pada 0-2 tahun masa kerja).

**Prioritas Menengah (3-6 Bulan):**

6. **Work-Life Balance Initiatives**: Implementasi flexible working hours dan remote work options 2-3 hari per minggu, terutama untuk departemen dengan work-life balance score rendah.

7. **Career Development Program**: Buat career pathway yang jelas untuk setiap role, program mentorship terstruktur, dan review promotion criteria untuk karyawan dengan YearsSinceLastPromotion > 3 tahun.

8. **Department-Specific Strategies**: 
   - Sales: Review sales targets dan improve commission structure
   - HR: Workload analysis dan career progression opportunities
   - R&D: Maintain current practices (performing well)

9. **Employee Engagement Programs**: Quarterly satisfaction surveys, regular town halls, employee recognition programs, dan improve workspace facilities.

10. **Manager Training**: Training untuk managers tentang retention best practices, cara conduct stay interviews, dan recognition techniques.

**Prioritas Jangka Panjang (6-12 Bulan):**

11. **Kompensasi dan Benefit Review**: Benchmark salary dengan market rate setiap 6 bulan, tingkatkan stock options, dan implementasi performance-based bonus yang kompetitif.

12. **Culture Building**: Develop retention culture melalui alumni network, employee referral programs, dan continuous feedback loops.

13. **Model Retraining**: Update model machine learning setiap 6 bulan dengan data attrition terbaru untuk meningkatkan akurasi prediksi.

14. **ROI Measurement**: Track dan measure effectiveness dari setiap intervention, calculate cost savings, dan adjust strategies berdasarkan hasil.

---

**Author**: Mahdi Shidqi  
**Email**: m128d5y1057@student.devacademy.id  
**ID Dicoding**: m128d5y1057  
**GitHub Repository**: https://github.com/Watterprof/HR-Analytics.git
