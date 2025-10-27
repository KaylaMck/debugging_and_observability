import csv
import psycopg2


def load_with_psycopg(csv_path, logger):

    logger.info("Connecting to Postgres...")

    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="myuser",
            password="mypassword",
            port="5432",
        )

        cursor = conn.cursor()
        logger.info("Connected to Postgres.")

        cursor.execute("DELETE FROM persons")
        logger.info("Cleared existing data from 'persons' table.")

        with open(csv_path, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)
            row_count = len(rows)

            logger.info(f"Processing {row_count} rows")

            insert_query = """
                INSERT INTO persons (id, name, age, city)
                VALUES (%s, %s, %s, %s)
            """

            for row in rows:
                cursor.execute(
                    insert_query,
                    (int(row["id"]), row["name"], int(row["age"]), row["city"]),
                )

            conn.commit()

        logger.info("Finished loading data.")

    except Exception as e:
        logger.error(f"Error loading data: {e}")
        if conn:
            conn.rollback()
        raise

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
