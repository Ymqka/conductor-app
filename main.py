from flask import Flask, request, jsonify, make_response, Response
from waitress import serve
import os
import jwt
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ["APP_JWT_SECRET"]

def token_required(a):
    @wraps(a)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        # token hard code is a bad thing, better would be to have a login method
        if not token:
            token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE1NTQ3NTU1NTUsImV4cCI6MjU1NDc1NTUwMCwiaWF0IjoxNTU0NzU1NTAwLCJqdGkiOiI5ZmRmMGE2Ni00YzllLTRlOTktODc4MC05YjdlOTNlMjFlMjciLCJ1c2VyX2lkIjoiMTA1YjM1MTgtNjQ2ZC00NjNlLWFkZGEtZDJiOTM5YzJkMDZkIiwidXNlcl9mdWxsX25hbWUiOiJCZXJ0cmFtIEdpbGZveWxlIiwidXNlcl9lbWFpbCI6Im51bGxAcGllZHBpcGVyLmNvbSJ9.-A8Gx18iTikKpedcxDlgcc7D8GMWFix0709Vfpbo1SI"
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        else:
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            except:
                return Response(
                    "bad token",
                    status=400,
                )

        current_user = jsonify({
            'user_id': data["user_id"],
            'user_full_name': data["user_full_name"],
            'user_email': data["user_email"]
        })

        return a(current_user, *args, **kwargs)

    return decorator


@app.route("/v1/user")
@token_required
def user(current_user):
    return current_user

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
