import sqlite3
from datetime import datetime

# poner ruta de accseso en este caso esta en la misma carpeta donde esta la basde de datos
DB_PATH = 'Base_FortiFile.db'

def conectar_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def insertar_reporte(user_id, categoria_id, location_id, nombre, descripcion, status, fecha_incidente):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports (
            ID_USERS, ID_CATEGORIAS, ID_LOCATIONS,
            Name_Reports, Descripcion, status, incident_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, categoria_id, location_id, nombre, descripcion, status, fecha_incidente))

    conn.commit()
    conn.close()
    print("✅ Reporte insertado con éxito.")

def consultar_reportes():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            r.ID_REPORTS,
            u.Email           AS Usuario,
            c.Name            AS Categoría,
            l.Name_Locations  AS Ubicación,
            r.Name_Reports    AS Objeto,
            r.status,
            r.incident_date,
            DATETIME(r.created_at, '-5 hours') AS Fecha_Creación_Colombia
        FROM reports r
        JOIN Users u       ON r.ID_USERS = u.ID_USERS
        JOIN Categorias c  ON r.ID_CATEGORIAS = c.ID_CATEGORIAS
        JOIN locations l   ON r.ID_LOCATIONS = l.ID_LOCATIONS
        ORDER BY r.ID_REPORTS DESC
        LIMIT 10;
    """)

    resultados = cursor.fetchall()
    print("\n📋 Últimos 10 reportes:")
    for fila in resultados:
        print(fila)

    conn.close()

# Ejemplo de uso
if __name__ == "__main__":
    insertar_reporte(
        user_id=101,
        categoria_id=201,
        location_id=301,
        nombre="Portátil HP gris",
        descripcion="Laptop gris con calcomanías",
        status="perdido",
        fecha_incidente="2025-06-21"
    )

    consultar_reportes()
