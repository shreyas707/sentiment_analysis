import pdb
import csv

csv_files = ["galaxynote8.csv", "galaxys7.csv", "galaxys8.csv", "iphone6.csv", "iphone7.csv"]

with open("../data/all_reviews.tsv", "w") as all_reviews :
	all_reviews.write("Reivew\tRating")

for csv_file in csv_files :
	with open("../data/all_reviews.tsv", "a") as all_reviews :
		with open('../data/' + csv_file) as csvfile :
			reader = csv.DictReader(csvfile)
			for row in reader :
				if row["Rating"] == "1.0" or row["Rating"] == "2.0" :
					all_reviews.write("\n" + row["Body"] + "\t" + "0")
				else :
					all_reviews.write("\n" + row["Body"] + "\t" + "1")
