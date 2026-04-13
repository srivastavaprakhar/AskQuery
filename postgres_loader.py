import os
import psycopg2
from dotenv import load_dotenv
from llama_index.core.schema import Document

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


# 🔥 GET FOREIGN KEYS (PostgreSQL)
def get_foreign_keys_pg(cursor, table_name):
    cursor.execute("""
        SELECT
            kcu.column_name,
            ccu.table_name AS foreign_table,
            ccu.column_name AS foreign_column
        FROM information_schema.key_column_usage kcu
        JOIN information_schema.constraint_column_usage ccu
        ON ccu.constraint_name = kcu.constraint_name
        WHERE kcu.table_name = %s
    """, (table_name,))
    
    return cursor.fetchall()


# 🚀 MAIN FUNCTION
def get_postgres_data():
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    # ✅ Get all public tables
    cursor.execute("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema='public';
    """)
    tables = [row[0] for row in cursor.fetchall()]

    documents = []

    for table in tables:
        try:
            # 🔹 Fetch base table data
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]

            # 🔥 Get foreign keys
            foreign_keys = get_foreign_keys_pg(cursor, table)

            for row in rows:
                row_data = dict(zip(col_names, row))
                field_lines = []

                # ✅ Base fields
                for col in col_names:
                    val = row_data.get(col)
                    if val is not None and str(val).strip():
                        field_lines.append(f"{col.replace('_', ' ').capitalize()}: {val}")

                # 🔥 FK RESOLUTION (same logic as your SQLite version)
                for from_col, ref_table, to_col in foreign_keys:
                    fk_val = row_data.get(from_col)

                    if fk_val:
                        try:
                            cursor.execute(
                                f"SELECT * FROM {ref_table} WHERE {to_col} = %s",
                                (fk_val,)
                            )
                            join_row = cursor.fetchone()

                            if join_row:
                                join_col_names = [desc[0] for desc in cursor.description]
                                join_data = dict(zip(join_col_names, join_row))

                                # 👉 only include first 2 useful fields
                                for jcol, jval in list(join_data.items())[:2]:
                                    if jval:
                                        field_lines.append(
                                            f"{jcol.replace('_', ' ').capitalize()} (from {ref_table}): {jval}"
                                        )

                        except Exception as e:
                            print(f"[!] FK join failed for {table}: {e}")

                # 🧠 RAG-FRIENDLY TEXT
                doc_text = f"Record from {table} table:\n" + "\n".join(field_lines)

                documents.append(
                    Document(
                        text=doc_text,
                        metadata={"table": table}
                    )
                )

        except Exception as e:
            print(f"[!] Error reading table '{table}': {e}")
            continue

    connection.close()
    return documents