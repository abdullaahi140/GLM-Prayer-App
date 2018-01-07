import requests
from lxml import html
import sqlite3
import datetime


class Database():

    def get_data(month):
        r = requests.get("http://www.greenlanemasjid.org/prayer-times/%s/" %(month[:-4]+"-"+month[-4:]))
        tree = html.fromstring(r.text)
        dateandtimes = [i.text for i in tree.cssselect("li.p-prayer-table-row__cell")]

        k = 0
        daylist = []
        for i in range(int((len(dateandtimes)/12))):
            daylist.append(dateandtimes[k:(k+12)])
            k += 12
        Database.create_database(daylist,month=month)

    def create_database(dtlist,month):
        conn = sqlite3.connect("timetable.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS %s (Day TEXT, Date TEXT, FajrStart TEXT, FajrJamat TEXT, Sunrise TEXT, DhuhrStart TEXT, DhuhrJamat TEXT, AsrStart TEXT, AsrJamat TEXT, Maghrib TEXT, IshaStart TEXT, IshaJamat TEXT)" %month)
        for i in dtlist:
            c.execute("INSERT INTO %s (Day, Date, FajrStart, FajrJamat, Sunrise, DhuhrStart, DhuhrJamat, AsrStart, AsrJamat, Maghrib, IshaStart, IshaJamat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" %month, (i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9],i[10],i[11]))
            conn.commit()
        conn.close()


class dateData():

    def today():
        date = datetime.date.today().strftime("%#d")
        month = datetime.date.today().strftime("%B%Y")
        return dateData.currentdaydata(date,month)

    def currentdaydata(date,month):
        conn = sqlite3.connect("timetable.db")
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM %s WHERE ROWID = ?" %month, [date])
        except sqlite3.OperationalError:
            Database.get_data(month)
            c.execute("SELECT * FROM %s WHERE ROWID = ?" %month, [date])
        tt_list = c.fetchone()
        conn.close()
        return tt_list


if __name__ == '__main__':

    Database.get_data("January2018")
    print(dateData.today())
    print("Finished")
