"""MongoDB Source — استخراج الأنشطة الطلابية."""
import pandas as pd
from pymongo import MongoClient
from app.config import MONGODB_URI, MONGODB_DB, MONGODB_COLLECTION
from app.utils.logger import logger


def extract_mongodb() -> pd.DataFrame:
    logger.info("MongoDB extraction started")
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        db = client[MONGODB_DB]
        collection = db[MONGODB_COLLECTION]
        documents = list(collection.find({}, {'_id': 0}))
        df = pd.DataFrame(documents)
        client.close()
        if not df.empty and 'clubs' in df.columns:
            df['clubs'] = df['clubs'].apply(
                lambda x: ', '.join(x) if isinstance(x, list) else str(x)
            )
        logger.info(f"MongoDB records: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"MongoDB extraction failed: {e}")
        return pd.DataFrame()