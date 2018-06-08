from bs4 import BeautifulSoup
import os,re, cPickle
import extract #contains functions for extracting data from preprocessed strings


#search through html table for
#strings containing country data (messy)
def read_table(fname, folder):
		raw_data = {}
                fpath = os.path.join(folder,fname)

                with open(fpath,'r') as f:
                        html_doc = f.read().decode('utf8')#check if read takes 'utf8' parameter
                        tbl = BeautifulSoup(html_doc,'html.parser')
                #remove subscripts and superscripts
                for x in tbl.findAll(['sup','sub']):
                        x.extract()

                #interpret table as rows
                rows = tbl.findAll('tr')
	
		#extract raw information and place in 'data'
                raw_data['name'] = fname
		for i in range(len(rows)):
                        row_hd = rows[i].th
                        try:
				row_text = rows[i].th.text
			except AttributeError:
				continue

			if row_text == u'Area':
				raw_data['area'] = rows[i+1].td.text
                        elif row_text == u'Official\xa0languages':
                                raw_data['language(s)'] = rows[i].td.text
                        elif row_text == u'Currency':
                                raw_data['currency'] = rows[i].td.text
                        elif row_text == u'GDP\xa0(PPP)':
                                raw_data['GDP (PPP)-tot'] = rows[i+1].td.text
                                raw_data['GDP (PPP)-pc'] = rows[i+2].td.text
                        elif row_text == u'GDP\xa0(nominal)':
                                raw_data['GDP (nom)-tot'] = rows[i+1].td.text
                                raw_data['GDP (nom)-pc'] = rows[i+2].td.text	
		return raw_data



#perform preprocessing on collected data
def preprocess(data):
        for key in data:
		#remove brackets (ie reference markers)
        	data[key] = re.sub(u'\[[\s\S]*?\]',u'',data[key])
        	#remove all parentheses and data within them (except when key == 'area')
        	if key != 'area':
        		data[key] = re.sub(u'\([\s\S]*?\)',u'',data[key])
		#replace any sequence of whitespace with ' ' (except when key == 'language(s)')
        	if key !='language(s)':
      			data[key] = re.sub(u'[\s\xa0]+',u' ',data[key])
		#remove whitespace at start/end of string
        	data[key] = re.sub(u'(^[\s\xa0]+|[\s\xa0]+$)',u'',data[key])
	return data



#return dictionary containing country info
#as dict called data  (dict is populated by calling functions in extract.py)
def extract_data(prepped_data):
        data = {}
        data['name'] = prepped_data['name']
        data['area_km2'],data['area_mi2'] = extract.area(prepped_data)
        data['currency'] = extract.currency(prepped_data)
        data['tot_GDP_nom'] = extract.GDP(prepped_data,'nom','tot')
        data['pc_GDP_nom']  = extract.GDP(prepped_data,'nom','pc')
        data['pc_GDP_PPP'] = extract.GDP(prepped_data,'PPP','pc')
        data['tot_GDP_PPP'] = extract.GDP(prepped_data,'PPP','tot')
        data['language(s)'] = extract.languages(prepped_data)
        return data

if __name__ =="__main__":      
	save_fnm = 'CountryData.pickle'#name of file to save country data to
	save_dir = os.path.dirname(os.getcwd())#directory in which to save file	
	save_fpath = os.path.join(save_dir,save_fnm) 	       
	html_dat_fpath = 'raw_html'
	print "Obtaining country data in '{}'".format(html_dat_fpath)

        #get country data from html files in 'html_dat_fpath'
	country_data = []#list containing country data
	for fname in os.listdir(html_dat_fpath):
		fname = fname.decode('utf8')#handle accents in country/file name
        	raw_data = read_table(fname,html_dat_fpath)
        	prepped_data = preprocess(raw_data)
	        data = extract_data(prepped_data)
        	country_data.append(data)

	#save country data
	with open(save_fpath,'wb') as f:
		cPickle.dump(country_data,f)
	print "Saved to '{}'".format(save_fpath)
