from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import redis
import json

rclient = redis.StrictRedis(host="localhost", port=6379, db=0)
app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        data = request.get_json()
        gameid = data["gameid"]
        rclient.set(gameid, b"None")
        maxplayers = int(data["maxplayers"])
        words = ["________", "________", "________", "________", "________", "________", "________", "________", ]
        gamedata = {'maxplayers': maxplayers, 'players': 1, 'whoseturn': 0, 'words': words}
        gamedata = json.dumps(gamedata)
        rclient.set(gameid, gamedata)
        return jsonify({'success': True})
    else: return jsonify({'success': False})

@app.route('/join', methods=['POST'])
def join():
    if request.method == 'POST':
        data = request.get_json()
        gameid = data["gameid"]
        try:
            gamedata = rclient.get(gameid)
            gamedata = gamedata.decode("utf-8")
            gamedata = json.loads(gamedata)
            currentplayers = gamedata['players']
            maxplayers = gamedata['maxplayers']
            if (currentplayers < maxplayers):
                currentplayers = currentplayers + 1
                gamedata['players'] = currentplayers

                if (currentplayers == maxplayers):
                    gamedata['whoseturn'] = 1

                gamedata = json.dumps(gamedata)
                rclient.set(gameid, gamedata)
                return jsonify({'success': True, 'player': currentplayers})

            
            else:
                print("Here 1")
                return jsonify({'success': False})
        
        except:
            print("Here 2")
            return jsonify({'success': False})
       
    else:
        print("Here 3") 
        return jsonify({'success': False})

@app.route('/getGameInfo', methods=['POST'])
def getinfo():
    if request.method == 'POST':
        data = request.get_json()
        gameid = data["gameid"]
        gamedata = rclient.get(gameid)
        gamedata = gamedata.decode("utf-8")
        gamedata = json.loads(gamedata)
        whoseturn = gamedata['whoseturn']
        sentwords = gamedata['words']
        return jsonify({'turn': whoseturn, 'words': sentwords})

@app.route('/sendWords', methods=['POST'])
def setdata():
    if request.method == 'POST':
        data = request.get_json()
        gameid = data["gameid"]
        gamedata = rclient.get(gameid)
        gamedata = gamedata.decode("utf-8")
        gamedata = json.loads(gamedata)
        words = gamedata['words']
        turn = gamedata['whoseturn']
        index1 = (turn - 1) * 2
        index2 = index1 + 1
        word1 = data["word1"]
        word2 = data["word2"]
        words[index1] = word1
        words[index2] = word2
        gamedata['words'] = words
        gamedata['whoseturn'] = turn + 1
        gamedata = json.dumps(gamedata)
        rclient.set(gameid, gamedata)
        return jsonify({'success': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
