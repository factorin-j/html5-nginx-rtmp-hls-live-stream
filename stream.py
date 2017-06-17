from flask import Flask, request, render_template, send_from_directory
import sqlite3
import status

app = Flask(__name__)

hostname = 'localhost:8888'


@app.route('/')
def index():
    return 'OK'


@app.route('/auth')
def auth():
    if request.args.get('name') is None or request.args.get('swfurl') is None:
        return 'Malformed request', status.HTTP_400_BAD_REQUEST

    username = request.args.get('name')
    idhash = request.args.get('swfurl').split("?")[-1]

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND id_hash=?", (username, idhash))

    if len(cur.fetchall()) == 0:
        return 'Incorrect credentials', status.HTTP_401_UNAUTHORIZED

    return 'OK', status.HTTP_200_OK


@app.route('/dist/<path:path>')
def serve_js(path):
    return send_from_directory('dist', path)


@app.route('/watch/<username>')
def serve_player(username):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    if len(cur.fetchall()) == 0:
        return "No such user!"
    else:
        return render_template('player.html', username=username, hostname=hostname)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889, debug=True)
