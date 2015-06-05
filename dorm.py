from flask import Flask, render_template, abort, url_for, request, g, redirect, flash
from badwords import isBadWord
import os
import random
import itertools
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from collections import namedtuple, Counter
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'entries.db')
db = SQLAlchemy(app)

# Class for an entry in the database


class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    dorm = db.Column(db.String(50))
    username = db.Column(db.String(50))
    community_adjective = db.Column(db.String(50))
    learned_thing_noun = db.Column(db.String(50))
    people_adjective = db.Column(db.String(50))
    greatest_part = db.Column(db.String(50))
    dining_noun = db.Column(db.String(50))
    one_word = db.Column(db.String(50))

    def __init__(self, dorm, data):
        self.dorm = dorm
        for key in data:
            setattr(self, key, data[key])
        if self.username == "":
            self.username = "Anonymous"

    def __repr__(self):
        return str([self.community_adjective, self.learned_thing_noun, self.people_adjective, self.greatest_part, self.dining_noun, self.one_word])

    def vals(self):
        return [self.community_adjective, self.learned_thing_noun, self.people_adjective, self.greatest_part, self.dining_noun, self.one_word]


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
         "courtside": Dorm("Courtside", 'img/courtside.jpg', 'subtitle text')
         }


# Finds the most common words in a dorm's dataset
# Runs in O(n logn) time but it's the best we can do without persisting
# frequency data to disk
def find_most_common(data):
    words = Counter()
    for entry in data:
        words.update(entry.vals())
    most_common = words.most_common(10)
    if len(most_common) == 0:
        return most_common
    maxval = most_common[0][1]
    minval = most_common[-1][1]
    if maxval == minval:
        minval = 0.0
    result = []
    for entry in most_common:
        fontsize = max(
            15.0, 35.0 * (float(entry[1]) - minval) / (maxval - minval))
        result.append((entry[0], fontsize))
    random.shuffle(result)
    return result


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/<dorm>/')
@app.route('/<dorm>/<int:id>')
def dorm_page(dorm, id=None):
    # Check to see if this is an invalid dorm name
    if dorm not in dorms:
        abort(404)
    # If not, get data from the database
    data = Entry.query.filter_by(dorm=dorm)
    # If an id has been provided, fetch the entry with that id and send it
    current_record = None if id == None else Entry.query.filter_by(
        id=id).first()
    # Find the most common words
    most_common = find_most_common(data.all())
    # random.shuffle(most_common)
    # Only send 5 random entries to the template itself
    data = data.order_by(func.random()).limit(5).all()
    # Then send the Dorm tuple and the associated data to the template
    return render_template('dorm.html', url=dorm, dorm=dorms[dorm], data=data, most_common=most_common, current_record=current_record)


# Route for processing the form data
@app.route('/<dorm>/submit', methods=['POST'])
def store_entry(dorm):
    if len(request.form) != 7:  # something's fishy...make them try again
        flash("Something was wrong with your submission. Please try again!")
        return redirect(url_for('dorm_page', dorm=dorm, _anchor='Dorm'))
    for field in request.form.values():
        for word in field.split():
            if isBadWord(word):
                flash("Looks like our filters didn't accept your message. Please try again!")
                return redirect(url_for('dorm_page', dorm=dorm, _anchor='Dorm'))
    e = Entry(dorm, request.form)
    db.session.add(e)
    db.session.commit()
    return redirect(url_for('dorm_page', dorm=dorm, id=e.id, _anchor='Dorm'))


# @app.errorhandler(404)
# def error(e):
#     # Return render_template('404.html'), 404
#     return "404 page not found"  # for now


# Make the dorms variable available to all templates without having
# to specifically send it
@app.context_processor
def inject_dorms():
    return dict(dorms=dorms)


# actually run Flask
if __name__ == '__main__':
    app.secret_key = "KcjKwI35Gee6eJYbkX9l"
    app.run()
