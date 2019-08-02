from flask import *
import os, json,requests,datetime
from bs4 import BeautifulSoup
app = Flask(__name__)

To_date = str(datetime.date.today())
if os.path.exists(To_date+".json"):
	with open(To_date+".json", "r") as file:
		read_data = file.read()
		top_news = json.loads(read_data)

	@app.route("/chatbot/AllNews")
	def get_alldata():
		return jsonify({'top_news':top_news})

	@app.route("/chatbot/AllNews/<category>")
	def get_all_data(category):
		return jsonify(top_news[category])
else:
	top_news = {"world":[],"business":[],"technology":[],"sports":[],"entertainment":[]}
	def Scraper_news():
		new_dic = {}
		URLS_of_menu = {"world":"http://www.newzcone.com/world/","business":"http://www.newzcone.com/business/",
		"technology":"http://www.newzcone.com/technology/networking-telecom/",
		"sports":"http://www.newzcone.com/sports/","entertainment":"http://www.newzcone.com/entertainment/"}
		Today = datetime.date.today()
		today = ""
		for string in str(Today):
			if string == "-":
				today +="/"
			else:
				today+=string
		for key in URLS_of_menu:
			url = URLS_of_menu[key]
			html = requests.get(url)
			soup = BeautifulSoup(html.text,"html.parser")
			findingUrl = soup.findAll("div",class_="news-entry")
			for div in findingUrl:
				a_tags = div.findAll("a")
			count = 0
			for a in a_tags:
				new_dic["Date"] = today
				new_dic["Discription"] = a.get_text().strip()
				new_dic["News_URL"] = a["href"]
				html = requests.get(a["href"])
				needsoup = BeautifulSoup(html.text,"html.parser")
				get_title = needsoup.title.get_text().strip()
				new_dic["Title"] = get_title
				count +=1
				if count == 5:
					break
				top_news[key].append(new_dic.copy())
		return(top_news)
	Master_data = Scraper_news()

	with open(To_date+".json","w") as file:
		read_data = json.dumps(Master_data, indent=4, sort_keys=True)
		file.write(read_data)
		file.close()

	@app.route("/chatbot/AllNews")
	def get_alldata():
		return jsonify({'top_news':top_news})

	@app.route("/chatbot/AllNews/<category>")# in the <categoty> user will enter the commands the he wants
	def get_all_data(category):
		return jsonify(top_news[category])

if __name__ == "__main__" :
	app.run(debug = True)