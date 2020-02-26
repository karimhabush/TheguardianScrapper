from flask import Flask, escape, request
import pymongo

app = Flask(__name__)

MONGO_URI = 'mongodb+srv://username:password@cluster0-gjmtx.mongodb.net/test?retryWrites=true&w=majority'
connection = pymongo.MongoClient(MONGO_URI)
db = connection['Theguardian']

@app.route('/articles')
def articles():

    page = int(request.args.get("page", "1"))
    num_articles = int(request.args.get("num_articles","5"))
    skips = num_articles * (page - 1 )
    
    result = str(list(db.articles.find().limit(num_articles).skip(skips)))
    return result

@app.route('/search/content')
def search_content():
	
	query = request.args.get("query","")
	query = query.replace(" ","|")

	page = int(request.args.get("page", "1"))
	num_articles = int(request.args.get("num_articles","5"))
	skips = num_articles * (page - 1 )

	result = str(list(db.articles.find({"content" : {"$regex" : query,"$options":"ig"}}).limit(num_articles).skip(skips)))
	return result

@app.route('/search/headline')
def search_headline():
	
	query = request.args.get("query","")
	query = query.replace(" ","|")
	

	page = int(request.args.get("page", "1"))
	num_articles = int(request.args.get("num_articles","5"))
	skips = num_articles * (page - 1 )

	result = str(list(db.articles.find({"headline" : {"$regex" : query,"$options":"ig"}}).limit(num_articles).skip(skips)))
	return result
