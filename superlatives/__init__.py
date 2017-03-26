#i CSH Superlatives Main

from flask import Flask, jsonify, request, session, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
import flask_migrate
import requests
import os
import sys
import pygal
import json
import sys

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
        'joshgm',
        'jmf',
        'zach',
        'mbillow',
        'jhollander',
        'meghan'
    ]

rtps = \
    [
        'ehouse',
        'com6056',
        'dgonyeo',
        'loothelion',
        'mbillow',
        'jmf',
        'smirabito'
    ]

admin_users = \
    [
        "kailey",
        "loothelion",
        "rosehacker"
    ]

# types
# rtp
# eboard
# double
# default
questions = \
    [
        {
            'name': 'Most likely to win any video game tournament',
            'type': 'default'
        },
        {
            'name': 'Most responsive RTP',
            'type': 'rtp'
        },
        {
            'name': 'Cutest Couple',
            'type': 'double'
        },
        {
            'name': 'Most likely to cause downtime',
            'type': 'rtp'
        },
        {
            'name': 'Most likely to be impeached',
            'type': 'eboard'
        },
        {
            'name': 'Most likely to brighten your day',
            'type': 'default'
        },
        {
            'name': 'Most artistic',
            'type': 'default'
        },
        {
            'name': 'Most musical',
            'type': 'default'
        },
        {
            'name': 'Most innocent',
            'type': 'default'
        },
        {
            'name': 'Most changed since freshmen year',
            'type': 'default'
        },
        {
            'name': 'Most likely to be the Illuminati puppet master',
            'type': 'default'
        },
        {
            'name': 'Most likely to survive in the L the longest',
            'type': 'default'
        },
        {
            'name': 'Most CSH spirit',
            'type': 'default'
        },
        {
            'name': 'Most unpredictable',
            'type': 'default'
        },
        {
            'name': 'Most likely to say ridiculous shit',
            'type': 'default'
        },
        {
            'name': 'Most likely to summon angry alumni',
            'type': 'rtp'
        },
        {
            'name': 'Best dancer',
            'type': 'default'
        },
        {
            'name': 'Most social',
            'type': 'default'
        },
        {
            'name': 'Most technical',
            'type': 'default'
        },
        {
            'name': 'Most likely to wake you up at 2AM',
            'type': 'default'
        },
        {
            'name': 'Most likely to be your future boss',
            'type': 'default'
        },
        {
            'name': 'Best to bring home to mom and dad',
            'type': 'default'
        },
        {
            'name': 'Life of the party',
            'type': 'default'
        },
        {
            'name': 'Most likely to say the wrong thing on a tour',
            'type': 'default'
        },
        {
            'name': 'Most likely to bring up a constitutional amendment',
            'type': 'default'
        },
        {
            'name': 'Best on floor chef',
            'type': 'default'
        },
        {
            'name': 'Best style',
            'type': 'double'
        },
        {
            'name': 'Most likely to do more after 2AM than most people do all day',
            'type': 'default'
        }
    ]
@app.route('/')
@auth.oidc_auth
def hi():
    return render_template("index.html")

@app.route('/questions')
@auth.oidc_auth
def list_questions():
    return jsonify(questions)

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
    username = str(session['userinfo'].get('preferred_username', ''))
    voted = True
    try:
        voted = models.Person.query.filter(
                    models.Person.uid == username
                ).first().voted
    except Exception:
        print("User not in superlatives db! " + username, file=stderr)

    if voted:
        return jsonify({'error': "already voted"})


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
    username = str(session['userinfo'].get('preferred_username', ''))
    voted = True
    try:
        voted = models.Person.query.filter(
                    models.Person.uid == username
                ).first().voted
    except Exception:
        print("User not in superlatives db! " + username, file=stderr)
    return jsonify({'voted': voted})

@app.route('/stats')
@auth.oidc_auth
def display_stats_page():
    username = str(session['userinfo'].get('preferred_username', ''))
    if not username in admin_users:
        return jsonify({'access': False})
    # display couples
    charts = []
    stats = get_stats()


    i = 0
    print(stats, file=sys.stderr)
    for stat in stats:
        if questions[i]['type'] == "double":
            # couple
            pie = pygal.Pie()
            pie.title = questions[i]['name']
            for couple, count in stats[i].items():
                c = couple.split(',')
                couple = ("%s, %s" % (getName(c[0]), getName(c[1])))
                pie.add(couple, count)
            charts.append(pie.render().decode('utf-8'))
        else:
            pie = pygal.Pie()
            pie.title = questions[i]['name']
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
            models.Person.id == int(id)).first().name
def get_stats():

    submissions = [m for m in models.SuperlativeVote.query.all()]

    answers = []
    for s in submissions:
        answer = json.loads(s.data)
        print(answer, file=sys.stderr)
        i = 0
        for q in questions:
            if q['type'] == "double":
                # double
                couple = [answer[i], answer[i+1]]
                couple.sort()

                answer.pop(i)
                answer.pop(i)
                answer.insert(i, couple[0] + "," + couple[1])
            i += 1
        print(answer, file=sys.stderr)
        answers.append(answer)

    results = []
    for i in range(len(questions)):
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
