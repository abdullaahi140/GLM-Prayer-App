import requests
from lxml import html
import sqlite3
import datetime


class Database():

    def get_data(month):
        r = requests.get("http://www.greenlanemasjid.org/prayer-times/%s/" %(month[:-4]+"-"+month[-4:]))
        tree = html.fromstring(r.text)
        prayertimes = [i.text for i in tree.cssselect("li.p-prayer-table-row__cell")]

        k = 0
        ptlist = []
        for i in range(int((len(prayertimes)/12))):
            ptlist.append(prayertimes[k:(k+12)])
            k += 12
        Database.create_database(ptlist,month=month)

    def create_database(ptlist,month):
        conn = sqlite3.connect("timetable.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS %s (Day TEXT, Date TEXT, FajrStart TEXT, FajrJamat TEXT, Sunrise TEXT, DhuhrStart TEXT, DhuhrJamat TEXT, AsrStart TEXT, AsrJamat TEXT, Maghrib TEXT, IshaStart TEXT, IshaJamat TEXT)" %month)
        for i in ptlist:
            c.execute("INSERT INTO %s (Day, Date, FajrStart, FajrJamat, Sunrise, DhuhrStart, DhuhrJamat, AsrStart, AsrJamat, Maghrib, IshaStart, IshaJamat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" %month, (i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11]))
            conn.commit()
        conn.close()


class dateData():

    def dt_grab_prayer_times(date,dateincrement=0,twelve=True,twofour=None):
        date = date + datetime.timedelta(days=dateincrement)
        day = date.strftime("%#d")
        month = date.strftime("%B%Y")
        tt = dateData.grab_prayer_times(day,month,twelve=twelve,twofour=twofour)
        return tt, date, day, month

    def grab_prayer_times(day,month,twelve=None,twofour=None):
        conn = sqlite3.connect("timetable.db")
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM %s WHERE ROWID = ?" %month, [day])
        except sqlite3.OperationalError:
            Database.get_data(month)
            c.execute("SELECT * FROM %s WHERE ROWID = ?" %month, [day])
        try:
            tt_list = dateData.am_or_pm(list(c.fetchone()),twelve=twelve,twofour=twofour)
        except TypeError:
            tt_list = None
        conn.close()
        return tt_list

    def dt_tt(tt,day="",month="",twelve=True,twofour=None,hourformat="%I:%M%p",yearformat=""):  
        tt = tt[:2] + [datetime.datetime.strptime(i+day+month, hourformat+yearformat) for i in tt[2:]]
        return tt

    def am_or_pm(tt,twelve=None,twofour=None,hourformat="%I:%M%p"):
        if twelve is True:
            strfformat = "%I:%M %p"
        if twofour is True:
            strfformat = "%H:%M"

        tt = dateData.dt_tt(tt,twelve=twelve,twofour=twofour,hourformat=hourformat)
        tt = tt[:2] + [datetime.datetime.strftime(i, strfformat) for i in tt[2:]]
        return tt


if __name__ == '__main__':
    print (dateData.dt_grab_prayer_times(datetime.datetime.today(),0,True,None)[0])
    # print(dateData.grab_prayer_times("26","November2017",twofour=True))
