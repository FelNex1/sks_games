import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=FELNEX\\SQLEXPRESS;"
    "DATABASE=SKS_Quest;"
    "Trusted_Connection=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    print("✅ Подключение к базе данных успешно!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sys.databases")
    print("\n📊 Список баз данных на сервере:")
    for row in cursor:
        print(f"   - {row[0]}")
    
    conn.close()
except Exception as e:
    print(f"❌ Ошибка: {e}")