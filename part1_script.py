import urllib2
import xml.etree.ElementTree as ET
import copy
import matplotlib.pyplot as plt
from collections import defaultdict


#Generatin a dictionary where the 'key' is the country and the 'value' is the a list of santiation values. Parameters are api url and information to extract.	
class AllCountries:
	def __init__(self, url, paramC, paramV, paramD):
		temp = {}
		self.temp = temp
		self.url = url
		self.paramC = paramC
		self.paramV = paramV
		self.paramD = paramD

		file = urllib2.urlopen(url)
		tree = ET.parse(file)
		root = tree.getroot()

		country = ''
		prev_country = ''
		value = ''
		year = ''
		prev_year = ''
	
		values = []
		same = False

		for child in root:
			for child2 in child:
				a = str(child2.tag)
				if (a == '{http://www.worldbank.org}'+paramC):
					if country != child2.text:
						if country != '':
							prev_country = country
						country = child2.text
						same = False
					else:
						same = True
				elif (a == '{http://www.worldbank.org}'+paramV):
					value = child2.text
				elif (a == '{http://www.worldbank.org}'+paramD):
					year = child2.text
				else:
					pass

			if value == None:
				value = 'None'
			if same:
				value  = year +'-'+value
				values.append(value)
				temp[country] = values
			elif prev_country!='':
				new_list = copy.copy(values)
				temp[prev_country] = new_list
				del values[:]

#Generates a set of countries based on there income level. Parameters are api url and information to extract.		
class IncomeCountries:
	def __init__(self, url, paramN):
		countries = set()
		self.url = url
		self.paramN = paramN
		self.countries = countries
		file = urllib2.urlopen(url)
		tree = ET.parse(file)
		root = tree.getroot()
		

		for child in root:
			for child2 in child:
				a = str(child2.tag)
				if (a == '{http://www.worldbank.org}'+paramN):
					countries.add(child2.text)


#Set figure size and text box
fig = plt.figure(figsize=(18,18))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
fig.text(0.05, 0.95, 'The general trend for sanitation facilities can be seen in the scatter plot titled "All Countries" this figure shows how the average of the sanitation values across the world were gradually increasing \n till about the mid 2000s then began to decrease. When we look at the average values in figures representing the "Income Group" the low income countries have the lowest average, \n while the high income countries have the highest, and understandably the middle income countries values are between the high income and low income countries.', fontsize='11',  verticalalignment='top', bbox=props)

#Creates subplots. Parameters are titles and positions on chart.
class FIGURE:
	def __init__(self,T1,POS1,T2,POS2,T3,POS3,T4,POS4):
		self.T1 = T1
		self.POS1 = POS1
		self.T2 = T2
		self.POS2 = POS2
		self.T3 = T3
		self.POS3 = POS3
		self.T4 = T4
		self.POS4 = POS4


		plot1 = fig.add_subplot(POS1)
		plot1.set_title(T1)
		plot1.set_ylabel('Sanitation Values')
		plot1.set_ylim([0, 10000])
		plot1.set_xlim([1960,2018])
		self.plot1 = plot1

		plot2 = fig.add_subplot(POS2)
		plot2.set_title(T2)
		plot2.set_xlabel('Years')
		plot2.set_ylabel('Sanitation Values')
		plot2.set_ylim([0, 10000])
		plot2.set_xlim([1960,2018])
		self.plot2 = plot2

		plot3 = fig.add_subplot(POS3)
		plot3.set_title(T3)
		plot3.set_ylabel('Sanitation Values')
		plot3.set_ylim([0, 10000])
		plot3.set_xlim([1960,2018])
		self.plot3 = plot3

		plot4 = fig.add_subplot(POS4)
		plot4.set_title(T4)
		plot4.set_xlabel('Years')
		plot4.set_ylabel('Sanitation Values')
		plot4.set_ylim([0, 10000])
		plot4.set_xlim([1960,2018])
		self.plot4 = plot4

#Creates scatter plot. Parameters are dictionary, graph instance, marker, and color for plot.
class XY:
	def __init__(self, dictionary, graph, m, c):
		x = []
		y = []
		self.dictionary = dictionary
		self.graph = graph
		self.m = m
		self.c = c
		
		#fills graph with average santiation values of that year
		for year in dictionary:
			avg = sum(dictionary[year])/float(len(dictionary[year]))
			y.append(avg)
			x.append(year)	
		graph.scatter(x,y, marker=m, color=c)

def main():

	#Dictionary with key = country abd value = list of sanitation values.
	ALL = AllCountries('http://api.worldbank.org/v2/countries/all/indicators/SH.STA.ACSN?date=1960:2018&per_page=17000', 'country', 'value', 'date')
	
	#Sets of countries based on income level
	low_income_countries = IncomeCountries('http://api.worldbank.org/v2/countries?incomeLevel=LIC','name')
	middle_income_countries = IncomeCountries('http://api.worldbank.org/v2/countries?incomeLevel=MIC&per_page=150','name')
	high_income_countries = IncomeCountries('http://api.worldbank.org/v2/countries?incomeLevel=HIC&per_page=100','name')

	#dictionaries
	temp_lic = defaultdict(list)
	temp_mic = defaultdict(list)
	temp_hic = defaultdict(list)
	temp_world = defaultdict(list)

	#fills above 4 dictionaries where key is year, and value is list of sanitation values of that year. Adds to appropriate dictionary based on income level of country
	for country in ALL.temp:
		for value in ALL.temp[country]:
			parts = value.split('-')
			year = parts[0]
			sanitation = parts[1]
			if (sanitation!='None'):
				temp_world[year].append(float(sanitation))
			if country in low_income_countries.countries:
				parts = value.split('-')
				year = parts[0]
				sanitation = parts[1]
				if (sanitation!='None'):
					temp_lic[year].append(float(sanitation))
			elif country in middle_income_countries.countries:
				parts = value.split('-')
				year = parts[0]
				sanitation = parts[1]
				if (sanitation!='None'):
					temp_mic[year].append(float(sanitation))
			elif country in high_income_countries.countries:
				parts = value.split('-')
				year = parts[0]
				sanitation = parts[1]
				if (sanitation!='None'):
					temp_hic[year].append(float(sanitation))
	
	#generates subplots
	g = FIGURE("Low Income Countries",221,"Middle Income Countries",223,"High Income Countries",222,"All Countries",224)

	#fills subplots with scatter plots of average values for relevant years from relevant income group dinctionary
	l = XY(temp_lic, g.plot1,'o','red')
	m = XY(temp_mic, g.plot2,'o','orange')
	h = XY(temp_hic, g.plot3,'o', 'green')
	w = XY(temp_world, g.plot4,'*','blue')

	fig.savefig('part1_output.pdf')

	
if __name__ == "__main__":
	main()







