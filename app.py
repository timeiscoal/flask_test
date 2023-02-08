from flask import Flask , request, jsonify
from flask.json import JSONEncoder

class CustomJSONEndocer(JSONEncoder):
    def default(self, obj):
        if isinstance(obj,set):
            return list(obj)
        
        return JSONEncoder.default(self,obj)

app = Flask(__name__)
app.users = {}
app.id_count = 1

@app.route("/ping", methods=(["GET"]))
def ping():
    return "pong"


@app.route("/sign-up", methods=(["POST"]))
def sign_up():
    new_user = request.json
    print(new_user)
    new_user["id"] = app.id_count
    app.users[app.id_count] = new_user
    app.id_count = app.id_count+1

    return jsonify(new_user)


app.tweets=[]

@app.route("/tweet", methods=["POST"])
def tweet():
    payload = request.json
    user_id = int(payload["id"])
    tweet = payload["tweet"]

    if user_id not in app.users:
        return "not users"
    elif len(tweet) > 30:
        return "text length limit is 30"

    user_id = int(payload["id"])
    app.tweets.append({
        "user_id":user_id,
        "tweet":tweet
        })
    return "" , 200

app.json_encoder = CustomJSONEndocer



@app.route("/follow", methods=["POST"])
def follow():
    payload = request.json
    user_id = int(payload["id"])
    user_id_to_follow = int(payload["follow"])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자를 찾을 수 없습니다."
    user = app.users[user_id]
    print("테스트1 :", user)
    user.setdefault("follow", set()).add(user_id_to_follow)
    print("테스트2:",user.setdefault("follow",set()))

    return jsonify(user)

@app.route("/unfollow",methods=["POST"])
def unfollow():
    payload = request.json
    user_id = int(payload["id"])
    user_id_to_follow = int(payload["unfollow"])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return "사용자를 찾을 수 없습니다." ,400

    user = app.users[user_id]
    user.setdefault("follow", set()).discard(user_id_to_follow)
    return jsonify(user)


@app.route("/timeline/<int:user_id>", methods=["GET"])
def timeline(user_id):
    if user_id not in app.users:
        return "사용자를 찾을 수 없습니다.",400

    follow_list = app.users[user_id].get("follow",set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]

    return jsonify({
        "user_id":user_id,
        "timeline": timeline
    })