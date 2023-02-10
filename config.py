db = {

    'user' : "root",
    "password" : "1234",
    "host" : "localhost",
    "port" : 3306,
    "database" : "miniter"
 }

db_url = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{datebase}?charset=utf8"

test_db = {
    'user':"test",
    'password' :"password",
    'host' :'localhost',
    'prot':'3306',
    'database':'test_db'
}

test_config = {
    'DB_URL' : f"mysql+mysqlconnector://{test_db['user']}:{test_db['password']}@{test_db['host']}:{test_db['prot']}/{test_db['database']}?charset=UTF8"
}