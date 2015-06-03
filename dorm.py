from flask import Flask, render_template, abort, url_for, request, g
import os
from flask.ext.sqlalchemy import SQLAlchemy
from collections import namedtuple
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'entries.db')
db = SQLAlchemy(app)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dorm = db.Column(db.String(30))
    text = db.Column(db.Text)

    def __init__(self, dorm, text):
        self.dorm = dorm
        self.text = text

    def __repr__(self):
        return '<Dorm: %r> %r' % self.dorm, self.text

class Dorm(object):
    def __init__(self, name, image, subtitle):
        self.name = name
        self.image = image
        self.subtitle = subtitle

# dorms is a dictionary mapping the url-friendly name to a Dorm object
dorms = {"rieber": Dorm("Rieber Court", 'img/rieber.jpg', 'subtitle text'),
         "hedrick": Dorm("Hedrick Court", 'img/hedrick.jpg', 'subtitle text'),
         "sproul": Dorm("Sproul Court", 'img/sproul.jpg', 'subtitle text'),
         "hitchsuites": Dorm("Hitch Suites", 'img/hitchsuites.jpg', 'subtitle text'),
         "dykstrahall": Dorm("Dykstra Hall", 'img/dykstrahall.jpg', 'subtitle text'),
         "deneve": Dorm("De Neve Plaza", 'img/deneve.jpg', 'subtitle text'),
         "deltapoint": Dorm("Delta Terrace & Canyon Point", 'img/deltapoint.jpg', 'subtitle text'),
         "courtside" : Dorm("Courtside", 'img/courtside.jpg', 'subtitle text') 
         }


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/<dorm>/')
def dorm_page(dorm):
    # check to see if this is an invalid dorm name
    if dorm not in dorms:
        abort(404)
    # if not, get data from the database somehow
    # data = get_data_from_database(dorm)
    # then send the Dorm tuple and the associated data to the template
    return render_template('dorm.html', dorm=dorms[dorm], data=None)


@app.errorhandler(404)
def error(e):
    # return render_template('404.html'), 404
    return "404 page not found"  # for now


# make the dorms variable available to all templates without having
# to specifically send it
@app.context_processor
def inject_dorms():
    return dict(dorms=dorms)


# actually run Flask
if __name__ == '__main__':
    app.run()
