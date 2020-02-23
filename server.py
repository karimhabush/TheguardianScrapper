from flask import Flask, escape, request
import pymongo

app = Flask(__name__)

MONGO_URI = 'mongodb+srv://theguardian:8uLoM1p8xrlWKJvn@tgcluster-gjmtx.mongodb.net/test?retryWrites=true&w=majority'
connection = pymongo.MongoClient(MONGO_URI)
db = connection['Theguardian']

@app.route('/articles')
def articles():
    page = request.args.get("page", "1")
    page_size = 5
    skips = page_size * (int(page) - 1 )
    result = str(list(db.articles.find().limit(page_size).skip(skips)))
    return result

@app.route('/search/content')
def search_content():
	query = request.args.get("query","")
	query = query.replace(" ","|")
	result = str(list(db.articles.find({"content" : {"$regex" : query,"$options":"ig"}})))
	return result
