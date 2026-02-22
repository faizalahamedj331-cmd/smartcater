import MySQLdb

# Connect to MySQL server (without database)
conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456')
cursor = conn.cursor()

# Drop and recreate database
cursor.execute('DROP DATABASE IF EXISTS smartcater')
cursor.execute('CREATE DATABASE smartcater CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')

conn.close()
print('Database recreated successfully!')
