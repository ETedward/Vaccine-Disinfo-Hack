"""
Before you start, install the library using: 

pip install GoogleNews

"""

from GoogleNews import GoogleNews
import pandas as pd

googlenews = GoogleNews()

googlenews.set_lang('en')
googlenews.set_encode('utf-8')

"""
Primary Phrases refer to the keywords we are interested in studying
Secondary Phrases refer to the target countries
"""
primary_phrases = ['Pfizer Vaccine', 'AstraZeneca Vaccine', 'Sputnik V Vaccine', 'Sinovac Vaccine']
secondary_phrases = ['Namibia', 'France', 'South Africa']


# months = ['01/01/2019', '02/01/2019', '03/01/2019', '04/01/2019', '05/01/2019', '06/01/2019', '07/01/2019', '08/01/2019', '09/01/2019', '10/01/2019', '11/01/2019', '12/01/2019', '01/01/2020', '02/01/2020', '03/01/2020', '04/01/2020', '05/01/2020', '06/01/2020', '07/01/2020', '08/01/2020', '09/01/2020', '10/01/2020', '11/01/2020', '12/01/2020', '01/01/2021']
"""
Months refer to the date range 
"""
months = ['08/01/2020', '09/01/2020', '10/01/2020', '11/01/2020', '12/01/2020', '01/01/2021']

fin = []

seen = []

for first in primary_phrases:
	for second in secondary_phrases:
		full_phrase = first+" "+second

		print(full_phrase)

		for i in range(0, len(months)-1):
			googlenews.set_time_range(months[i],months[i+1])
			googlenews.get_news(full_phrase)
			res = googlenews.results(sort=True)

			#It would be very easy to get more than the first page. Simply use: googlenews.get_page(2) or result = googlenews.page_at(2), in conjunction with googlenews.total_count() 
			#(to see how many results show up on that page, if there are zero, then probably that'the last page, but I'm not sure if that's exactly how it works)

			for result in res:
				if result['title'] not in seen:
					result['start date'] = months[i]
					result['end date'] = months[i+1]
					result['primary phrase'] = first
					result['secondary phrase'] = second
					result['full phrase'] = full_phrase
					fin.append(result)
					seen.append(result['title'])

df = pd.DataFrame(fin)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(df)

df.to_csv("./output.csv",index=False)