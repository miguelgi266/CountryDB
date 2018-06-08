
###Contains methods to extract appropriate data from strings preprocessed with
###

import re

#return tuple of floats containing area in km2 and mi2 from data['area'], (where possible)
#return None for whichever value that is unretrievable
def area(country):
        try:
                area_km2 = re.search(u'[0-9,\.]+(?= km)',country['area']).group(0)
                area_km2 = re.sub(u',',u'',area_km2)
        except:#AttributeError (Maybe??)
                area_km2 = None
        try:
                area_mi2 = re.search(u'[0-9,\.]+(?= sq mi)',country['area']).group(0)
                area_mi2 = re.sub(u',',u'',area_mi2)
        except:
                area_mi2 = None



        return area_km2, area_mi2

#returns string containing name of first currency to occur in the 
#'Currency' row of table, if possible. Else returns None
def currency(country):
        try:
                currency = re.match(u'.+?(?=\s*(,|$))',country['currency']).group(0)
        except:
                currency = None
        return currency


#depending on parameters, returns tot. (nom.) GDP,
#tot. (PPP) GDP, per cap. (nom.) GDP or 
#per cap. (PPP) GDP as float, if possible. else returns None
def GDP(country, metric, pop):
        key = 'GDP ({})-{}'.format(metric,pop)
        if pop =='tot':
                w2n = {'million':1e6,'thousand':1e3,'trillion':1e12,'billion':1e9}
                try:
                        mantissa,mag = re.search(u'[0-9\.,]+ \w+',country[key]).group(0).split()
                        mantissa  = float(re.sub(u',',u'',mantissa))
                        gdpval = float(mantissa)*w2n[mag]
                except: gdpval = None
        elif pop =='pc':
                try:
                        gdpval = re.search(u'[0-9\.,]+',country[key]).group(0)
                        gdpval = float(re.sub(u',',u'',gdpval))
                except: gdpval = None
        return gdpval


#return list of  languages found in Official languages row, if possible.
#else return [None]
def languages(country):
        try:
                langstring = country[u'language(s)']
                langstring = re.sub(u'\s*(\n|,)\s*',u'\n',langstring)
                languages =  re.findall(u'[^\n,]+',langstring)
        except:
                languages =  []
        return languages



