
# اختبارات شاملة Pipeline.
#تغطي 5 مصادر + قواعد الجودة + التكامل.


import unittest
import os
import pandas as pd

from app.sources.csv_source import extract_csv
from app.sources.postgres_source import extract_postgres
from app.sources.mongodb_source import extract_mongodb
from app.sources.html_source import extract_html
from app.sources.api_source import extract_api
from app.transformation.cleaner import remove_duplicates, handle_missing_values
from app.transformation.integration import integrate_data
from app.validation.quality import validate_data


class TestPipeline(unittest.TestCase):

    #  اختبارات المصادر الخمسة

    def test_01_csv_loaded(self):
        """Test 1: هل تم تحميل CSV؟"""
        df = extract_csv()
        self.assertFalse(df.empty, "CSV يجب أن يحتوي بيانات")
        self.assertIn('student_id', df.columns)
        self.assertIn('student_name', df.columns)
        print(f"\n   CSV rows: {len(df)}")

    def test_02_postgres_connection(self):
        """Test 2: هل تم الاتصال بـ PostgreSQL؟"""
        df = extract_postgres()
        self.assertFalse(df.empty, "PostgreSQL يجب أن يحتوي بيانات")
        self.assertIn('gpa', df.columns)
        self.assertIn('attendance', df.columns)
        print(f"\n   PostgreSQL rows: {len(df)}")

    def test_03_mongodb_connection(self):
        """Test 3: هل تم الاتصال بـ MongoDB؟"""
        df = extract_mongodb()
        self.assertFalse(df.empty, "MongoDB يجب أن يحتوي بيانات")
        self.assertIn('participation_score', df.columns)
        self.assertIn('clubs', df.columns)
        print(f"\n   MongoDB rows: {len(df)}")

    def test_04_html_scraping(self):
        """Test 4: هل تم استخراج بيانات HTML؟"""
        df = extract_html()
        self.assertFalse(df.empty, "HTML يجب أن يحتوي بيانات")
        self.assertIn('course_name', df.columns)
        print(f"\n   HTML rows: {len(df)}")

    def test_05_api_connection(self):
        """Test 5: هل تم الاتصال بالـ API؟"""
        df = extract_api(use_mock=True)
        self.assertFalse(df.empty, "API يجب أن يحتوي بيانات")
        self.assertIn('registration_status', df.columns)
        print(f"\n   API rows: {len(df)}")

    #  اختبارات Cleaner

    def test_06_duplicates_removed(self):
        """Test 6: هل تمت إزالة التكرارات؟"""
        df = pd.DataFrame({
            'student_id': [1, 1, 2, 3],
            'name': ['A', 'A', 'B', 'C']
        })
        cleaned, removed = remove_duplicates(df)
        self.assertEqual(len(cleaned), 3, "يجب أن يبقى 3 سجلات بعد إزالة التكرار")
        self.assertEqual(removed, 1, "يجب أن يُزال سجل واحد")
        print(f"\n   Removed: {removed} duplicate(s)")

    def test_07_missing_values(self):
        """Test 7: هل تمت معالجة Missing Values؟"""
        df = pd.DataFrame({
            'student_id': [1, 2, 3],
            'age': [20, None, 22],
            'gpa': [3.0, 3.5, None],
            'attendance': [90, 85, 95]
        })
        cleaned = handle_missing_values(df)
        self.assertFalse(cleaned['gpa'].isna().any(),
                         "gpa يجب أن يُعوّض بالمتوسط")
        self.assertFalse(cleaned['attendance'].isna().any(),
                         "attendance يجب أن يُعوّض بالمتوسط")
        print(f"\n   Missing values handled")

    #  اختبارات Validation

    def test_08_invalid_rejected(self):
        """Test 8: هل تم رفض البيانات غير الصالحة؟"""
        df = pd.DataFrame({
            'student_id': [1, 2, 3],
            'age': [20, 150, 22],
            'gpa': [3.0, 2.5, 5.0],
            'attendance': [90, 85, 95],
            'avg_score': [80, 75, 85],
            'participation_score': [80, 75, 85],
        })
        valid, rejected = validate_data(df)
        self.assertEqual(len(valid), 1, "يجب أن يبقى سجل واحد صالح")
        self.assertEqual(len(rejected), 2, "يجب رفض سجلين")
        print(f"\n   Valid: {len(valid)}, Rejected: {len(rejected)}")

   
    #  اختبار Integration
    

    def test_09_integration(self):
        """Test 9: هل تم دمج المصادر بنجاح؟"""
        csv_df = pd.DataFrame({
            'student_id': [1, 2],
            'name': ['A', 'B']
        })
        postgres_df = pd.DataFrame({
            'student_id': [1, 2],
            'gpa': [3.5, 2.8]
        })
        mongodb_df = pd.DataFrame({
            'student_id': [1, 2],
            'participation_score': [80, 90]
        })
        api_df = pd.DataFrame({
            'student_id': [1, 2],
            'registration_status': ['Registered', 'Registered']
        })
        html_df = pd.DataFrame()

        result = integrate_data(csv_df, postgres_df, mongodb_df, html_df, api_df)
        self.assertEqual(len(result), 2)
        self.assertIn('gpa', result.columns)
        self.assertIn('participation_score', result.columns)
        self.assertIn('registration_status', result.columns)
        print(f"\n   Integrated columns: {len(result.columns)}")

 

    def test_10_final_dataset_created(self):
        """Test 10: هل تم إنشاء final_dataset.csv؟"""
        from main import run_pipeline
        run_pipeline()
        self.assertTrue(
            os.path.exists('data/processed/final_dataset.csv'),
            "final_dataset.csv يجب أن يُنشأ"
        )
        self.assertTrue(
            os.path.exists('data/rejected/rejected_records.csv'),
            "rejected_records.csv يجب أن يُنشأ"
        )
        # تحقق  الملف غير فارغ
        df = pd.read_csv('data/processed/final_dataset.csv')
        self.assertGreater(len(df), 0, "final_dataset.csv يجب أن يحتوي بيانات")
        print(f"\n   Final dataset: {len(df)} rows, {len(df.columns)} columns")


if __name__ == '__main__':
    unittest.main(verbosity=2)