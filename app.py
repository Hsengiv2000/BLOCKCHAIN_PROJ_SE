from flask import Flask, render_template, request, redirect, url_for, flash
app = Flask(__name__)
import json as js
from flask import json
from flask_restful import Resource, request, reqparse
from bson.json_util import dumps, default
from bson import json_util
from random import random
import pymongo
from bson.objectid import ObjectId

def parse_json(data):
    return json.loads(json_util.dumps(data))
myclient = pymongo.MongoClient("mongodb://localhost:27017/") #Connecting to the local MongoDB database
mydb = myclient["blockchain"] #the json file has been imported as a db
donations = mydb["donations"] #the collection inside the database
projects =mydb["projects"]


@app.route("/",methods = ['POST', 'GET'])
def login():
	##metamask?

	return render_template('login.html')
@app.route("/home",methods = ['POST', 'GET'])
def home():
	##metamask?

	return render_template('home.html')

@app.route("/new",methods = ['POST', 'GET'])
def addProject():
	dictionary = dict(request.form)
	dictionary["creator_address"]= request.cookies.get("address")
	print(dictionary)
	try:
		projects.insert_one(dictionary)
		return redirect(url_for('home'))
	except Exception as e:
		pass

	return render_template('new-project.html')

@app.route("/fund",methods = ['POST', 'GET'])
def fundProject():
	dics={}
	counter=0
	for i in projects.find():
		counter+=1
		dics[counter]=parse_json(i)
	#print(dics)
	#list_projects = []
	#for outer_key in dics:
		#temp = []
		#for inner_key in dics[outer_key]:
			#if inner_key == 'name' or inner_key == 'description' or inner_key == 'img':
			#	temp.append(dics[outer_key][inner_key])

		#list_projects.append(temp)
	#print(list_projects)

	#projects = [["static/start.jpg", "Test Title", "Test Description",],["static/start.jpg", "Test Title", "Test Description",],["static/start.jpg", "Test Title", "Test Description",]]
	return render_template('fund.html', projects = dics)

@app.route("/view",methods = ['POST', 'GET'])
def viewProject():
	dics={}
	address = request.cookies.get("address")
	
	print("actual address" , request.cookies.get("address"))
	counter=0
	for i in projects.find():

		if i.get("creator_address",None) == address:
			counter+=1
			dics[counter]=parse_json(i)
	#print(dics)
	#list_projects = []
	#for outer_key in dics:
		#temp = []
		#for inner_key in dics[outer_key]:
			#if inner_key == 'name' or inner_key == 'description' or inner_key == 'img':
			#	temp.append(dics[outer_key][inner_key])

		#list_projects.append(temp)
	#print(list_projects)

	#projects = [["static/start.jpg", "Test Title", "Test Description",],["static/start.jpg", "Test Title", "Test Description",],["static/start.jpg", "Test Title", "Test Description",]]
	return render_template('ViewProj.html', projects = dics)

@app.route("/project/<pid>",methods = ['POST', 'GET'])
def projectDetails(pid):
	print(pid)
	address = request.cookies.get("address")
	print(pid.split(":")[1].strip()[0:-1].strip("'"))
	proj = [i for i in projects.find({"_id": ObjectId(str(pid.split(":")[1].strip()[0:-1].strip("'")))})][0]
	print(proj)

	return render_template('project.html', name= proj['name'], deadline=proj['enddate'], description=proj['description'], img = "static/start.jpg", address=address)

@app.route("/donations/<key>/<value>",methods = ['POST', 'GET'])
def getDonation(key,value):

	#print (donations.find({key:value}))
	return list(donations.find({key:value}))

#@app.route("/alldonations",methods = ['POST', 'GET'])
#def getAllDonation():

	#print (donations.find({key:value}))
	#dics={}
	#counter=0
	#for i in projects.find():
	#	counter+=1
	#	dics[counter]=parse_json(i)
	#print(dics)
	#return dics
		





#@app.route("/project/<key>/<value>",methods = ['POST', 'GET'])
#def getDonation(key,value):
	
	#print (projects.find({key:value}))
	#return str(list(donations.find({key:value})))


if __name__ == "__main__": #Running on port 3306
    app.run(host = '0.0.0.0' , port=2000)
	