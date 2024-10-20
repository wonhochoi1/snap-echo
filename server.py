from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb+srv://ishansheth31:Kevi5han1234@textstorage.saw2kxe.mongodb.net/textstorage?retryWrites=true&w=majority&tls=true')
# client = MongoClient('mongodb+srv://your_mongo_uri')
db = client['textstorage']  # Replace with your DB name
collection = db['test1']  # Collection name

@app.route('/getData', methods=['GET'])
def get_data():
    try:
        data = list(collection.find({}, {'_id': False}))  # Exclude _id from the result
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
