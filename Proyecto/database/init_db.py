# Inicializador de la base de datos SQLite

import sqlite3

def create_tables():
    conn = sqlite3.connect("database/fortifile.db")
    cursor = conn.cursor()
    # TODO: Crear tablas de usuario y archivos
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
