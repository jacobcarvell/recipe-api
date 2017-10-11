from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from json import dumps

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
api = Api(app)

def scrapeTaste(url):
    try:
        res = requests.get(url)
    except requests.exceptions.RequestException as e:
        return 0

    html = res.content
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('h1').get_text()
    img = soup.select_one('figure.lead-image-block img[src]')['src']
    ingredients = []
    for i in soup.select('section.recipe-ingredients-section div.ingredient-description'):
        ingredients.append(i.text)

    method = []
    for i in soup.select('section.recipe-method-section div.recipe-method-step-content'):
        method.append(i.text)

    data = {
        url: {
            'title': title,
            'image': img,
            'ingredients': ingredients,
            'method': method
        }
    }

    return data

class scrapeRecipe(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('url', type=str, help='This is the url for the website')
            args = parser.parse_args()

            _userURL = args['url']
            print(args['url'])

            if not args['url']:
                return {'error': 'No url supplied'}
            else:
                res = scrapeTaste(args['url'])
                if res == 0:
                    return {'error': 'No valid url supplied'}
                else:
                    return {'status': 'success', 'data': res}
        except Exception as e:
            return {'error': str(e)}

api.add_resource(scrapeRecipe, '/addrecipe')

if __name__ == '__main__':
    app.run(debug=True)

# scrapeTaste('http://www.taste.com.au/recipes/moroccan-chicken-bowl/QR30rnEH')
