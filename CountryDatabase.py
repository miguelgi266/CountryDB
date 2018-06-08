import sqlite3,cPickle



#Adds functionality to sqlite3.Connection class to 
#connect to a database containing country information
#structured as in create_tables method in cdbConnection class

#Also helps construct new database from data 
#(given as list of dictionaries with the following structure:
#{u'name':unicode, u'currency':unicode/None, u'area_km2':float/None,u'area_mi2':float/None,u'tot_GDP_nom':float/None,
#u'pc_GDP_nom':float/None,u'tot_GDP_PPP':float/None,pc_GDP_PPP:float/None,u'language(s)':list of unicode/[]}
class cdbConnection(sqlite3.Connection):	
	#initialize connection to database, if database is empty,
	#it will populate it with values in country_list
	#if country_list is empty and database is empty, connection will exit
	def __init__(self,db_loc,country_list = None):
		super(cdbConnection,self).__init__(db_loc)#,factory = Countrydb)
		if self.is_new_db():
			self.create_tables()
			self.populate_tables(country_list)
		else:
			msg = u'{} is not empty'.format(db_loc)
                	msg += u'\ncannot initialize an existing database with country_list'
                	msg += u'\nconnection will close'
			assert country_list not in {None,[]}, msg

	#define cursor using class 'dbCursor'
	def cursor(self):
		return  super(cdbConnection,self).cursor(cdbCursor)
	#Checks if database is new 

	#Tests whether database is an empty file/ empty memory database
	def is_new_db(self):
		cur = self.cursor()
		cur.execute(u'''SELECT COUNT(1) FROM sqlite_master WHERE TYPE = "table"''')
		num_tables = cur.fetchone()[0]
		cur.close()
		if num_tables == 0:
			return True
		else:
			return False
	#creates tables CountryData, CountryLanguages, and LangTable if database is new
	def create_tables(self):
		cur = self.cursor()
		cur.execute(u"""CREATE TABLE CountryData(
                Name TEXT NOT NULL, Currency TEXT, `Area (in sq km)` Real, `Area (in sq mi)` Real, `total GDP (nom)` Real, 
                `per capita GDP (nom)` Real,`total GDP (PPP)` Real, `per capita GDP (PPP)` Real, UNIQUE(Name))""")
		cur.execute(u"CREATE TABLE CountryLanguages(Country TEXT NOT NULL, Language TEXT NOT NULL, UNIQUE(Country,Language))")
		cur.execute(u"CREATE TABLE LangTable( Language TEXT NOT NULL, UNIQUE(Language))")	
		self.commit()
		cur.close()
	#adds countries in country_list to database
	#meant to be used as part of __init__
	def populate_tables(self,country_list):
		cur = self.cursor()
		for cdat in country_list:
			cur.addCountryInfo(cdat)
			self.commit()
		cur.close()



class cdbCursor(sqlite3.Cursor):
	#adds information about a new country (given as dictionary cdat into  database)
	#updates tables accourdingly
	def addCountryInfo(self,cdat):
		self.inspect_data(cdat)
		if self.in_db(cdat[u'name']) == True:
			print u"{} is already in database".format(cdat['name'])
			print u"At this moment, updating a country's info must be done using dbCursor.execute method"
		else:		
			self.execute(u"""INSERT INTO CountryData VALUES
			(:name ,:currency, :area_km2, :area_mi2, :tot_GDP_nom, :pc_GDP_nom,:tot_GDP_PPP,:pc_GDP_PPP)
			""",cdat)
			for lang in cdat[u'language(s)']:
				self.execute(u'INSERT INTO CountryLanguages VALUES(?,?)',(cdat[u'name'],lang))
				self.execute(u"""INSERT OR IGNORE INTO LangTable  VALUES (?) """,(lang,))
	#removes country data from database (if it exists), performing necessary updates to tables
	#input should be country name, if country is not in database, no change will take place
	def delCountryInfo(self,cName):
		self.execute(u"DELETE FROM CountryData WHERE Name = ?",(cName,))
		self.execute(u"DELETE FROM CountryLanguages WHERE Country = ?",(cName,))
		self.execute(u"""DELETE FROM LangTable WHERE 
		NOT EXISTS (SELECT * FROM CountryLanguages WHERE Language = LangTable.Language)""")

	#NOT YET IMPLEMENTED, updates database with the information of a country 
	#with name cdat['name'] calls addCountryInfo if country is not in database
	def updateCountryInfo(self,cdat):
		if self.in_db(cdat[u'name']):
			print 'update functionality needs to be added'
		else:
			self.addcountryInfo(cdat)

        #checks if country is already in database, country name should be given as (unicode) string
        def in_db(self,country_name):
                self.execute(u"SELECT COUNT(1) FROM CountryData WHERE Name = ?",(country_name,))
                return False if self.fetchone()[0] == 0 else True
 	#makes sure data is given as a dictionary and dictionary contains correct keys
        @classmethod
        def inspect_data(cls,cdat):
                assert type(cdat) == dict, u"country data must be dictionary"
                req_k = {u'name',u'currency',u'area_km2',u'area_mi2',
		u'tot_GDP_nom',u'pc_GDP_nom',u'tot_GDP_PPP',u'pc_GDP_PPP'}
                key_diff = req_k - set(cdat.keys())
                assert key_diff == set(), u"Country data dictionaries must include appropriate keys"


