# تشغيل ETL بـ 5 مصادر.
import time
from app.sources.csv_source import extract_csv
from app.sources.postgres_source import extract_postgres
from app.sources.mongodb_source import extract_mongodb
from app.sources.html_source import extract_html
from app.sources.api_source import extract_api
from app.transformation.cleaner import (
    clean_text_columns, remove_duplicates, handle_missing_values
)
from app.transformation.transformer import transform_data
from app.transformation.integration import integrate_data
from app.validation.quality import validate_data
from app.output.csv_writer import save_processed_data, save_rejected_data
from app.utils.logger import logger


def run_pipeline() -> None:
    start = time.time()
    logger.info("=" * 60)
    logger.info("PIPELINE STARTED (5 Sources)")
    logger.info("=" * 60)

    csv_data = extract_csv()
    postgres_data = extract_postgres()
    mongodb_data = extract_mongodb()
    html_data = extract_html()
    api_data = extract_api()

    if csv_data.empty:
        logger.error("CSV empty — aborting")
        return

    csv_data = clean_text_columns(csv_data)
    csv_data = handle_missing_values(csv_data)
    csv_data, duplicates = remove_duplicates(csv_data)

    integrated = integrate_data(
        csv_data, postgres_data, mongodb_data, html_data, api_data
    )
    transformed = transform_data(integrated)
    valid_df, rejected_df = validate_data(transformed)

    save_processed_data(valid_df)
    save_rejected_data(rejected_df)

    elapsed = round(time.time() - start, 2)
    logger.info("=" * 60)
    logger.info("PIPELINE EXECUTION SUMMARY")
    logger.info("=" * 60)
    logger.info(f"CSV Records          : {len(csv_data)}")
    logger.info(f"PostgreSQL Records   : {len(postgres_data)}")
    logger.info(f"MongoDB Records      : {len(mongodb_data)}")
    logger.info(f"HTML Records         : {len(html_data)}")
    logger.info(f"API Records          : {len(api_data)}")
    logger.info(f"Integrated Records   : {len(integrated)}")
    logger.info(f"Valid Records        : {len(valid_df)}")
    logger.info(f"Rejected Records     : {len(rejected_df)}")
    logger.info(f"Duplicate Records    : {duplicates}")
    logger.info(f"Processing Time      : {elapsed} seconds")
    logger.info("=" * 60)


if __name__ == "__main__":
    run_pipeline()