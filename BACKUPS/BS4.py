import requests
from bs4 import BeautifulSoup as bs
import lxml


def get_data(month):
    r = requests.get("http://www.greenlanemasjid.org/prayer-times/%s-2017/" %month)
    soup = bs(r.text, "lxml")
    dateandtimes = [i.string for i in soup.select("[class~=p-prayer-table-row__cell]")][12:]

    k = 0
    daylist = []
    for i in range(int((len(dateandtimes)/12))):
        daylist.append(dateandtimes[k:(k+12)])
        k += 12
    
    return daylist


print(get_data("January"))
print("fin")