Code to create and query a database containing country data
==============================================================

The code in this repository is divided into three parts:  
1. downloading info table html from the Wikipedia pages of countries found at
https://en.wikipedia.org/wiki/List_of_sovereign_states
2. extracting country data from the downloaded html tables and saving it
into a pickle file as a list of dictionaries  
where each dictionary corresponds to information about one country
3. Using a dbConnection and dbCursor class to create, modify, and query a database
using the pickle file

### Requirements
This code is run using Python 2.7.12 and requires installing the following modules:  
BeautifulSoup 4 (tested using version 4.4.1)  
Matplotlib (tested using version 2.0.2)  

### Directory Description
CountryDatabase.py: contains the cdbConnection class and cdbCursor class which inherit
methods from sqlite3 Connection and Cursor classes and define additional methods to 
create and interact with databases containing country data. Information on the structure 
of the database can be found in this file.

CountryStats.py: Creates an in memory country database using cdbConnection and cdbCursor classes.
Queries database to retrieve country's area in square mi and square km and uses these values to 
estimate conversion factor from sq km to sq mi (using least squares regression through origin).
queries database to find the 8 languages which are most often an official language of a country.
creates plot of  sq km vs sq mi and plots regression line and a bar plot of top 8 languages vs number of 
countries where they are an official language. 


WikiScrape: Folder containing Python scripts to download html tables from Wikipedia
and extract data from the tables.


WikiScrape/raw_html: Empty folder. Will contain files obtained by running WikiTables.py


WikiScrape/extract.py: Contains methods to clean up and extract data obtained
from WikiTables.py; imported into TableParse.py 


WikiScrape/WikiTables.py: Downloads country info table using links for each country 
found in https://en.wikipedia.org/wiki/List_of_sovereign_states and saves the resulting 
html as a file with the name of the country in folder raw_html.


WikiScrape/TableParse.py: Parses html files in raw_html to obtain country data.
creates a list of dictionaries where each dictionary contains a country's data
and saves the list to Countrydata.pickle in main directory


### Executing code
move to WikiScrape directory  
Execute WikiScrape/WikiTables.py  
Execute WikiScrape/TableParse.py  
move to the main project directory  
Execute CountryStats.py 










