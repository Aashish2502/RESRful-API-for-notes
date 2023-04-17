db = db.getSiblingDB("notesDB")
db.notesDB.drop() 

db.notesDB.insertMany([{
    "title": "Test123",
    "content": "Lorem Ipsum"
},
{   "title": "Test_123",
    "content": "Lorem Ipsum"}
])