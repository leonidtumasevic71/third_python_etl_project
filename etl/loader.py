import pandas as pd
import logging
from sqlalchemy import text
from config import load_dotenv, engine
from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger(__name__)

def csv_loader(file_name: str) -> pd.DataFrame:
    path = Path(r'C:\Users\111\Desktop\third\data') / file_name

    if not path.exists():
        logger.error(f"file {file_name} was not found, path: {path}")
        raise FileNotFoundError (f"file {file_name} was not found, path: {path}")

    if not path.is_file():
        logger.error(f"object {file_name} is not a file, path: {path}")
        raise ValueError (f"object {file_name} is not a file, path: {path}")

    if path.suffix != ".csv":
        logger.error(f"file {file_name} has different extension")
        raise ValueError (f"file {file_name} has different extension")

    if path.stat().st_size == 0:
        logger.error(f"the file {file_name} is empty")
        raise ValueError (f"the file {file_name} is empty")

    try:
        df = pd.read_csv(path)
        logger.info(f"file {file_name} was successfully loaded")
        return df
    except Exception as e:
        logger.error(f"file write error {file_name}: {e}")
        raise RuntimeError(f"file write error {file_name}: {e}")

def uploader(df: pd.DataFrame, table_name: str) -> None:
    if df.empty:
        logger.error(f"empty DataFrame")
        raise ValueError (f"empty DataFrame")

    try:
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
    except SQLAlchemyError:
        logger.error(f"no database connection")
        raise

    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        logger.info(f"{len(df)} rows were loaded into {table_name}")
    except SQLAlchemyError as e:
        logger.error(f"file write error: {e}")
        raise

def required_columns_validator(df: pd.DataFrame, required_columns: set[str]) -> None :
    missing = required_columns - set(df.columns)

    if missing:
        raise KeyError(
            f"Missing columns: {missing}"
        )
