from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)

class Albums(Resource):
    #methods
    pass

class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict()
        return {'data' : data}, 200
    #methods
    pass

api.add_resource(Albums, '/albums')
api.add_resource(Users, '/users') #users is entry point

@app.route('/album_name/<string:album>/<string:artist>')
def album_name(album: str, artist: str):
    score = getInfo(getAlbumUrl(album, artist))
    return jsonify(message="Album: " + album + ". Artist: " + artist + ". Score: " + score)


#Scrapes score from a pitchfork album review
def getInfo(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="site-content")
    for element in results:
        score = element.find(class_="score-box")
        break
    score = score.find(class_="score")
    elist = []
    for element in results:
        elist.append(element)
    return score.text.strip()

def getAlbumUrl(album, artist):
    qartist = artist.replace(" ", "%20").lower().replace('\'', "%27")
    qalbum = album.replace(" ", "%20").lower().replace('\'', "%27")
    rartist = artist.replace(" ", "-").lower().replace('\'', "")
    ralbum = album.replace(" ", "-").lower().replace('\'', "")
    searchurl = 'https://pitchfork.com/search/?query=' + qalbum #+ "%20" + qartist
    page = requests.get(searchurl)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all('a')
    album_link = ""
    for link in soup.find_all('a'):
        if ralbum in link.get('href'):
            album_link = link.get('href')
            temp = "https://pitchfork.com" + album_link
            if verifyUrl(temp, rartist):
                break
    return "https://pitchfork.com" + album_link

def verifyUrl(url, artist):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="site-content")
    results = str(results)
    if artist in results:
        return True
    return False

if __name__ == '__main__':
    app.run()




