import config
from sqlalchemy import create_engine ,text
from app import create_app


# 터미널에 pytest

def testcode_to(num):
    return  2 + num

def test_testcode_to():
    assert testcode_to(2) == 4


@pytest.fixture
def api():
    app= create_app(config.test_config)
    app.config['TEST'] = True
    api = app.test_client()

    return api


def test_tweet(api):
    # 사용자 생성
    new_user = {
        'email' : 'timeiscoal@qwe.com',
        'password' : '123',
        'name' : '이름',
        'profile' : 'test profile'

    }
    resp =  api.post(
        '/sign=up',
        data = json.dumps(new_user),
        content_type = 'application/json'
    )
    assert resp.status_code == 200

    
    resp_json = json.loads(resp.data.decoce('UTF-8'))
    new_user_id = resp_json['id']

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