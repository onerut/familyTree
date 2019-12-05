from bs4 import BeautifulSoup


class htmlParser:
	def __init__(self, htmlFile):
		self.soup = BeautifulSoup(htmlFile, 'html.parser')

	def parse(self):
		#get all row elements
		tr_list = self.soup.find_all("tr")
		
		#delete the last two rows as they are useless data
		tr_list.pop(len(tr_list)-1)
		tr_list.pop(len(tr_list)-1)

		#get the first row which contains the legend for the table
		legend = tr_list.pop(0)
		attributes = list()

		#create a list of attributes for each ancestor
		for th in legend.find_all("th"):
			attributes.append(th.string)

		#get individuals' data in the table and put them into a list of dicts
		family_members = list()
		for tr in tr_list:
			td_list = tr.contents
			family_member = dict()
			for index,td in enumerate(td_list):
				if td.string == "\n":
					td_list.pop(index)
			for index,td in enumerate(td_list):
				value = str()
				if td.string is None:
					for string in td.stripped_strings:
						value = value + "\n" + string
				else:
					value = td.string
				value = value.strip('\n')
				family_member[attributes[index]] = value
			
			family_members.append(family_member)

		#list complete. Now return it.
		return family_members
