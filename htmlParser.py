from html.parser import HTMLParser

from bs4 import BeautifulSoup


class htmlParser:
	def __init__(self, htmlFile):
		self.soup = BeautifulSoup(htmlFile, 'html.parser')

	def parse(self):
		trList = self.soup.find_all("tr")
		trList.pop(len(trList)-1)
		trList.pop(len(trList)-1)
		print(trList)
		return True
