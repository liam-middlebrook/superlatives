# CSH Superlatives Main

from flask import Flask, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
import flask_migrate
import os
import sys
import pygal

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

import superlatives.models

if os.path.exists(os.path.join(os.getcwd(), "config.env.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

requests.packages.urllib3.disable_warnings()

auth = OIDCAuthentication(app,
                          issuer=app.config['OIDC_ISSUER'],
                          client_registration_info=app.config['OIDC_CLIENT_CONFIG'])
eboard = \
    [
        'ajgajg1134',
        'com6056',
        'faokryn',
        'henry',
        'jeid',
        'maxime',
        'mbillow',
        'rosehacker',
        'victoria'
    ]

rtps = \
    [
        'com6056',
        'dgonyeo',
        'ehouse',
        'jeid',
        'loothelion',
        'mbillow',
        'rbuzzell',
        'robgssp',
        'rossdylan',
        'slackwill'
    ]

questions = \
    [
        'Cutest Couple',
        'Most Technical',
        'Most Social',
        'Most Likely to Win Any Video Game Tournament',
        'Most Artistic',
        'Most CSH Spirit',
        'Most Likely to Launch a Million Dollar Startup',
        'Most Innocent',
        'Best Dancer',
        'Most Likely to Never Come Back After This Year',
        'Most Likely to Cause Downtime',
        'Most Repsonsive RTP',
        'Most Likely to Summon Angry Alumni',
        'Most Likely to be de-RTP\'d',
        'Most Likely to be Impeached',
        'Most Likely to Brighten Your Day',
        'Most Likely to Say Ridiculous Shit',
        'Most Likely to Take Over CSH in a Violent Coup de Grâce',
        'Most Wiki Contributions',
        'Most Predictable',
        'Least Predictable',
        'Most Changed Since Freshman Year',
        'Most Musical',
        'Most Likely to Survive in The L the Longest',
        'Most Likely to Go to Bed When Everbody Else is Waking Up',
        'Most Likely to be the Illuminate Puppetmaster',
        'Most Lit CSHer'
    ]
@app.route('/')
@auth.oidc_auth
def hi():
    return jsonify({'message':"hi"})

@app.route('/people')
@auth.oidc_auth
def list_people():
    people = [
                {
                    'name': m.name,
                    'id': m.id
                } for m in models.Person.query.all()]
    return jsonify({'people': people})

@app.route('/rtps')
@auth.oidc_auth
def list_rtps():
    people = [
                {
                    'name': m.name,
                    'id': m.id
                } for m in models.Person.query.filter(
                    models.Person.uid.in_(rtps))]
    return jsonify({'people': people})

@app.route('/eboard')
@auth.oidc_auth
def list_eboard():
    people = [
                {
                    'name': m.name,
                    'id': m.id
                } for m in models.Person.query.filter(
                    models.Person.uid.in_(eboard))]
    return jsonify({'people': people})


#   Accepts a json post
#
#   answers is an array of integers
#   associating people with IDs
#
@app.route('/submit', methods=['POST'])
@auth.oidc_auth
def submit():
    username = str(session['userinfo'].get('sub', ''))
    voted = True
    try:
        voted = models.Person.query.filter(
                    models.Person.uid == username
                ).first().voted
    except Exception:
        print("User not in superlatives db! " + username)

    if voted:
        return jsonify({'error': "already voted"})


    print(request.form)
    print(request.json)

    data = request.get_json()
    answers = data['answers']
    quote = data['quote']
    history = data['history']

    # Only vote once
    models.Person.query.filter(
        models.Person.uid == username).\
        update(
            {
                "quote": quote,
                "fav_history": history,
                "voted": True
            })

    db.session.add(models.SuperlativeVote(answers))
    db.session.flush()
    db.session.commit()

    return jsonify({'status': "ok"})

@app.route('/voted')
@auth.oidc_auth
def check_if_voted():
    username = str(session['userinfo'].get('sub', ''))
    voted = True
    try:
        voted = models.Person.query.filter(
                    models.Person.uid == username
                ).first().voted
    except Exception:
        print("User not in superlatives db!")
    return jsonify({'voted': voted})

@app.route('/stats')
@auth.oidc_auth
def display_stats_page():
    # display couples
    charts = []
    stats = get_stats()

    pie = pygal.Pie()
    pie.title = questions[0]
    # couples
    for couple, count in stats[0].items():
        c = couple.split(',')
        couple = ("%s, %s" % (getName(c[0]), getName(c[1])))
        pie.add(couple, count)
    charts.append(pie.render().decode('utf-8'))

    stats.pop(0)

    i = 1
    for stat in stats:
        pie = pygal.Pie()
        pie.title = questions[i]
        for person, count in stat.items():
            pie.add(getName(person), count)
        charts.append(pie.render().decode('utf-8'))
        i += 1

    table = ""

    html = """
        <html>
             <head>
                  <title>%s</title>
             </head>
              <body>
                <table>
                <tr>
                <th>
                    <td>Name</td>
                    <td>Quote</td>
                    <td>Favorite Moment in History</td>
                </th>
                </tr>
                 %s
                 </table>
                 %s
             </body>
        </html>
    """ % ("Superlatives", ''.join(getMoments()), ''.join(charts))
    return html

def getMoments():

    return [("""
    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
    </tr>
    """ % (p.name, p.quote, p.fav_history)) for p in models.Person.query.filter(
            models.Person.voted == True)]
def getName(id):

    return models.Person.query.filter(
            models.Person.id == id).first().name
def get_stats():

    submissions = [m for m in models.SuperlativeVote.query.all()]

    answers = []
    for s in submissions:
        answer = []
        for i in range(28):
            answer.append(s.__getitem__("superlative_" + str(i)))

        couple = [answer[0], answer[1]]
        couple.sort()
        answer.pop(0)
        answer.pop(0)
        answer.insert(0, ("%d,%d" % (couple[0], couple[1])))
        answers.append(answer)

    results = []
    for i in range(27):
        results.append({})

    for a in answers:
        i = 0
        for v in a:
            if v in results[i]:
                results[i][v] += 1
            else:
                results[i][v] = 1
            i += 1
    return results


@app.route("/logout")
@auth.oidc_logout
def logout():
    return redirect(url_for('index'), 302)
