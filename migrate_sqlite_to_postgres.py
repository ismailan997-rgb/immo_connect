import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()

from app import DATABASE_URL, get_db_connection, init_db


TABLES = ("users", "properties", "reviews")
SOURCE_QUERIES = {
    "users": "SELECT * FROM users ORDER BY id",
    "properties": """SELECT properties.* FROM properties
        JOIN users ON users.id = properties.user_id
        ORDER BY properties.id""",
    "reviews": """SELECT reviews.* FROM reviews
        JOIN properties ON properties.id = reviews.property_id
        ORDER BY reviews.id""",
}
ORPHAN_QUERIES = {
    "biens sans utilisateur": """SELECT properties.id FROM properties
        LEFT JOIN users ON users.id = properties.user_id
        WHERE users.id IS NULL ORDER BY properties.id""",
    "avis sans annonce": """SELECT reviews.id FROM reviews
        LEFT JOIN properties ON properties.id = reviews.property_id
        WHERE properties.id IS NULL ORDER BY reviews.id""",
}


def migrate():
    if not DATABASE_URL:
        raise RuntimeError("Configurez DATABASE_URL avant la migration.")
    if not os.path.exists("database.db"):
        raise FileNotFoundError("database.db est introuvable.")

    init_db()
    source = sqlite3.connect("database.db")
    source.row_factory = sqlite3.Row
    try:
        for label, query in ORPHAN_QUERIES.items():
            orphan_ids = [row[0] for row in source.execute(query).fetchall()]
            if orphan_ids:
                print(f"Attention : {len(orphan_ids)} {label} ignoré(s), IDs : {orphan_ids}.")

        with get_db_connection() as target:
            for table in TABLES:
                populated = target.execute(
                    f"SELECT EXISTS (SELECT 1 FROM {table}) AS populated"
                ).fetchone()["populated"]
                if populated:
                    raise RuntimeError(
                        f"La table PostgreSQL {table} n'est pas vide; migration annulée."
                    )

            for table in TABLES:
                rows = source.execute(SOURCE_QUERIES[table]).fetchall()
                if not rows:
                    continue
                columns = rows[0].keys()
                column_list = ", ".join(columns)
                placeholders = ", ".join("%s" for _ in columns)
                values = [tuple(row[column] for column in columns) for row in rows]
                with target.cursor() as cursor:
                    cursor.executemany(
                        f"INSERT INTO {table} ({column_list}) VALUES ({placeholders})",
                        values,
                    )

            for table in TABLES:
                target.execute(
                    f"""SELECT setval(
                        pg_get_serial_sequence('{table}', 'id'),
                        COALESCE(MAX(id), 1),
                        COUNT(*) > 0
                    ) FROM {table}"""
                )
    finally:
        source.close()

    print("Migration SQLite vers PostgreSQL terminée.")


if __name__ == "__main__":
    migrate()