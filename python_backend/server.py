import sys
import flask
import mysql.connector

mysql_user = 'anonymous'
mysql_pwd  = 'PiWaC!23CyZzkAYYpi&2S'
mysql_host = 'mysql1'
mysql_db   = 'all_the_things'

mydb = mysql.connector.connect(user = mysql_user, password = mysql_pwd,
                              host = mysql_host,
                                    database = mysql_db)


mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM lonely_heroes")
myresult = mycursor.fetchall()

print("Hello python! This is {}".format(sys.argv[0]))
print("Listing lonely heroes:")
for i, name, copter in myresult:
    print("ID: {}, Name: {}, Ponycopter: {}".format(i, name, bool(copter)))

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
    print("Requested users")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM lonely_heroes")
    myresult = mycursor.fetchall()
    return flask.jsonify(myresult)

if __name__ == '__main__':
    # Note that flask by default listens to localhost / 127.0.0.1
    # that's not going to work with docker port forwarding - localhost addresses
    # are not allowed to escape the local network so they can't be forwarded out of
    # a docker network. 
    app.run(host="0.0.0.0") #debug=True)
    mydb.close()