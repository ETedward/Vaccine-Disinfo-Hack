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

	all_df = []

	sid_obj = SentimentIntensityAnalyzer() 	

	googlenews = GoogleNews()
	googlenews.set_lang('en')
	googlenews.set_encode('utf-16')

	"""
	Primary Phrases refer to the keywords we are interested in studying
	Secondary Phrases refer to the target countries
	"""
	company_name = ['Pfizer', 'AstraZeneca', 'Sputnik', 'Sinovac', 'Moderna', 'Johnson & Johnson']

	# testing_countries = ['Egypt', 'Kenya', 'Nigeria', 'Zamibia']
	testing_countries = []

	"""
	Months refer to the date range 
	"""
	# months = ['08/01/2020', '09/01/2020', '10/01/2020']
	months = ['01/01/2020', '02/01/2020', '03/01/2020', '04/01/2020', '05/01/2020', '06/01/2020', '07/01/2020', '08/01/2020', '09/01/2020', '10/01/2020', '11/01/2020', '12/01/2020', '01/01/2021', '02/01/2021']

	for first in company_name:

		fin = []
		seen = []
		
		with open('sample.csv', mode='r') as csv_file:
			csv_reader = csv.DictReader(csv_file)
			
			summary_data = []

			for row in csv_reader:
				# print(row)
				second = row['\ufeffCountry']
				if (second not in testing_countries and len(testing_countries)!=0): 
					continue

				full_phrase = first+" "+second

				print(full_phrase)

				counter = 0
				sum_sent = 0
				
				pos_count = 0
				# neu_count = 0
				neg_count = 0

				neg_article = {'title': 'N/A', '% Negative': 0}

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

							counter += 1
							sum_sent += result['Magnitude']
							
							# result.pop('date')
							# result.pop('datetime')
							# result.pop('img')
							# result.pop('media')

							# if result['% Negative'] > result['% Neutral'] and result['% Negative']>result['% Positive']: neg_count += 1
							# elif result['% Neutral'] > result['% Positive']: neu_count += 1
							# else: pos_count += 1
							if result['% Positive'] > result['% Negative']: pos_count += 1
							else: neg_count += 1

							if result['% Negative'] >= neg_article['% Negative']: neg_article = result

							fin.append(result)
							seen.append(result['title'])

				posPercent = 50
				if pos_count+neg_count>0: posPercent = pos_count/(pos_count + neg_count)

				country_comp_score = {'country': second, 'latitude': row['Latitude'], 
				'longitude': row['Longitude'], 'magnitude': (sum_sent/counter), 'positive': pos_count, 
				'negative': neg_count, 'pos/(pos+neg)': posPercent, 'Most negative title': neg_article['title']}

				summary_data.append(country_comp_score)
				all_df.append((country_comp_score, first))

			df = pd.DataFrame(fin)
			df.drop(columns=['date', 'datetime', 'img', 'media'])
			df.to_csv("./Output/{}_output.csv".format(first),index=False)

			summary_df = pd.DataFrame(summary_data)
			summary_df.to_csv("./Output/{}_summary_output.csv".format(first),index=False)
			# all_df.append(summary_df)
	
	# meta_data = []
	# # with open('sample.csv', mode='r') as csv_file:
	# dic_len = sum(1 for line in open('sample.csv'))

	# with open('sample.csv', mode='r') as csv_file:
	# 	csv_reader = csv.DictReader(csv_file)
	# 	for j in range(0, dic_len):
	# 		most_pos = 0
	# 		for i in range(0, len(company_name)):
	# 			if all_df[most_pos][j]['positive']<all_df[i][j]['positive']: 
	# 				most_pos = i
	# 		meta_data.append({all_df[0][j]['\ufeffCountry']: company_name[most_positive]})

	fields = ['Country', 'Company', 'Count']  

	meta_data = []
	seen = []
	for result in all_df:
		if result[0]['country'] not in seen:
			seen.append(result[0]['country'])
			meta_data.append([result[0]['country'], result[1], result[0]['positive']])
		else:
			for candidate in meta_data:
				if candidate[0]==result[0]['country'] and candidate[2]<result[0]['positive']:
					candidate[1] = result[1]
					candidate[2] = result[0]['positive']

	with open('./Output/meta_data.csv', 'w') as f:
		write = csv.writer(f)      
		write.writerow(fields)
		write.writerows(meta_data)

if __name__ == "__main__":
    main()