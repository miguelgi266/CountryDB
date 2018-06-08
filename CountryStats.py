import cPickle
import numpy as np
import matplotlib.pyplot as plt
from CountryDatabase import cdbConnection, cdbCursor

#(0,0)-intercept fit
def origin_linregress(a,b):
        A = np.vstack([a,np.zeros(len(a))]).T
        return np.linalg.lstsq(A,b)[0][0]


with open('CountryData.pickle','rb') as f:
	country_list = cPickle.load(f)

#establish connection to database
conn = cdbConnection(':memory:',country_list)
cur = conn.cursor()

#with area data from countries estimate 
#km^2 to mi^2 conversion factor using linear regression through origin

#retrieve data performing sql query with inherited execute method
cur.execute("SELECT `area (in sq km)`,`area (in sq mi)` FROM CountryData")
area_dat = cur.fetchall()
x_area,y_area = map(np.array,zip(*area_dat))

print 'Estimating km^2 to mi^2 conversion factor'
exact = 0.386102
cf = origin_linregress(x_area,y_area)
print 'Exact conversion factor: {}'.format(exact)
print 'Estimated conversion factor from data: {:.6f}'.format(cf)
print 'Correct to 3 significant digits present in the data'


#Get sorted list of top 8 Languages 
#with official status and plot in bar chart
cur.execute("""SELECT Language, COUNT(*) FROM CountryLanguages 
WHERE Language NOT IN ('None','None at Federal Level')
GROUP BY Language ORDER BY Count(*) DESC LIMIT 8""")
OLC = cur.fetchall()
langname,numctr = zip(*OLC)
#close connection to database now that we have retrieved necessary info
cur.close()
conn.close()


#plot data and regression for area data
plt.figure(1)
plt.title('square kilometers vs square miles' )
plt.xlabel('area in (sq km)')
plt.ylabel('area in (sq mi)')
plt.plot(x_area,y_area,'o',color = 'black',label = 'datapoint')
plt.plot(x_area,cf*x_area,'r',color = 'purple',label = 'regression line')
eq = r'Equation: y = ${0:.3g}x$'.format(cf)
plt.text(1, 0,eq, ha ='right',va='bottom',transform = plt.gca().transAxes)
plt.legend()
plt.tight_layout()


#create bar chart of 8 most common official languages
plt.figure(2)
plt.bar(range(8),numctr)
plt.xticks(range(8),langname, fontsize = 8)
plt.title('Languages by number of countries with official status' )
plt.xlabel('Countries')

for i in range(8):
    plt.text(i,numctr[i], str(numctr[i]))

plt.figure(1)
plt.tight_layout()
plt.show()
