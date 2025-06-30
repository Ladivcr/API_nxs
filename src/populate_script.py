import json
import psycopg2
from psycopg2.extras import execute_values
import time

DB_URL = "postgresql://toor:toor@db:5432/toor"
# Usese en caso de levantar el proyecto en Modo Local
# "postgresql://toor:toor@localhost:5432/toor"


def create_tables():
    """
    Crea las tablas 'brands' y 'models' en la base de datos.
    Se conecta a la DB_URL y ejecuta las sentencias SQL para crear las tablas.
    """
    conn = None
    cur = None
    max_retries = 10
    retry_delay = 5  # seconds

    for i in range(max_retries):
        try:
            print(
                f"Intentando conectar a la base de datos para crear tablas (Intento {i+1}/{max_retries})..."
            )
            conn = psycopg2.connect(DB_URL)
            cur = conn.cursor()

            # SQL para crear la tabla brands
            create_brands_table_sql = """
            CREATE TABLE IF NOT EXISTS brands (
                id SERIAL PRIMARY KEY,
                name VARCHAR(30) UNIQUE NOT NULL
            );
            """

            # SQL para crear la tabla models
            create_models_table_sql = """
            CREATE TABLE IF NOT EXISTS models (
                id SERIAL PRIMARY KEY,
                name VARCHAR(70) UNIQUE NOT NULL,
                average_price DECIMAL(10,2),
                brand_id INTEGER,
                CONSTRAINT fk_brand FOREIGN KEY (brand_id) REFERENCES brands(id)
            );
            """

            # Ejecutar las sentencias SQL
            cur.execute(create_brands_table_sql)
            cur.execute(create_models_table_sql)

            # Confirmar los cambios
            conn.commit()
            print("✅ Tablas 'brands' y 'models' creadas/verificadas correctamente.")
            break  # Salir del bucle si la conexión y creación son exitosas

        except psycopg2.OperationalError as e:
            print(f"Error de conexión a la base de datos: {e}")
            print(f"Reintentando en {retry_delay} segundos...")
            time.sleep(retry_delay)
            if i == max_retries - 1:
                print("❌ Fallo al conectar y crear tablas después de varios reintentos.")
                raise  # Re-lanzar la excepción si se agotan los reintentos
        except Exception as e:
            if conn:
                conn.rollback()  # Revertir cualquier cambio en caso de error
            print(f"Error al crear tablas: {e}")
            raise  # Re-lanzar la excepción para que el programa se detenga
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


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
    create_tables()
    data = load_json_data("models.json")
    populate_database(data)
