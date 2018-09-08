

import mechanize
from bs4 import BeautifulSoup
import sys
import StringIO
from Data_Objects import *


def getCityData(search_city, search_state):

	br = mechanize.Browser()
	#br.set_all_readonly(False)    # allow everything to be written to
	br.set_handle_robots(False)   # ignore robots
	br.set_handle_refresh(False)
	br.addheaders = [('User-agent', 'Firefox')]

	br.open('https://www.ewg.org/tapwater/advanced-search.php')

	br.select_form(nr = 1)
	br.form = list(br.forms())[1]  # use when form is unnamed
	control = br.form.find_control('stab') 
	control.readonly = False
	control.value =  [search_state.decode('utf-8', 'ignore')]


	control = br.form.find_control('systemname') 
	control.readonly = False
	control.value =  search_city
	response = br.submit() 


	raw =  br.response().read()
	html = BeautifulSoup(raw, 'html.parser')

	cities =  html.select('table')[0] #raises Index Error if no data

	city = City(search_city)

	rows = cities.tbody.find_all('tr')

	if rows == None:
		print "no results found"
		exit()


	for row in rows:
		cols = row.find_all('td')
		city.addSite(Site(cols[0].a.getText(), cols[1].getText(), int(cols[2].getText().split(': ')[1].replace(',',''))))


	base_url = br.geturl()

	for selected in city.sites:

		br.open(base_url)

		raw =  br.response().read()
		#print selected.name

		city_link = br.find_link(text=selected.name)
		br.follow_link(city_link)
		#print("*************")


		raw =  br.response().read()
		html = BeautifulSoup(raw, 'html.parser')

		sections = html.find_all('section')
		contaminants = [ c for c in sections if c.has_attr('class') and c['class'][0]=="contaminant-data"]

		contaminants = [c for c in contaminants if c.div.h3.br == None]

		# d = contaminants[0].parent.parent.parent
		# contaminants_above = [c for c in contaminants if c.parent.parent.parent and c.parent.parent.parent.has_attr('id') and c.parent.parent.parent['id']=='contams_above_hbl']

		
		for c in contaminants:
			#print(c.div.h3)
			try:
				national = c.find('div', attrs={"class":"national-ppb-popup"}).getText().replace(',','')
			except AttributeError:
				national_ppb = None
			except ValueError:
				continue
			else:
				national_ppb = float(national.split(' ')[0])
				if national.split(' ')[1] == 'ppm':
					national_ppb *= 1000
				elif national.split(' ')[1] == 'ppt':
					national_ppb /= 1000


			try:
				state = c.find('div', attrs={"class":"state-ppb-popup"}).getText().replace(',','')
			except AttributeError:
				state_ppb = None
			except ValueError:
				continue
			else:
				state_ppb = float(state.split(' ')[0])
				if state.split(' ')[1] == 'ppm':
					state_ppb *= 1000
				elif state.split(' ')[1] == 'ppt':
					state_ppb /= 1000


			try:
				utility = c.find('div', attrs={"class":"this-utility-ppb-popup"}).getText().replace(',','')
			except AttributeError:
				utility_ppb = None
			except ValueError:
				continue
			else:
				utility_ppb = float(utility.split(' ')[0])
				if utility.split(' ')[1] == 'ppm':
					utility_ppb *= 1000
				elif utility.split(' ')[1] == 'ppt':
					utility_ppb /= 1000


			try:
				guideline = c.find('div', attrs={"class":"health-guideline-ppb"}).getText().replace(',','')
			except AttributeError:
				guideline_ppb = None
			except ValueError:
				continue
			else:
				guideline_ppb = float(guideline.split(':')[1].split(' ')[0])
				if guideline.split(' ')[1] == 'ppm':
					guideline_ppb *= 1000
				elif guideline.split(' ')[1] == 'ppt':
					guideline_ppb /= 1000

			cont = Contaminant.createContaminant(c.div.h3.getText(), utility_ppb, guideline_ppb, state_ppb, national_ppb, selected, city)
			if cont is not None:
				selected.addContaminant(cont)

	#cont_objs = city.getContaminants()
	#print(cont_objs)
	return city







	#