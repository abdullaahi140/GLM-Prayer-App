import requests
from bs4 import BeautifulSoup
import lxml

def main():
    r = requests.get("http://www.greenlanemasjid.org/prayer-times/november-2017/")

    soup = BeautifulSoup(str(r.text), "lxml")
    dirtydata = soup.find_all('ol')
    dirtydata = spring_clean(dirtydata)

    soup = BeautifulSoup(dirtydata, "html.parser")
    print(soup.li["class"])

    dateandtimes = []
    for i in soup.select("[class~=p-prayer-table-row__cell]"):
        dateandtimes.append(i.string)
    print(dateandtimes)

    days = soup.select("[class~=p-prayer-table-row__cell--day]")

    
    #<ol class="p-prayer-table-row" prayer-date="31-10-2017">
    
    """
    f2 = open("dirty-output.html","r")
    tempdirtydata = f2.read()

    cleandata = tempdirtydata.prettify()
        
    print (cleandata)

    f3 = open("scrape-output.html","w")
    f3.write(i)
    f3.close()
    """
    print ("Finished")

def spring_clean(offender):
    offender = str(offender)[1:-1]
    return offender

main()