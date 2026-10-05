"""Transformer Module — تحويل الأنواع وإضافة الأعمدة المشتقة."""
import pandas as pd
from app.utils.logger import logger


def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Converting data types")
    if 'student_id' in df.columns:
        df['student_id'] = pd.to_numeric(
            df['student_id'], errors='coerce'
        ).astype('Int64')
    for col in ['age', 'attendance', 'credit_hours', 'total_credits',
                'library_visits', 'participation_score']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].apply(
                lambda x: int(x) if pd.notna(x) else x
            ).astype('Int64')
    for col in ['gpa', 'avg_score']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').round(2)
    return df


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Adding derived columns")

    def get_performance(gpa):
        if pd.isna(gpa): return 'Unknown'
        if gpa >= 3.5: return 'Excellent'
        if gpa >= 3.0: return 'Very Good'
        if gpa >= 2.5: return 'Good'
        if gpa >= 2.0: return 'Acceptable'
        return 'At Risk'

    if 'gpa' in df.columns:
        df['performance_level'] = df['gpa'].apply(get_performance)

    if 'attendance' in df.columns:
        df['attendance_status'] = df['attendance'].apply(
            lambda x: 'Good' if pd.notna(x) and x >= 75 else 'Low'
        )

    if 'scholarship' in df.columns:
        df['scholarship_status'] = df['scholarship'].apply(
            lambda x: 'Yes' if x is True else 'No'
        )

    if 'participation_score' in df.columns:
        def get_engagement(score):
            if pd.isna(score): return 'Unknown'
            if score >= 85: return 'High'
            if score >= 60: return 'Medium'
            return 'Low'
        df['engagement_level'] = df['participation_score'].apply(get_engagement)

    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Transformation started")
    df = convert_data_types(df)
    df = add_derived_columns(df)
    logger.info("Transformation completed")
    return df