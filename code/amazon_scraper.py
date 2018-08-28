import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import pdb
import requests
import time
from random import randint
import csv

# Ignore SSL certificate errors
ssl._create_default_https_context = ssl._create_unverified_context

phones = {
			"iphone6": "https://www.amazon.com/Apple-iPhone-Factory-Unlocked-Phone/product-reviews/B00NQGP42Y/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews",
			"iphone7": "https://www.amazon.com/Apple-iPhone-Unlocked-Black-Version/product-reviews/B01M1EXQY4/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews",
			"galaxys8": "https://www.amazon.com/Samsung-Galaxy-S8-Unlocked-64GB/product-reviews/B06Y14T5YW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews",
			"galaxys7": "https://www.amazon.com/Samsung-Galaxy-S7-Edge-G935F/product-reviews/B01CJU9BBM/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews",
			"galaxynote8": "https://www.amazon.com/Samsung-Galaxy-SM-N950F-Factory-Unlocked/product-reviews/B075KQ622T/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
			}


for phone_name, phone_url in phones.items():
	
	print("Scraping " + phone_name)

	start_page = 1
	if phone_name == "galaxynote8" :
		end_page = 8
	else :
		end_page = 50
        
	# To get the last page
	# end_page = int(str(soup.find_all("li", attrs={"class": "page-button"})[-1]).split("\">")[2].split("<")[0])

	csv_data = [["Rating", "Title", "Date", "Verified Purchase", "Body", "Helpful Votes"]]

	with open(('../data/' + phone_name + '.csv'), 'w') as csv_file :
		writer = csv.writer(csv_file, delimiter=',')
		writer.writerows(csv_data)

	while start_page <= end_page :

		csv_data = []

		sleep_time = randint(0, 3)
		print("\nSleeping for " + str(sleep_time) + " seconds.")
		time.sleep(sleep_time)

		print("Scraping page " + str(start_page))

		url = phone_url + "&pageNumber=" + str(start_page)

		# Amazon blocks requests that don't come from browser. Hence need to mention user-agent
		user_agent = 'Mozilla/5.0'
		headers = {'User-Agent' : user_agent}

		values = {}

		data = urllib.parse.urlencode(values).encode('utf-8')
		req = urllib.request.Request(url, data, headers)
		response = urllib.request.urlopen(req)
		html = response.read()

		soup = BeautifulSoup(html, 'html.parser')

		reviews = soup.find_all("div", attrs={"class": "a-section review"})

		for review in reviews :

			csv_body = []

			# Star Rating
			rating = str(review).split("<span class=\"a-icon-alt\">")[1].split("</span>")[0].split(" ")[0]
			csv_body.append(rating)

			# Title
			title = str(review).split("data-hook=\"review-title\"")[1].split("\">")[1].split("</a>")[0]
			csv_body.append(title)
			
			# Date
			date = str(review).split("data-hook=\"review-date\">")[1].split("</span>")[0].split("on ")[1]
			csv_body.append(date)

			# Verified Purchase
			try :
				# 1 = purchased, 2 = not purchased
				verified_purchased = str(review).split("data-hook=\"avp-badge\">")[1].split("</span>")[0]
				csv_body.append("1")
			except :
				csv_body.append("0")

			# Body
			body = str(review).split("data-hook=\"review-body\">")[1].split("</span>")[0] + "\n"
			# to remove <br>, <br/> and </br>
			body = body.replace("<br>", ".").replace("<br/>", ".").replace("</br>", ".").strip()
			csv_body.append(body)

			# Helpful Votes
			try :
				votes = str(review).split("data-hook=\"helpful-vote-statement\"")[1].split(">")[1].split("<")[0].strip().split()
				if votes[0] == "One" :
					csv_body.append("1")
				else :
					csv_body.append(votes[0])
			except :
				csv_body.append("0")

			csv_data.append(csv_body)

		print("Writing to file.\n")

		with open(('../data/' + phone_name + '.csv'), 'a') as csv_file :
			writer = csv.writer(csv_file, delimiter=',')
			writer.writerows(csv_data)

		start_page += 1
