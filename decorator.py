from functools import wraps
import jwt
from flask import request, Response

# 인자 값으로 들어오는 f 는 데코레이터가 적용되는 함수이다.
# wraps 데코를 반드시 적어줄 필요는 없지만 여러 이슈들을 해결해준다.
# decorator 함수이다. 데코 함수를 리턴해 줘야 하므로 nested 함수로 지정해준다. 함수의 인자가 arg, kwarge로 되어 있는 이유는 여러 다양한 함수에 적용 될 수 있으므로 모든 형태의 인자를 받을 수 있어야 한다. 그래서 다음과 같은 인자값을 설정해준것이다.
def test_decorator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("데코 함수")
        return f(*args,**kwargs)

    return decorated_function

@test_decorator
def func():
    print("함수 실행하기")



# 인증 데코 함수

def login_required(f):
    @wraps 
    def decorated_function(*args,**kwargs):
        # 전송된 HTTP 요청에서 'authorization' 헤더 값을 읽어 엑세스 토큰을 얻음
        access_token = request.headers.get('Authorization')
        # authoriztion 헤더가 전송 되었다면 복호화해서 payload Json을 읽는다.
        # None이면 인증허가를 하지 않는다.
        if access_token is not None:
            try:
                # 복호화해서 payload json을 읽는 것 뿐만 아니라 해당 토큰이 해당 백엔드 API 서버에서 생성된 토큰인지도 함께 확인한다.
                #이를 위해서는 해당 JWT signature 부분을 암호화 할때 사용한 시크릿 키가 필요하다 여기서 config에서 시크릿 키 필드 값을 읽는다.
                payload = jwt.decode(access_token, current_app.config["JWT_SECRET_KEY"],'HS256')
                # 복호화 과정에서 문제가 발생시
            except jwt.InvalidTokenError:
                payload = None
            
                # 그래서 페이로드가 none이면 401 Unauthorized 응답
            if payload is None: return Response(status=401)

            #jwt에서 복호화한 payload json에서 user_id를 읽어 해당 사용자의 아이디를 사용해서 데이터베이스에서 사용자 정보를 읽는다.
            #get_user_info 함수는 주어진 사용자 아이디를 바탕으로 데이터베이스에서 사용자 정보를 읽어들이는 함수이다.
            user_id = payload['user_id']
            g.user_id = user_id
            g.user = get_user_info(user_id) if user_id else None

        else:
            return Response(status=401)
        

        return f(*args,**kwargs)
    return decorated_function