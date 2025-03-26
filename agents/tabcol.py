import pymysql
def databases(host, user, password, database):
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=database
        )
        cur = conn.cursor()
        cur.execute("SHOW TABLES") 
        tables = [table[0] for table in cur.fetchall()]

        schema = {}
        for table in tables:
            cur.execute(f"SHOW COLUMNS FROM {table}")
            columns = [column[0] for column in cur.fetchall()]
            schema[table] = columns
        return schema

    except pymysql.MySQLError as e:
        return f"Error: {e}"

    finally:
        if 'conn' in locals() and conn:
            conn.close()
