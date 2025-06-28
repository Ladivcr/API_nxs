import json
import psycopg2
from psycopg2.extras import execute_values

DB_URL = "<DB_URL>"


def load_json_data(path="models.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def populate_database(data):
    """Function to populate database"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    try:
        # 1. Obtener las marcas únicas
        brand_names = sorted(set(item["brand_name"] for item in data))
        # 2. Insertar marcas (evitar duplicados)
        execute_values(
            cur,
            """
            INSERT INTO brands (name)
            VALUES %s
            ON CONFLICT (name) DO NOTHING;
            """,
            [(name,) for name in brand_names],
        )

        # 3. Obtener el mapping brand_name → brand_id
        cur.execute("SELECT id, name FROM brands WHERE name = ANY(%s);", (brand_names,))
        brand_map = {name: id for id, name in cur.fetchall()}

        # 4. Preparar datos para insertar modelos
        model_values = [
            (
                item["id"],
                item["name"],
                item["average_price"],
                brand_map[item["brand_name"]],
            )
            for item in data
        ]

        execute_values(
            cur,
            """
        INSERT INTO models (id, name, average_price, brand_id)
        VALUES %s
        ON CONFLICT (name) DO NOTHING;
        """,
            model_values,
        )

        conn.commit()
        print("✅ Base de datos poblada correctamente.")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    data = load_json_data("models.json")
    populate_database(data)
