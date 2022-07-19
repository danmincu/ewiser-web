from flask import Flask, request, render_template

# from nltk_api.definition.response import DefinitionResponseBuilder
# from nltk_api.lemma.processor import POS
from werkzeug.exceptions import BadRequest

# from nltk_api.definition.processor import DefinitionProcessor
# from nltk_api.util.responses import BadRequestIncorrectPos
# from nltk_api.util.response_wrappers import json_response_with_time
from bin import annotate
from web.response_wrappers import json_response_with_time
from web.responses.response import ResponseBuilder

app = Flask(__name__)
processor = annotate

@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/definition/<string:word>')
@app.route('/definition/<string:word>/<string:pos>')
@json_response_with_time
def definitions(word, pos):

    use_similar = request.args.get('use_similar', None) is not None

    # -d cuda - c / home / danmincu / ewiser / res / downloaded / ewiser.semcor + wngt.pt / home / danmincu / ewiser / test.txt
    processor.test_run()

    return word


def assert_correct_format(candidate):
    if not isinstance(candidate, dict):
        raise TypeError('The value should ba dictionary.')
    if 'word' not in candidate or 'partOfSpeech' not in candidate:
        raise KeyError('Mandatory keys are missing. Expecting word and type keys.')


@app.route('/lemma', methods=['POST'])
@json_response_with_time
def lemmas():

    payload = request.get_json()
    for query in payload:
        try:
            assert_correct_format(query)
        except (TypeError, KeyError):
            return BadRequest("Incorrect format of query.")
    response = ResponseBuilder()
    response.add_entry("test", "hello")
    return response.build()


@app.route('/tagger', methods=['POST'])
@json_response_with_time
def tagger():
    payload = request.get_json()
    if not all(isinstance(entry, str) for entry in payload):
        return BadRequest("Incorrect format of entered data. Expects JSON array with strings.")
    remove_stops = request.args.get('remove_stops', None) is not None
    show_symbols = request.args.get('symbols', None) is not None

    response = ResponseBuilder()
    response.add_entry("test", "hello")
    return response.build()

@app.route('/doc/definition', methods=['GET'])
def doc_definition():
    return render_template('definition.html')


@app.route('/doc/lemmatization', methods=['GET'])
def doc_lemmatization():
    return render_template('lemma.html')


@app.route('/doc/tagger', methods=['GET'])
def doc_tagger():
    return render_template('tagger.html')


@app.route('/doc/similar', methods=['GET'])
def doc_similar():
    return render_template('similar.html')


@app.route('/credits', methods=['GET'])
def about():
    return render_template('about.html')
