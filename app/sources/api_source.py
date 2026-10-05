"""REST API Source — استخراج بيانات التسجيل (Mock)."""
import pandas as pd
import requests
from app.config import API_URL, USE_MOCK_API
from app.utils.logger import logger


MOCK_API_DATA = [
    {"student_id": 1001, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1002, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1003, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1004, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1005, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1006, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1007, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1008, "registration_status": "Pending", "semester": "2024-Fall"},
    {"student_id": 1010, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1011, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1012, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1013, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1014, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1015, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1016, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1017, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1018, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1019, "registration_status": "Registered", "semester": "2024-Fall"},
    {"student_id": 1020, "registration_status": "Registered", "semester": "2024-Fall"},
]


def extract_api(api_url: str = API_URL, use_mock: bool = USE_MOCK_API) -> pd.DataFrame:
    logger.info("API extraction started")
    if use_mock or api_url is None:
        logger.info("Using mock API data")
        df = pd.DataFrame(MOCK_API_DATA)
    else:
        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            df = pd.DataFrame(response.json())
        except Exception as e:
            logger.error(f"API request failed: {e}")
            logger.info("Falling back to mock API data")
            df = pd.DataFrame(MOCK_API_DATA)
    logger.info(f"API records: {len(df)}")
    return df