import logging
from logging.handlers import RotatingFileHandler
import os
from db_psycopg import load_with_psycopg # pylint: disable=import-error

def setup_logger():

    logger = logging.getLogger('data_pipeline')
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    os.makedirs('logs', exist_ok=True)

    file_handler = RotatingFileHandler(
        'logs/data_pipeline.log',
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()

def main():
    logger.info("Starting data pipeline...")

    try:
        csv_path = 'data/sample.csv'
        load_with_psycopg(csv_path, logger)
        logger.info("Pipeline finished.")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()