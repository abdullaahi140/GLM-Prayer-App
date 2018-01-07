import requests
import datetime
from lxml import html

def get_data(month):
    r = requests.get("http://www.greenlanemasjid.org/prayer-times/%s/" %(month[:-4]+"-"+datetime.date.today().strftime("%Y")))
    tree = html.fromstring(r.content)
    dateandtimes = tree.xpath("//ol/li/text()")
    
    k = 0
    daylist = []
    for i in range(int((len(dateandtimes)/12))):
        daylist.append(dateandtimes[k:(k+12)])
        k += 12

    return daylist

print(get_data("january2018"))
print("fin")