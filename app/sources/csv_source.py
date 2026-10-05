#CSV Source — استخراج بيانات الطلاب من ملف CSV.
import pandas as pd
from app.config import CSV_FILE
from app.utils.logger import logger


def extract_csv(file_path: str = CSV_FILE) -> pd.DataFrame:
    logger.info("CSV extraction started")
    try:
        df = pd.read_csv(file_path)
        logger.info(f"CSV records: {len(df)}")
        return df
    except FileNotFoundError:
        logger.error(f"CSV file not found: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        return pd.DataFrame()