from flask import Flask, jsonify, make_response, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from nanoid import generate

# Configuration
app = Flask(__name__)
# app.secret_key = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)
port = 4545
baseURL = f'http://localhost:{port}'


db = SQLAlchemy(app)

# Model Definition


class Shorturl(db.Model):
    __tablename__ = "shorturl"

    id = db.Column('id', db.String, primary_key=True)
    originalURL = db.Column('originalURL', db.String)

    def __init__(self, id, originalURL):
        self.id = id
        self.originalURL = originalURL

# Routing


@app.route('/')
def index():
    d = {
        'url_list': [
            {
                'url': '/info',
                'method': 'GET',
                'params': '',
                'body': '',
                'desc': 'Shows all data from database'
            },
            {
                'url': '/shortenurl',
                'method': 'POST',
                'params': '',
                'body': '{url: "YOUR_STRING_URL"}',
                'desc': 'Generates new short url from original url'
            },
            {
                'url': '/go/:id',
                'method': 'GET',
                'params': ':id => the shorten url id',
                'body': '',
                'desc': 'Access your ORIGINAL Url and redirect to the page'
            }
        ]
    }
    return make_response(jsonify(d), 200)


@app.route('/info')
def info():
    allData = Shorturl.query.all()
    response = []
    for data in allData:
        response.append({
            "originalURL": data.originalURL,
            "shortURL": f"{baseURL}/go/{data.id}",
        })
    return make_response(jsonify(response), 200)


@app.route('/shortenurl', methods=['POST'])
def shortenurl():
    if request.method == "POST":
        req = request.json

        if req == None or not 'url' in req:
            return make_response(jsonify({'message': 'BAD-REQUEST'}), 400)

        url = req['url']
        newID = generate(size=10)

        new_shorturl = Shorturl(newID, url)

        db.session.add(new_shorturl)
        db.session.commit()

        return make_response(jsonify({
            "originalURL": url,
            "shortURL": f"{baseURL}/go/{newID}"
        }), 200)
    return make_response(jsonify({'message': 'NOT-FOUND'}), 404)


@app.route('/go/<id>')
def go(id):
    found_data = Shorturl.query.filter_by(id=id).first()
    if found_data:
        return redirect(found_data.originalURL, code=302)

    return make_response(jsonify({'message': 'NOT-FOUND'}), 404)


if __name__ == "__main__":
    db.create_all()
    app.run(port=port, debug=True)
