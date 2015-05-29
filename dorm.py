from flask import Flask, render_template, abort, url_for, request
app = Flask(__name__)

dorms = ["rieberterrace", "riebervista", "rieberhall", "hedrickhall",
         "hedricksummit", "sproulhall", "sproulcove", "sproullanding",
         "hitchsuites", "dykstrahall", "deneve"]

@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/<dorm>/')
def dorm_page(dorm):
    if dorm not in dorms:
        abort(404)
    #data = get_data_from_database(dorm)
    #return render_template('dorm.html', dorm=dorm, data=data)




@app.errorhandler(404)
def error(e):
    #return render_template('404.html'), 404
    return "404 page not found" # for now

if __name__ == '__main__':
    app.run()
