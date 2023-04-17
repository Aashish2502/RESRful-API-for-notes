from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/notesDB'
# mongo = PyMongo(app)

def get_db():
    client = MongoClient(host='notesDB',
                         user='root',
                         password='pass',
                         authSource='Admin',
                        port=27017)
    db = client["notesDB"]
    return db



# Create note
@app.route('/notes', methods=['POST'])
def create_note():

    title = request.json['title']
    content = request.json['content']
    collection = get_db( ).notesDB
    collection.insert_one({'title': title, 'content': content})
    return jsonify({'title': title, 'content': content}) 

# Read all notes
@app.route('/notes', methods=['GET'])
def get_notes():
    notes = []
    collection = get_db( ).notesDB
    for note in collection.find():
        notes.append({'_id': str(note['_id']), 'title': note['title'], 'content': note['content']})
    return jsonify({'result': notes})

# Read a note by ID
@app.route('/notes/<note_id>', methods=['GET'])
def get_note_by_id(note_id):
    collection=get_db( ).notesDB
    note = collection.find_one({'_id': ObjectId(note_id)})
    if note:
        result = {'_id': str(note['_id']), 'title': note['title'], 'content': note['content']}
    else:
        result = 'Note not found'
    return jsonify({'result': result})

# Update a note by ID
@app.route('/notes/<note_id>', methods=['PUT'])
def update_note_by_id(note_id):
    title = request.json['title']
    content = request.json['content']
    collection = get_db( ).notesDB
    result = collection.update_one({'_id': ObjectId(note_id)}, {'$set': {'title': title, 'content': content}})
    if result.modified_count == 1:
        return jsonify({'result': 'Note updated'})
    else:
        return jsonify({'result': 'Note not found'})

# Delete a note by ID
@app.route('/notes/<note_id>', methods=['DELETE'])
def delete_note_by_id(note_id):
    collection=get_db( ).notesDB
    result = collection.delete_one({'_id': ObjectId(note_id)})
    if result.deleted_count == 1:
        return jsonify({'result': 'Note deleted'})
    else:
        return jsonify({'result': 'Note not found'})

if __name__ == '__main__':
    app.run(debug=True)
