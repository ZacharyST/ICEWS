'''
The purpose of this script is to take ICEWS data and compare its protest recording with GDELT.
v2- Saved once create protests dataset.  
v3 - Updated read_csv to know that CAMEO Code is string, so don't have to have line 30 to modify string manually.
'''
import pandas as pd
import datetime as dt



#Vestigial from earlier code where needed to convert from GDELT 2-letter code to full name.
protestFullCountries = {'AG':'Algeria','BA':'Bahrain','EG':'Egypt','IZ':'Iraq','JO':'Jordan','KU':'Kuwait','LE':'Lebanon','LY':'Libya','MO':'Morocco','MU':'Oman','QA':'Qatar','SA':'SaudiArabia','SY':'Syria','TS':'Tunisia','AE':'UnitedArabEmirates','YM':'Yemen'} 

#################################################
#
#		READ IN DATA
#			- No longer necessary for creating protest data
#################################################
data = pd.read_csv('/Users/Zack/Documents/UCSD/Data/ICEWS/events.2010.20150313084533.tab', sep = '\t',dtype={'CAMEO Code':object})
data2 = pd.read_csv('/Users/Zack/Documents/UCSD/Data/ICEWS/events.2011.20150313084656.tab', sep = '\t',dtype={'CAMEO Code':object})
data = data.append(data2)

cols = {col: col.replace(' ', '_') for col in data.columns}
data.rename(columns=cols,inplace=True)

#Keep only starting at 2010-11-01
data = data[data['Event_Date'] > '2010-11'] #Keeps Nov. 1 since that is '2010-11-01'. Confirm with set(data['Event_Date'])

#Add leading zero to two-digit codes.  EventRootCodes should be 2 digits long, but those that are less than 10 are not given a leading zero.  This code  are supposed to all start with 3 digits.  For example, 18 is actually "Make Empathetic Comment", (01-8) not "Assault" (18).  018 therefore is now "Make Empathetic Comment".  There are no instances of 18 being Assault (or 14 being protests) - no missing trailing zeroes - so this works so long as that pattern holds.   
#data['CAMEO_Code_Modified'] = ['%03d' %item if len(str(item)) <= 2 else item for item in data['CAMEO_Code']]

#Keep only protests.  To do that, first need to standardize CAMEO Code.  
keep = [True if '14' == str(item)[0:2] else False for item in data['CAMEO_Code_Modified']]
protests = data[keep]

#Save out.  31,959 protests across the world in 13 months.  
protests.to_csv('/Users/Zack/Documents/UCSD/Data/ICEWS/2010_2011_AllProtests.csv',index=False)


#################################################
#
#		DEFINE FUNCTIONS
#
#################################################
def selectCountry(country, data = protests):
	temp = data[data['Country'] == country]
	return temp

def aggCountry(data):
	temp = data 
	temp['Protest'] = 1
	temp = temp.groupby('Event_Date').aggregate({'Protest':'sum'}) #Create daily protest count,
	#temp.reset_index(inplace=True) #Make Event_Date a column
	return temp


def addMissingDates(data, start_date = '2010-11-01', end_date = '2011-12-31'):
	#### There are 426 days that each country should have.
	idx = pd.date_range(start_date, end_date)

	data.index = pd.DatetimeIndex(data.index)
	data = data.reindex(idx,fill_value=0) #This line does the magic

	return data

def saveOut(country, data):
	data['country'] = country
	data.to_csv('/Users/Zack/Documents/UCSD/Dissertation/Papers/RetweetsAndProtest/ProcessedData/ICEWS/ICEWS_All_Protests_'+ country + '.csv')


#################################################
#
#		DO WORK
#
#################################################
protests = pd.read_csv('/Users/Zack/Documents/UCSD/Data/ICEWS/2010_2011_AllProtests.csv')

countries = protestFullCountries.values()

for country in countries:
	print 'Working on %s' %country
	country_protests = selectCountry(country,data=protests)
	country_agg = aggCountry(data=country_protests)
	country_all_dates = addMissingDates(data=country_agg, start_date = '2010-11-01', end_date = '2011-12-31')
	saveOut(country, data = country_all_dates)

