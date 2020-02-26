from flask import Flask, request, Response
import pymongo
from bson import json_util
import json 


app = Flask(__name__)

MONGO_URI = 'mongodb+srv://username:password@cluster0-gjmtx.mongodb.net/test?retryWrites=true&w=majority'
connection = pymongo.MongoClient(MONGO_URI)
db = connection['Theguardian']

@app.route('/articles')
def articles():

    page = int(request.args.get("page", "1"))
    num_articles = int(request.args.get("num_articles","5"))
    skips = num_articles * (page - 1 )
    
    result = db.articles.find().limit(num_articles).skip(skips)
    return Response(
    	json_util.dumps({
    		'status':'success',
    		'page':page,
    		'num_articles_found':result.count(), 
    		'num_articles_per_page':num_articles,
    		'results' : result}),
    	mimetype='application/json'
	)

@app.route('/search/content')
def search_content():
	
	query = request.args.get("query","")
	query = query.replace(" ","|")

	page = int(request.args.get("page", "1"))
	num_articles = int(request.args.get("num_articles","5"))
	skips = num_articles * (page - 1 )

	result = db.articles.find({"content" : {"$regex" : query,"$options":"ig"}}).limit(num_articles).skip(skips)

	return Response(
    	json_util.dumps({
    		'status':'success',
    		'page':page,
    		'num_articles_found':result.count(), 
    		'num_articles_per_page':num_articles,
    		'results' : result}),
    	mimetype='application/json'
	)

@app.route('/search/headline')
def search_headline():
	
	query = request.args.get("query","")
	query = query.replace(" ","|")
	

	page = int(request.args.get("page", "1"))
	num_articles = int(request.args.get("num_articles","5"))
	skips = num_articles * (page - 1 )

	result = db.articles.find({"headline" : {"$regex" : query,"$options":"ig"}}).limit(num_articles).skip(skips)
	return Response(
    	json_util.dumps({
    		'status':'success',
    		'page':page,
    		'num_articles_found':result.count(), 
    		'num_articles_per_page':num_articles, 
    		'results' : result}),
    	mimetype='application/json'
	)

