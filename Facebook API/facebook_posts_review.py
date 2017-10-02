from flask import Flask
from flask import render_template
from flask import request
import requests
import re

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('facebook_details.html')

@app.route("/result", methods=['GET', 'POST'])  
def display():
  base_url = "https://graph.facebook.com/v2.8/me/feed?access_token=" + request.form['token'] + "&since=" + request.form['since'] + "&until=" + request.form['until'] + "&limit=100"
  req = requests.get(base_url)
  if req.status_code == 200:
    content = req.json()
    complete_data = content['data']
    print complete_data
  while content.has_key("paging") and content['paging'].has_key("next"): 
	next_set = content['paging']['next']
	reqt = requests.get(next_set)
	res = reqt.json()
	complete_data = complete_data + res['data']
	content = res
	reviews = {}
	for post in complete_data:
	  key_n = post['created_time'][0:7]	
	  if not reviews.has_key(key_n):
	    reviews[key_n] = 1
	  else:
	    reviews[key_n] = reviews[key_n] + 1    
  return render_template('welcome.html',output=reviews)
  
if __name__ == "__main__":
  app.run(debug=True)