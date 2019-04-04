import psycopg2


def connect_database(user='admin', password='postgres', host='127.0.0.1', port='5432', database='flask_api'):
    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
    return connection


def init_database(connection):
    try:
        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE notes
                  (id     SERIAL PRIMARY KEY     NOT NULL,
                  title   TEXT   NOT NULL,
                  body    TEXT); '''

        cursor.execute(create_table_query)

        create_table_query = '''CREATE TABLE users
                          (id         SERIAL   PRIMARY KEY   NOT NULL,
                          username    TEXT     UNIQUE        NOT NULL,
                          password    TEXT); '''

        cursor.execute(create_table_query)
        connection.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        return False


def get_all(connection):
    try:
        cursor = connection.cursor()
        postgres_select_query = "SELECT * FROM notes"
        cursor.execute(postgres_select_query)
        keys = ['id', 'title', 'body']
        note_list = []
        for row in cursor.fetchall():
            note_list.append(dict(zip(keys, row)))

        return note_list
    except (Exception, psycopg2.Error) as error:
        return False


def get_note(connection, nid):
    try:
        cursor = connection.cursor()
        postgres_select_query = "SELECT * FROM notes WHERE id = %s"
        cursor.execute(postgres_select_query, [nid])
        keys = ['id', 'title', 'body']
        for row in cursor.fetchall():
            return dict(zip(keys, row))
    except (Exception, psycopg2.Error) as error:
        return str(error)
        return False


def add_note(connection, note):
    try:
        cursor = connection.cursor()
        postgres_insert_query = " INSERT INTO notes (title, body) VALUES (%s,%s)"
        values = (note['title'], note['body'])
        cursor.execute(postgres_insert_query, values)
        connection.commit()
        return True
    except (Exception, psycopg2.Error) as error:
        return False


def update_note(connection, nid, note):
    try:
        set_string = "SET "
        params = tuple(note.values())
        tmp = [];
        for item in note.items():
            if item[0] == "title":
                tmp.append("title = %s")
            if item[0] == "body":
                tmp.append("body = %s")
        set_string += ", ".join(tmp)
        params += (nid,)
        postgres_update_query = "UPDATE notes " + set_string + " WHERE id = %s"
        cursor = connection.cursor()
        cursor.execute(postgres_update_query, params)
        connection.commit()

        note = get_note(connection, nid)
        return note
    except (Exception, psycopg2.Error) as error:
        return str(error)
        return False


def del_note(connection, nid):
    try:
        cursor = connection.cursor()
        postgres_delete_query = "DELETE FROM notes WHERE id = %s"
        cursor.execute(postgres_delete_query, (nid,))
        connection.commit()
        return True
    except (Exception, psycopg2.Error) as error:
        return False


def add_user(connection, user):
    try:
        cursor = connection.cursor()
        postgres_insert_query = " INSERT INTO users (username, password) VALUES (%s,%s)"
        values = (user['username'], user['password'])
        cursor.execute(postgres_insert_query, values)
        connection.commit()
        return True
    except (Exception, psycopg2.Error) as error:
        return False


def get_user_by_username(connection, username):
    try:
        cursor = connection.cursor()
        postgres_select_query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(postgres_select_query, [username])
        keys = ['id', 'username', 'password']
        for row in cursor.fetchall():
            return dict(zip(keys, row))
    except (Exception, psycopg2.Error) as error:
        return str(error)
        return False
