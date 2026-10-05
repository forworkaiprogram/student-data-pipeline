"""Integration Module — دمج المصادر الخمسة على student_id."""
import pandas as pd
from app.utils.logger import logger


def integrate_data(
    csv_df: pd.DataFrame,
    postgres_df: pd.DataFrame,
    mongodb_df: pd.DataFrame,
    html_df: pd.DataFrame,
    api_df: pd.DataFrame,
) -> pd.DataFrame:
    logger.info("Integration started")

    merged = pd.merge(csv_df, postgres_df, on='student_id', how='left')
    logger.info(f"After CSV + PostgreSQL: {len(merged)}")

    if not mongodb_df.empty:
        merged = pd.merge(merged, mongodb_df, on='student_id', how='left')
        logger.info(f"After + MongoDB: {len(merged)}")

    if not api_df.empty:
        merged = pd.merge(merged, api_df, on='student_id', how='left')
        logger.info(f"After + API: {len(merged)}")

    logger.info(f"Integrated records: {len(merged)}")
    return merged