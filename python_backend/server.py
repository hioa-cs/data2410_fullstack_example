import sys
import flask
import mysql.connector

# For Google OAuth token verification
from google.oauth2 import id_token as goog_token
from google.auth.transport import requests as goog_req

# Config.
# TODO: Place this in a config file
mysql_user = 'anonymous'
mysql_pwd  = 'PiWaC!23CyZzkAYYpi&2S'
mysql_host = 'mysql1'
mysql_db   = 'all_the_things'
#NOTE: Replace oauth_id with your own client ID
oauth_id   = '42.apps.googleusercontent.com'

mydb = mysql.connector.connect(user = mysql_user, password = mysql_pwd,
                               host = mysql_host,
                               database = mysql_db)


mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM lonely_heroes")
myresult = mycursor.fetchall()

print("Hello python! This is {}".format(sys.argv[0]))
print("Listing lonely heroes:")
for i, name, email, copter, access, img in myresult:
    print("ID: {}, Name: {}, Email: {}, Ponycopter: {} Access: {} Img: {}"
        .format(i, name, email, bool(copter), access, img))

#mydb.close()

# The API
app = flask.Flask(__name__, static_folder="/var/fullstack/frontend", static_url_path="")

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def serve_page(path):
    print("Request received for {}".format(path))
    return flask.send_from_directory('/var/fullstack/frontend', path)

@app.route('/api/users/', methods=['GET'])
def get_users():
    if flask.request.method == 'GET':
        print("Requested users")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM lonely_heroes")
        myresult = mycursor.fetchall()

        auth_token = flask.request.headers.get("Authorization")
        if (auth_token):
            print("AUTHENTICATION ATTEMPT. Token: {}".format(auth_token))
            valid_user = validate_token(auth_token)

            if not valid_user:
                return flask.jsonify([])

            print("{} is a valid Google user".format(valid_user['given_name']))
            auth_email = valid_user['email']

            # If the logged in user is registered and has a high access level
            # add more secrets
            access = 0
            for id, name, email, pony, acc, img  in myresult:
                if email == auth_email:
                    print("{} is a registered user in this app, access level {}"
                        .format(name, acc))
                    access = acc

            if (access >= 100):
                morph_img = "https://www.denofgeek.com/wp-content/uploads/2020/08/the-matrix-4-morpheus.jpg?resize=768%2C432"
                myresult.insert(0, (43, "Morpheus",None, True, 100, morph_img))

            smith_img = "https://consequence.net/wp-content/uploads/2020/01/agent-smith-matrix-e1579642927212.jpg?quality=50"
            myresult.insert(0, (42, "Agent Smith The Dangerous",None, True, 99, smith_img))

        return flask.jsonify(myresult)


def validate_token(token):
    some_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY5ZWQ1N2Y0MjQ0OTEyODJhMTgwMjBmZDU4NTk1NGI3MGJiNDVhZTAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiMTk5MTgxNjM0NTkyLW04YmVuaTUzM2Y5ZThhYWJmZWRwZ2ZlZzc3dWhraTk1LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTk5MTgxNjM0NTkyLW04YmVuaTUzM2Y5ZThhYWJmZWRwZ2ZlZzc3dWhraTk1LmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA2MDA0Mzg5OTc5NzEzNjc5ODc1IiwiZW1haWwiOiJkZXJlay5iaXBhcnRpc2FuQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiejN6dW5vUUtDcGlDS2xrUHdmVjhrUSIsIm5hbWUiOiJEZXJlayBCaXBhcnRpc2FuIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FBVFhBSnlvdGZfSy01S0c2cFg4emZDX05JblI4OGpBbUE0V3ZSYXRUR1c3PXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkRlcmVrIiwiZmFtaWx5X25hbWUiOiJCaXBhcnRpc2FuIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2MjAyOTUzNzQsImV4cCI6MTYyMDI5ODk3NCwianRpIjoiYmNlYmE0M2FkM2RlZTFhNjlmYjgwOTIxZGI4ZWJjNGY0ZGU3YzQxMCJ9.EyOWk8Sph7mawEy5HTSvCgQNWObVp6DmJEMp1fWgmcH6m4q6YNf2Ubge7M_dwP2zp39XoWPrgRQXs2hceFKVlhKnhvGVeVaxS4e-0C9hnQFfKUDTOFMjY-hgBd0UoP9N8cUIcK1MiLgatkRiajX9Rykdf2QSAxXQd0LkD1AAueoCyrwJsDyLnogzlBnvtCc_hN8r9_TLC7v-XBrZPeW3pOrsrmGzQkCnDCtTYg7TtFv-1r5p6OK74DB3x-BqRFVyp7u_9d-zxoG__8sq2WnocutwieXUSf7q1NNWGSzcba0SmOHpg35u5dqWFhGirZRRhTvHlI5D2lqGl1ctR7XWOA"
    if (token == some_token):
        print("Token is re-used. OK.")
        return True
    else:
        print("Never seen this token before...")

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = goog_token.verify_oauth2_token(token, goog_req.Request(), oauth_id)
        print("\nTOKEN VALID. User: {}\nUser data: \n{}\n"
            .format(idinfo['given_name'],idinfo))
        return idinfo

    except ValueError as err:
        # Invalid token
        print(f"Token validation failed: {err}")

    return False

if __name__ == '__main__':
    # Note that flask by default listens to localhost / 127.0.0.1
    # that's not going to work with docker port forwarding - localhost addresses
    # are not allowed to escape the local network so they can't be forwarded out of
    # a docker network.
    app.run(host="0.0.0.0") #debug=True)
    mydb.close()