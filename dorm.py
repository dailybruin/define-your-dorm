from flask import Flask, render_template, abort, url_for, request
from collections import namedtuple
app = Flask(__name__)

# I'm basically defining Dorm as a 'struct' with two fields, name and image
# in Python, it's a namedtuple
Dorm = namedtuple('Dorm', 'name image')
# dorms is a dictionary mapping the url-friendly name to a Dorm object
dorms = {"rieberterrace": Dorm("Rieber Terrace", 'img/rieberterrace.jpg'),
         "riebervista": Dorm("Rieber Vista", 'img/riebervista.jpg'),
         "rieberhall": Dorm("Rieber Hall", 'img/rieberhall.jpg'),
         "hedrickhall": Dorm("Hedrick Hall", 'img/hedrickhall.jpg'),
         "hedricksummit": Dorm("Hedrick Summit", 'img/hedricksummit.jpg'),
         "sproulhall": Dorm("Sproul Hall", 'img/sproulhall.jpg'),
         "sproulcove": Dorm("Sproul Cove", 'img/sproulcove.jpg'),
         "sproullanding": Dorm("Sproul Landing", 'img/sproullanding.jpg'),
         "hitchsuites": Dorm("Hitch Suites", 'img/hitchsuites.jpg'),
         "dykstrahall": Dorm("Dykstra Hall", 'img/dykstrahall.jpg'),
         "deneve": Dorm("De Neve Plaza", 'img/deneve.jpg')
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
