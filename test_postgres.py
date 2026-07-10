import psycopg2

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        dbname="salary_db",
        user="postgres",
        password="postgres123",
    )

    print("Connexion OK")
    print(conn.get_dsn_parameters())

    conn.close()

except Exception as e:
    import traceback
    traceback.print_exc()