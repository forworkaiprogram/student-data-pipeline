

# ---------- مسارات الملفات ----------
CSV_FILE = 'data/raw/students.csv'
HTML_FILE = 'data/raw/courses.html'
FINAL_OUTPUT = 'data/processed/final_dataset.csv'
REJECTED_OUTPUT = 'data/rejected/rejected_records.csv'
LOG_FILE = 'logs/pipeline.log'

# ---------- PostgreSQL ----------

POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'students_db',
    'user': 'postgres',
    'password': 'YOUR_PASSWORD_HERE',  # ← غيّر هذا
}

# ---------- MongoDB ----------
MONGODB_URI = 'mongodb://localhost:27017/'
MONGODB_DB = 'students_db'
MONGODB_COLLECTION = 'student_activities'

# ---------- REST API ----------
API_URL = None
USE_MOCK_API = True

# ---------- قواعد الجودة ----------
QUALITY_RULES = {
    'age_min': 16,
    'age_max': 30,
    'gpa_min': 0.0,
    'gpa_max': 4.0,
    'attendance_min': 0,
    'attendance_max': 100,
    'score_min': 0,
    'score_max': 100,
    'participation_min': 0,
    'participation_max': 100,
}