import pymysql
import pandas as pd

def select_operation(query, host, user, password, database):
    try:
        con = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=database
        )
        cur = con.cursor()
        cur.execute(query)
        
        results = cur.fetchall()
        columns = [desc[0] for desc in cur.description] if cur.description else []

        if results and columns:
            df = pd.DataFrame(results, columns=columns)   
        else:
            df = pd.DataFrame({"Message": ["Query returned no results"]})   

        return df

    except pymysql.MySQLError as e:
        return pd.DataFrame({"Error": [str(e)]})   

    finally:
        if 'con' in locals() and con:
            con.close()
