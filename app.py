from resources.text_similarity import get_lines_text
from distutils.log import debug
from flask import Flask, jsonify, request
from flask_cors import CORS

from config import config

app = Flask(__name__)
CORS(app)

@app.route('/evaluation', methods=['POST'])
def list_values():
    text = request.json['text']
    try:
        guaranteed_analysis, has_taurine, ingredients = get_lines_text(text)
        result = {'Analisis': guaranteed_analysis, 'Taurina': has_taurine, 'Ingredientes': ingredients}
        return jsonify(result)
    except Exception as ex:
        return "Error"

if __name__=='__main__':
    app.config.from_object(config['production'])
    app.run()