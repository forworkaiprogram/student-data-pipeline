# Student Data Pipeline — Multi-Source Data Integration

> مشروع هندسة بيانات احترافي يدمج بيانات الطلاب من **5 مصادر مختلفة** في Dataset موحد جاهز للتحليل والـ Machine Learning.

---

## 📖 1. Project Overview

في بيئات العمل الحقيقية، نادراً ما تكون البيانات موجودة في مصدر واحد. هذا المشروع يحاكي سيناريو واقعياً في مؤسسة تعليمية، حيث تكون بيانات الطلاب موزعة على أنظمة مختلفة.

**الهدف:** بناء Pipeline متكامل يجمع البيانات من 5 مصادر، ينظفها، يتحقق من جودتها، يدمجها، ويحفظها في ملف CSV نهائي جاهز للاستخدام.

---

## 🏗️ 2. Architecture

### هيكل المشروع
student_data_pipeline/
│
├── app/
│ ├── init.py
│ ├── config.py # الإعدادات المركزية
│ ├── sources/ # طبقة الاستخراج
│ │ ├── init.py
│ │ ├── csv_source.py # CSV
│ │ ├── postgres_source.py # PostgreSQL
│ │ ├── mongodb_source.py # MongoDB
│ │ ├── html_source.py # HTML Scraping
│ │ └── api_source.py # REST API
│ ├── transformation/ # طبقة التحويل
│ │ ├── init.py
│ │ ├── cleaner.py # تنظيف
│ │ ├── transformer.py # تحويل
│ │ └── integration.py # دمج
│ ├── validation/ # طبقة التحقق
│ │ ├── init.py
│ │ └── quality.py
│ ├── output/ # طبقة الإخراج
│ │ ├── init.py
│ │ └── csv_writer.py
│ └── utils/
│ ├── init.py
│ └── logger.py
│
├── data/
│ ├── raw/ # البيانات الخام
│ │ ├── students.csv
│ │ ├── courses.html
│ │ └── setup_mongodb.py
│ ├── processed/ # البيانات المعالجة
│ │ └── final_dataset.csv
│ └── rejected/ # السجلات المرفوضة
│ └── rejected_records.csv
│
├── database/
│ └── setup_postgres.sql
│
├── logs/
│ └── pipeline.log
│
├── tests/
│ └── test_pipeline.py
│
├── main.py
├── requirements.txt
└── README.md
text


### الطبقات (Layers)

┌─────────────────────────────────────────────────┐
│ SOURCES (5 مصادر) │
│ CSV │ PostgreSQL │ MongoDB │ HTML │ REST API │
└──────────────────┬──────────────────────────────┘
↓
┌─────────────────────────────────────────────────┐
│ TRANSFORMATION │
│ Clean → Integrate → Transform │
└──────────────────┬──────────────────────────────┘
↓
┌─────────────────────────────────────────────────┐
│ VALIDATION (7 قواعد) │
│ Valid Records ─→ Output │
│ Invalid Records ─→ Rejected │
└──────────────────┬──────────────────────────────┘
↓
┌─────────────────────────────────────────────────┐
│ OUTPUT │
│ final_dataset.csv │ rejected_records.csv │
└─────────────────────────────────────────────────┘
text


---

## 📊 3. Data Sources

| # | المصدر | التقنية | نوع البيانات | الحقول الرئيسية |
|---|--------|---------|--------------|-----------------|
| 1 | **CSV** | ملف نصي | بيانات الطلاب الأساسية | student_id, name, age, major, city |
| 2 | **PostgreSQL** | قاعدة بيانات علائقية | سجلات أكاديمية + تسجيلات | gpa, attendance, score, courses |
| 3 | **MongoDB** | قاعدة بيانات NoSQL | أنشطة وسلوك | clubs, participation_score, behavior |
| 4 | **HTML** | Web Scraping | كتالوج المقررات | course_name, instructor, level |
| 5 | **REST API** | HTTP | حالة التسجيل | registration_status, semester |

**المفتاح المشترك للدمج:** `student_id`

---

## 🔄 4. ETL Pipeline

### المراحل

#### 1️⃣ Extract — الاستخراج
- قراءة البيانات من 5 مصادر مختلفة
- كل مصدر له وحدته الخاصة في `app/sources/`

#### 2️⃣ Clean — التنظيف
- إزالة المسافات الزائدة (`re.sub`)
- توحيد حالة الأحرف (Title Case)
- إزالة التكرارات (`drop_duplicates`)
- معالجة القيم المفقودة

#### 3️⃣ Integrate — الدمج
- دمج البيانات على `student_id`
- استخدام `left join` للحفاظ على كل السجلات
- إثراء CSV ببيانات من باقي المصادر

#### 4️⃣ Transform — التحويل
- تحويل الأنواع (`age`: int، `gpa`: float)
- إضافة الأعمدة المشتقة

#### 5️⃣ Validate — التحقق
- تطبيق 7 قواعد جودة
- فصل السجلات الصالحة عن المرفوضة

#### 6️⃣ Load — التحميل
- حفظ `final_dataset.csv`
- حفظ `rejected_records.csv`
- تسجيل كل شيء في `logs/pipeline.log`

---

## ✅ 5. Data Quality Rules

| # | القاعدة | الشرط |
|---|---------|-------|
| 1 | student_id موجود | not NULL |
| 2 | student_id فريد | unique |
| 3 | العمر منطقي | 16 ≤ age ≤ 30 |
| 4 | GPA صحيح | 0 ≤ gpa ≤ 4 |
| 5 | الحضور صحيح | 0 ≤ attendance ≤ 100 |
| 6 | الدرجة صحيحة | 0 ≤ score ≤ 100 |
| 7 | المشاركة صحيحة | 0 ≤ participation_score ≤ 100 |

**السجلات الفاشلة** تُسجَّل في `rejected_records.csv` مع `error_reason`.

---

## 🛠️ 6. Installation

### المتطلبات الأساسية

- Python 3.10+
- PostgreSQL 14+
- MongoDB 6+

### الخطوات

```bash
# 1) استنسخ المشروع
git clone <repository>
cd student_data_pipeline

# 2) أنشئ بيئة افتراضية
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac

# 3) ثبّت المكتبات
pip install -r requirements.txt

# 4) أنشئ قاعدة PostgreSQL
psql -U postgres -c "CREATE DATABASE students_db;"
psql -U postgres -d students_db -f database/setup_postgres.sql

# 5) جهّز MongoDB
python data/raw/setup_mongodb.py

# 6) عدّل app/config.py بكلمة مرور PostgreSQL

🚀 7. Running
تشغيل Pipeline الكامل
bash

python main.py

تشغيل الاختبارات
bash

python -m unittest tests.test_pipeline -v

الناتج المتوقع
text

PIPELINE STARTED (5 Sources)
CSV Records          : 20
PostgreSQL Records   : 19
MongoDB Records      : 18
HTML Records         : 5
API Records          : 19
Integrated Records   : 20
Valid Records        : 16
Rejected Records     : 4
Processing Time      : 0.15 seconds

📤 8. Output
الملف	الوصف
data/processed/final_dataset.csv	Dataset نهائي (16 سجل × 22 عمود)
data/rejected/rejected_records.csv	السجلات المرفوضة (4 سجلات)
logs/pipeline.log	سجل كامل للتنفيذ
الأعمدة النهائية في final_dataset.csv:
المجموعة	الأعمدة
الأساسية	student_id, student_name, age, major, city
الأكاديمية	gpa, attendance, status, avg_score, total_credits, courses
الأنشطة	clubs, library_visits, participation_score, behavior, scholarship
التسجيل	registration_status, semester
المشتقة	performance_level, attendance_status, scholarship_status, engagement_level
🎓 9. Answers to Final Questions
1. لماذا نحتاج إلى Data Pipeline عند التعامل مع مصادر متعددة؟

لأن البيانات في الواقع موزعة على أنظمة مختلفة (قواعد بيانات، ملفات، APIs). بدون Pipeline:

    سيكون الجمع يدوياً وبطيئاً

    ستكون الأخطاء كثيرة

    لن تكون هناك ضمانة لجودة البيانات

    سيكون من المستحيل معالجة البيانات بشكل دوري

الـ Pipeline يؤتمت العملية بالكامل ويضمن الجودة.
2. ما الفرق بين Extract و Transform و Load؟
المرحلة	الوظيفة
Extract	جلب البيانات الخام من المصادر
Transform	تنظيف، تحويل، وإثراء البيانات
Load	حفظ البيانات النهائية في الوجهة
3. ما المشاكل التي واجهتها أثناء دمج البيانات؟

    أنواع مختلفة: student_id كـ string في CSV و integer في PostgreSQL

    قيم مفقودة: بعض الطلاب غير موجودين في كل المصادر

    تكرارات: طالب واحد موجود مرتين في CSV

    مسافات زائدة: Mona Ahmed في CSV

    حالات أحرف مختلفة: sanaa vs Sanaa

4. كيف تعاملت مع Missing Values؟

    student_id مفقود → حذف السجل

    gpa و attendance مفقودان → تعويض بالمتوسط

    age مفقود → لا يُعوَّض، يُرفض السجل لاحقاً في Validation

5. كيف تعاملت مع Duplicate Records؟

استخدمت df.drop_duplicates(subset=['student_id'], keep='first') — احتفظ بأول ظهور للسجل وأحذف الباقي، مع تسجيل عدد السجلات المحذوفة.
6. كيف تعاملت مع Invalid Records؟

    فصلها في rejected_records.csv

    تسجيل error_reason لكل سجل

    استمرار الـ Pipeline بدون توقف

7. لماذا يجب فصل Transformation عن Data Validation؟

    Transformation: تهدف لتوحيد البيانات وجعلها متسقة

    Validation: تهدف لضمان الجودة ورفض السجلات السيئة

الفصل يجعل الكود:

    أنظف

    أسهل للصيانة

    أسهل للاختبار

    قابلاً لإعادة الاستخدام

8. لماذا يعتبر Data Validation جزءاً أساسياً من هندسة البيانات؟

لأن "Garbage In = Garbage Out". بدون Validation:

    التحليلات ستكون خاطئة

    نماذج ML ستكون ضعيفة

    القرارات ستكون سيئة

Validation تضمن أن البيانات الداخلة للتحليل موثوقة.
9. كيف يمكن تطوير Pipeline ليعمل دورياً وألياً؟

باستخدام:

    Cron Jobs (Linux) / Task Scheduler (Windows)

    Apache Airflow أو Prefect للجداول المعقدة

    GitHub Actions للـ CI/CD

    Docker + Kubernetes للإنتاج

10. كيف يمكن جعل Pipeline يتعامل مع ملايين السجلات؟

    Chunking: معالجة البيانات على دفعات (chunksize في pandas)

    Distributed Processing: استخدام PySpark أو Dask

    Database Optimization: فهارس، Partitioning

    Streaming: استخدام Kafka للبيانات اللحظية

    Parallelism: معالجة المصادر بالتوازي

11. ما الفرق بين Streaming Processing و Batch Processing؟
المعيار	Batch	Streaming
التوقيت	دوري (ساعات/أيام)	لحظي
البيانات	ضخمة	مستمرة
التعقيد	أقل	أعلى
الأدوات	Airflow, Spark	Kafka, Flink
الاستخدام	التقارير اليومية	IoT, Fraud Detection
🏆 10. Excellence Features (Bonus)
الميزة	الحالة
Pipeline Metrics	✅ ملخص تنفيذي كامل
Multi-Source Integration	✅ 5 مصادر
Data Lineage	🔄 (يمكن إضافته)
Reusable Architecture	✅ كل مصدر في ملف منفصل
Error Handling	✅ try/except في كل مصدر
👨‍💻 Author

طالب هندسة البيانات
التكليف العملي الشامل — Multi-Source Data Integration Pipeline
📝 License

هذا المشروع لأغراض تعليمية