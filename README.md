Code to create and query a database containing country data
==============================================================

The code in this repository is divided into three parts:
1. download info table html from the Wikipedia pages of countries found at
https://en.wikipedia.org/wiki/List_of_sovereign_states
2. extracting country data from the downloaded html tables and saving it
into a pickle file as a list of dictionaries where each dictionary corresponds to
information about one country
3. Using a dbConnection and dbCursor class to create, modify, and query a database
using the pickle file

