# CSH Superlatives Main

from database import init_db

from flask import Flask, jsonify, request
import json
import sys
import pygal

json_config = None

app = Flask(__name__)

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
def hi():
    return jsonify({'message':"hi"})

@app.route('/people')
def list_people():
    import models
    people = [
                {
                    'name': m.name,
                    'id': m.id
                } for m in models.Person.query.all()]
    return jsonify({'people': people})

@app.route('/rtps')
def list_rtps():
    import models
    people = [
                {
                    'name': m.name,
                    'id': m.id
                } for m in models.Person.query.filter(
                    models.Person.uid.in_(rtps))]
    return jsonify({'people': people})

@app.route('/eboard')
def list_eboard():
    import models
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
def submit():
    import models

    from database import db_session
    #ensure webauth user hasn't already submitted
    username = request.headers.get('x-webauth-user')
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

    db_session.add(models.SuperlativeVote(answers))
    db_session.flush()
    db_session.commit()

    return jsonify({'status': "ok"})

@app.route('/voted')
def check_if_voted():
    import models
    #ensure webauth user hasn't already submitted
    username = request.headers.get('x-webauth-user')
    voted = True
    try:
        voted = models.Person.query.filter(
                    models.Person.uid == username
                ).first().voted
    except Exception:
        print("User not in superlatives db!")
    return jsonify({'voted': voted})

@app.route('/stats')
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

    html = """
        <html>
             <head>
                  <title>%s</title>
             </head>
              <body>
                 %s
             </body>
        </html>
    """ % ("Superlatives", ''.join(charts))
    return html

def getName(id):
    import models

    return models.Person.query.filter(
            models.Person.id == id).first().name
def get_stats():
    import models

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

with open(sys.argv[1]) as config_file:
    json_config = json.load(config_file)

    init_db(json_config['db']['url'])

    app.run(**json_config['flask'])
