from __future__ import division

import numpy

class City:
	"""docstring for City"""
	def __init__(self, name, sites=None):
		self.name = name
		self.sites = sites
		try:
			self.population = numpy.sum([x.population for x in self.sites])
		except:
			self.population = 0

	def addSite(self, site):
		if self.sites == None:
			self.sites = []

		self.sites.append(site)
		self.population += site.population

	def getContaminants(self):
		return [c for c in Contaminant.contaminants if c.city is self]



class Contaminant:

	contaminants = []

	def __init__(self, name, actual, guideline, state, national, sites, city):
		self.name = name
		self.actual = actual
		self.guideline = guideline
		self.national = national
		self.sites = sites
		Contaminant.contaminants.append(self)
		self.city = city
		self.ppb = None

	@staticmethod
	def createContaminant(name, actual, guideline, state, national, site, city):
		duplicate =  [c for c in Contaminant.contaminants if c.name==name and c.city is city]

		if duplicate:
			if actual is None:
				#print 'TERMINATED'
				return None
			duplicate[0].sites.append(site)
			duplicate[0].actual.append(actual)
			return duplicate[0]

		else:
			return Contaminant(name, [actual], guideline, state, national, [site], city) if actual is not None else None

	def getPPB(self):
		
		#print(self.actual)
		try:
			self.ppb = numpy.average(self.actual, weights=[site.population / self.city.population for site in self.sites])
		except:
			return self.actual
		return self.ppb

	def relativePPB(self):
		self.getPPB()
		return (self.ppb - self.national) / self.national




class Site():

	def __init__(self, name, city_name, population, neighbors=None, contaminants=None):

		self.name = name
		self.city_name = city_name
		self.contaminants = contaminants
		self.neighbors = neighbors
		self.population = population

	def addContaminant(self, contaminant):
		if self.contaminants==None:
			self.contaminants = []

		self.contaminants.append(contaminant)

