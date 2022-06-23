from flask import Flask, jsonify
import flask

from es import ESKNN

app = Flask(__name__)

# Check the index
esknn = ESKNN()
result = esknn.create_index()
INDEX_FLAG = False
if result == 1:
    INDEX_FLAG = True
elif result == 2:
    INDEX_FLAG = True
else:
    print('main.py -> Something went wrong with create index.')


@app.route('/', methods=['GET'])
def home():
    return 'Hello World!'

# Insert a new document route
@app.route('/api/insert_document')
def insert_document():
    data = flask.request.json
    
    esknn.insert_document(data)

    return jsonify(
        {
            "status": 200
        }
    )


# Search documents route
@app.route('/api/search_document')
def search_document():
    data = flask.request.json
    
    field_name = data['field_name']
    query = data['query']

    result = esknn.search_document(query, field_name)

    documents = []

    hits = result['hits']['hits']

    for hit in hits:
        documents.append(hit['_source'])

    return {
        "status": 200,
        "documents": documents
    }
