import bcrypt

def setup_function():
    #유저 생성
    # 여기서 중요한 점은 사용자 아이디를 자동으로 생성하게 하지말고 고정 값으로 정해주는 것이다. 그래야 실제 unit test함수에서 해당 사용자 아이디를 알 수 있다.
    #teardown_function을 통해 test 데이터를 전부 삭제해 준다. TRUNCATE SQL 구문은 해당 테이블의 데이터를 모두 삭제시켜 준다.
    #TURNCATE SQL 구문을 실행할 때 해당 테이블에 외부 키가 갈려있으면 테이블의 데이터를 삭제 할 수 없다. 그래서 임의로 SET FOREING_KEY_CHECK = 0 SQL구문을 실행해서 외부키를 잠시 비활성화 시킨다. 실제 서비스 중인 데이터베이스에서는 실행하면 안되는 SQL구문이다.
    #그리고 비활성화 되었던 외부키를 다시 활성화 한다.
    hashed_password = bcrypt.hashpw(b"1234", bcrypt.gensalt())
    new_user = {
        'id' : 1,
        'name' : "최강록",
        'email' :'timeiscoal@qwe.com',
        "profile" : 'test profile',
        'hashed_password' : hashed_password
    }
    database.execute(text("""
    INSERT INTO users(
        id,
        name,
        email,
        profile,
        hashed_password

    )VALUES(
        :id,
        :name,
        :email,
        :profile,
        :hashed_password
    )
    """), new_user)

    def teardown_function():
        database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        database.execute(text("TRUNCATE users"))
        database.execute(text('TRUNCATE tweets'))
        database.execute(text("TRUNCATE user_follow_list"))
        database.execute(text('SET FOREIGN_KEY_CHECKS=1'))

    def test_tweet(api):
        #로그인
        resp = api.post(
            '/login',
            data = json.dumps({'email':'timeiscoal@qwe.com', "password":"123"}),content_type = 'application/json'
        )
        resp_json = json.loads(resp.data.decode('UTF-8'))

        # 게시글
        resp = api.post(
            '/tweet',
            data = json.dump({'tweet':"첫 게시글"}),
            content_type = 'application/json',
            headers = {'Authorization' : access_token}
            
        )
        assert resp.status_code ==200

        # 게시글 확인
        resp = api.get(f'/timeline/{new_user_id}')
        tweets = json.loads(resp.data.decode('utf-8'))

        assert resp.status_code == 200
        assert tweets ==(
            'user_id':1,
            'timeline' : [{
                'user_id':1
                'tweet' : "첫 게시글"
            }]
        )

        #py test -p no:warning -vv -s