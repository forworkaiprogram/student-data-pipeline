# تنظيف النصوص، التكرارات، القيم المفقودة.
import re
import pandas as pd
from app.utils.logger import logger


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Cleaning text columns")
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        df[col] = df[col].astype(str)
        df[col] = df[col].apply(lambda x: re.sub(r'\s+', ' ', x).strip())
        if col in ['city', 'major', 'student_name', 'behavior', 'clubs']:
            df[col] = df[col].str.title()
    return df


def remove_duplicates(df: pd.DataFrame) -> tuple:
    before = len(df)
    df = df.drop_duplicates(subset=['student_id'], keep='first')
    removed = before - len(df)
    logger.info(f"Duplicate records removed: {removed}")
    return df, removed


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Handling missing values")
    df = df.dropna(subset=['student_id'])
    for col in ['age', 'gpa', 'attendance', 'score']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    for col in ['gpa', 'attendance']:
        if col in df.columns and df[col].isna().any():
            mean_val = df[col].mean()
            df[col] = df[col].fillna(round(mean_val, 2))
    return df