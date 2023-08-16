from sqlite3 import Connection


def init_db(path="db.sqlite3"):
    sql = """
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        usertype VARCHAR (255) NOT NULL,
        username VARCHAR (255) UNIQUE NOT NULL,
        email VARCHAR (255) UNIQUE NOT NULL,
        password VARCHAR (255) NOT NULL
        );
    """
    connection = Connection(path)
    connection.execute(sql)
    connection.close()


if __name__ == "__main__":
    init_db()
