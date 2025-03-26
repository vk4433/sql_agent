import pymysql

def cud_operation(query, host, user, password, database):
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=database
        )

        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        return "Update successfully"

    except pymysql.MySQLError as e:
        if 'conn' in locals() and conn.open:  
            conn.rollback()
        return f"Error: {e}"

    finally:
        if 'conn' in locals() and conn.open: 
            conn.close()
