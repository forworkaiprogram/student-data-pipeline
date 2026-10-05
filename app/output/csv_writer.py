"""CSV Writer — حفظ المخرجات النهائية."""
import os
import pandas as pd
from app.config import FINAL_OUTPUT, REJECTED_OUTPUT
from app.utils.logger import logger


def save_processed_data(df: pd.DataFrame, path: str = FINAL_OUTPUT) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8-sig')
    logger.info(f"Final dataset saved: {path} ({len(df)} records)")


def save_rejected_data(df: pd.DataFrame, path: str = REJECTED_OUTPUT) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if df.empty:
        df = pd.DataFrame(columns=['student_id', 'error_reason'])
    df.to_csv(path, index=False, encoding='utf-8-sig')
    logger.info(f"Rejected records saved: {path} ({len(df)} records)")