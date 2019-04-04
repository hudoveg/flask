from db import connect_database, init_database

conn = connect_database('admin', 'postgres', '127.0.0.1', '5432', 'flask_api')
init_database(conn)