"""HTML Source — Scraping لبيانات المقررات."""
import pandas as pd
from bs4 import BeautifulSoup
from app.config import HTML_FILE
from app.utils.logger import logger


def extract_html(file_path: str = HTML_FILE) -> pd.DataFrame:
    logger.info("HTML extraction started")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'lxml')
        table = soup.find('table', {'id': 'courses-table'})
        if not table:
            logger.error("HTML table not found")
            return pd.DataFrame()
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        rows = []
        for tr in table.find('tbody').find_all('tr'):
            cells = [td.get_text(strip=True) for td in tr.find_all('td')]
            if cells:
                rows.append(cells)
        df = pd.DataFrame(rows, columns=headers)
        logger.info(f"HTML records: {len(df)}")
        return df
    except FileNotFoundError:
        logger.error(f"HTML file not found: {file_path}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"HTML extraction failed: {e}")
        return pd.DataFrame()