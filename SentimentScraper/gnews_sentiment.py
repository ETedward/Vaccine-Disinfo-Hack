"""
Before you start, install the library using: 

pip install GoogleNews

"""

from GoogleNews import GoogleNews
import pandas as pd

#Sentiment Analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import csv


def main():

	sid_obj = SentimentIntensityAnalyzer() 	

	googlenews = GoogleNews()
	googlenews.set_lang('en')
	googlenews.set_encode('utf-16')

	"""
	Primary Phrases refer to the keywords we are interested in studying
	Secondary Phrases refer to the target countries
	"""
	company_name = ['Pfizer', 'AstraZeneca', 'Sputnik', 'Sinovac']

	# testing_countries = ['Egypt', 'Kenya', 'Nigeria', 'Zambia']
	testing_countries = []

	"""
	Months refer to the date range 
	"""
	months = ['08/01/2020', '09/01/2020', '10/01/2020']
	# months = ['01/01/2019', '02/01/2019', '03/01/2019', '04/01/2019', '05/01/2019', '06/01/2019', '07/01/2019', '08/01/2019', '09/01/2019', '10/01/2019', '11/01/2019', '12/01/2019', '01/01/2020', '02/01/2020', '03/01/2020', '04/01/2020', '05/01/2020', '06/01/2020', '07/01/2020', '08/01/2020', '09/01/2020', '10/01/2020', '11/01/2020', '12/01/2020', '01/01/2021']

	for first in company_name:

		fin = []
		seen = []
		
		with open('sample.csv', mode='r') as csv_file:
			csv_reader = csv.DictReader(csv_file)
			
			for row in csv_reader:
				# print(row)
				second = row['\ufeffCountry']
				if (second not in testing_countries&&len(testing_countries)!=0): 
					continue

				full_phrase = first+" "+second

				# print(full_phrase)

				for i in range(0, len(months)-1):
					googlenews.set_time_range(months[i],months[i+1])
					googlenews.get_news(full_phrase)
					res = googlenews.results()

					#It would be very easy to get more than the first page. Simply use: googlenews.get_page(2) or result = googlenews.page_at(2), in conjunction with googlenews.total_count() 
					#(to see how many results show up on that page, if there are zero, then probably that'the last page, but I'm not sure if that's exactly how it works)

					for result in res:
						if result['title'] not in seen:
							# print(result)
							result['start date'] = months[i]
							result['end date'] = months[i+1]
							result['company'] = first
							result['country'] = second
							result['latitude'] = row['Latitude']
							result['longitude'] = row['Longitude']

							sentiment_dict = sid_obj.polarity_scores(result['title'])
							result['% Negative'] = sentiment_dict['neg']*100
							result['% Neutral'] = sentiment_dict['neu']*100
							result['% Positive'] = sentiment_dict['pos']*100
							result['Magnitude'] = sentiment_dict['compound']*50 + 50
							
							# result.pop('date')
							# result.pop('datetime')
							# result.pop('img')
							# result.pop('media')

							fin.append(result)
							seen.append(result['title'])

			df = pd.DataFrame(fin)
			df.drop(columns=['date', 'datetime', 'img', 'media'])
			df.to_csv("./Output/{}_output.csv".format(first),index=False)

if __name__ == "__main__":
    main()