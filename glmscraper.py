import requests
from bs4 import BeautifulSoup
import lxml

def main():
    r = requests.get("http://www.greenlanemasjid.org/prayer-times/november-2017/")

    soup = BeautifulSoup(str(r.text), "lxml")
    dirtydata = soup.find_all('ol')
    dirtydata = spring_clean(dirtydata)

    soup = BeautifulSoup(dirtydata, "lxml")
    dateandtimes = []
    for i in soup.select("[class~=p-prayer-table-row__cell]"):
        dateandtimes.append(i.string)

    daylist = []
    k=0
    for i in range(int((len(dateandtimes)/12))):
        x= (dateandtimes[k:(k+12)])
        daylist.append(x)
        k+=12
    
    print(daylist)

def spring_clean(offender):
    offender = str(offender)[1:-1]
    return offender

main()