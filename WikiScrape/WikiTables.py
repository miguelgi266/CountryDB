import requests
from bs4 import BeautifulSoup

#link to page containing table of countries with links to wikipedia page
country_tbl_pg = 'https://en.wikipedia.org/wiki/List_of_sovereign_states'
sess = requests.session()
raw_html = sess.get(country_tbl_pg)
html_doc = BeautifulSoup(raw_html.text,'html.parser')


#Extract rows from 1st table in page
table_rows = html_doc.table.findAll('tr')

#ignore first four rows (not countries)
#extract link to wikipedia page of country in row
country_links = []
for row in table_rows[4:]:
	#if row has attribute style or does not have href attribute
	#it does not contain link to a country's wikipedia page, skip
	if row.has_attr('style') == False and row.a.has_attr('href'):
		link = row.a['href']
		#a link containing '#' belongs to different section
		#in page, it is therefore not link to a country's page, skip
		if '#' not in link:
			country_links.append(link)


homepage = 'https://en.wikipedia.org'
#for each link, open link, retrieve, and clean data
for link in country_links:
        html_doc = sess.get(homepage+link)
	html_doc = html_doc.text
	soup = BeautifulSoup(html_doc,'html.parser')
        name = soup.body.find('h1',attrs = {'id':'firstHeading'}).text
	print 'obtained data for',name
	with open(u'raw_html/'+name,'w') as f:
		tbl = soup.find('table',class_ = 'infobox geography vcard')
		f.write(unicode(tbl).encode('utf8'))
sess.close()
