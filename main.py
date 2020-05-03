from flask import Flask, request, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

GAMES = {}

@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        data = request.get_json()
        gameid = data["gameid"]
        maxplayers = int(data["maxplayers"])
        words = ["________", "________", "________", "________", "________", "________", "________", "________", ]
        GAMES[gameid] = {'maxplayers': maxplayers, 'players': 1, 'whoseturn': 0, 'words': []}
        return jsonify({'success': True})
    else: return jsonify({'success': False})

@app.route('/join', methods=['POST'])
def join():
    if request.method == 'POST':
        data = request.get_json()
        gameid = data["gameid"]
        if GAMES.get(gameid) != None:
            currentplayers = GAMES[gameid]['players']
            maxplayers = GAMES[gameid]['maxplayers']
            if (currentplayers < maxplayers):
                currentplayers = currentplayers + 1
                GAMES[gameid]['players'] = currentplayers

                if (currentplayers == maxplayers):
                    GAMES[gameid]['whoseturn'] = 1

                return jsonify({'success': True, 'player': currentplayers})

            
            else:
                print("Here 1")
                return jsonify({'success': False})
        
        else:
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
        whoseturn = GAMES[gameid]['whoseturn']
        sentwords = GAMES[gameid]['words']
        return jsonify({'turn': whoseturn, 'words': sentwords})

@app.route('/sendWords', methods=['POST'])
def setdata():
    if request.method == 'POST':
        data = request.get_json()
        gameid = data["gameid"]
        words = GAMES[gameid]['words']
        turn = GAMES[gameid]['whoseturn']
        index1 = (turn - 1) * 2
        index2 = index1 + 1
        word1 = data["word1"]
        word2 = data["word2"]
        words[index1] = word1
        words[index2] = word2
        GAMES[gameid]['words'] = words
        GAMES[whoseturn] = turn + 1
        return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)