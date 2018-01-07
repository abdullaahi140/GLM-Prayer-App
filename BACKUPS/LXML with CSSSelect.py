import requests
import datetime
from lxml import html, cssselect

def get_data(month):
    r = requests.get("http://www.greenlanemasjid.org/prayer-times/%s/" %(month[:-4]+"-"+month[-4:]))
    tree = html.fromstring(r.content)
    dateandtimes = [i.text for i in tree.cssselect("li.p-prayer-table-row")] 

    k = 0
    daylist = []
    for i in range((len(dateandtimes)/12)):
        daylist.append(dateandtimes[k:(k+12)])
        k += 12

    return daylist

print(get_data("December2017"))
print("Finished")