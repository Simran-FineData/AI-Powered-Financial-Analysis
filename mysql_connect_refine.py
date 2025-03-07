import pymysql
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="glintler_refine_finance",
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )
# Function to execute queries with auto-reconnect
def execute_query(query,params=[]):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query,params)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except pymysql.err.OperationalError:
        print("Reconnecting to MySQL...")
        return execute_query(query)  # Retry the query

