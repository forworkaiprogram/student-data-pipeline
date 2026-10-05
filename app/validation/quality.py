#قواعد الجودة.
import pandas as pd
from app.config import QUALITY_RULES
from app.utils.logger import logger


def validate_record(row: pd.Series) -> list:
    errors = []

    if pd.isna(row.get('student_id')):
        errors.append("Missing student_id")

    age = row.get('age')
    if pd.isna(age):
        errors.append("Missing Age")
    elif not (QUALITY_RULES['age_min'] <= age <= QUALITY_RULES['age_max']):
        errors.append(f"Invalid Age: {age}")

    gpa = row.get('gpa')
    if pd.notna(gpa) and not (QUALITY_RULES['gpa_min'] <= gpa <= QUALITY_RULES['gpa_max']):
        errors.append(f"Invalid GPA: {gpa}")

    att = row.get('attendance')
    if pd.notna(att) and not (QUALITY_RULES['attendance_min'] <= att <= QUALITY_RULES['attendance_max']):
        errors.append(f"Invalid Attendance: {att}")

    score = row.get('avg_score')
    if pd.notna(score) and not (QUALITY_RULES['score_min'] <= score <= QUALITY_RULES['score_max']):
        errors.append(f"Invalid Score: {score}")

    part = row.get('participation_score')
    if pd.notna(part) and not (QUALITY_RULES['participation_min'] <= part <= QUALITY_RULES['participation_max']):
        errors.append(f"Invalid Participation: {part}")

    if pd.isna(gpa) and pd.isna(att):
        errors.append("Missing source data (PostgreSQL)")

    return errors


def validate_data(df: pd.DataFrame) -> tuple:
    logger.info("Validation started")
    errors_list = []
    valid_indices = []

    for idx, row in df.iterrows():
        errors = validate_record(row)
        if errors:
            errors_list.append({
                'student_id': row.get('student_id', 'N/A'),
                'error_reason': '; '.join(errors)
            })
        else:
            valid_indices.append(idx)

    valid_df = df.loc[valid_indices].copy()
    rejected_df = pd.DataFrame(errors_list)

    logger.info(f"Valid records: {len(valid_df)}")
    logger.info(f"Rejected records: {len(rejected_df)}")
    logger.info("Validation completed")
    return valid_df, rejected_df