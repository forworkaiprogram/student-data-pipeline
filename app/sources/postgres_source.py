"""PostgreSQL Source — استخراج السجلات الأكاديمية."""
import pandas as pd
import psycopg2
from app.config import POSTGRES_CONFIG
from app.utils.logger import logger


def extract_postgres() -> pd.DataFrame:
    logger.info("PostgreSQL extraction started")
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        query = """
            SELECT 
                ar.student_id,
                ar.gpa,
                ar.attendance,
                ar.status,
                AVG(e.score) AS avg_score,
                SUM(c.credit_hours) AS total_credits,
                STRING_AGG(DISTINCT c.course_name, ', ') AS courses
            FROM academic_records ar
            LEFT JOIN enrollments e ON ar.student_id = e.student_id
            LEFT JOIN courses c ON e.course_id = c.course_id
            GROUP BY ar.student_id, ar.gpa, ar.attendance, ar.status
            ORDER BY ar.student_id
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        logger.info(f"PostgreSQL records: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"PostgreSQL extraction failed: {e}")
        return pd.DataFrame()