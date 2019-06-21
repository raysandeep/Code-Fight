from flask import Flask, render_template, request, jsonify

import os
import sys
import redis
from utility import utility, cron
from dotenv import load_dotenv
import requests
from requests.exceptions import HTTPError

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/say_name', methods=['POST'])
def say_name():
    token = "9d0c1b4ee351e3e9aadb462399e4e77434467180"
    json = request.get_json()
    org = json['first_name']
    org1 = json['last_name']
    print(org,org1)
    redis = None
    res = utility.leaderboard(token, org,redis)
    res1 = utility.leaderboard(token,org1,redis)
    scr = 0 
    scr1 = 0 
    for key in res:
        scr +=  res[key]
    for key in res1:
        scr1 +=  res1[key]
    word = org + " score is " + scr
    word1 = org1 + " score is " + scr1

    return jsonify(first_name=word, last_name=word1)

@app.route('/api/contribution', methods=['POST'])
def contribution():
    token = "9d0c1b4ee351e3e9aadb462399e4e77434467180"
    json = request.get_json()
    name = json['first_name']
    org = json['last_name']
    redis = None
    res = utility.leaderboard(token, org,redis)
    scr = 0
    scr1 =0
    print(res)
    for key in res:
        scr +=  res[key]
    
    for i in res:
        if name == i:
            scr1 = res[name]
            score = 0
            score = round((scr1/scr)*100,2)
        else :
            score = "check name properly" 

    return jsonify(first_name=name, last_name=score)

if __name__ == '__main__':
    app.run(debug=True)
    