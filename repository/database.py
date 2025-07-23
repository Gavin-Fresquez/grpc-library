from mysql.connector import connect


def connect_db():
    try:
        db = connect(
            host='localhost',
            user='root',
            password='your_password',
            database='books'
        )
        return db
    except:
        return None


if __name__ == '__main__':
    if connect_db():
        print('connection success')

