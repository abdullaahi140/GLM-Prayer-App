import requests
from bs4 import BeautifulSoup as bs
import lxml
import sqlite3
import datetime


class Database():

    def get_data(month):
        r = requests.get("http://www.greenlanemasjid.org/prayer-times/%s-2017/" %month)
        soup = bs(str(r.text), "lxml")
        dirtydata = soup.find_all('ol')
        dirtydata = Database.spring_clean(dirtydata)

        soup = bs(dirtydata, "lxml")
        dateandtimes = []
        for i in soup.select("[class~=p-prayer-table-row__cell]"):
            dateandtimes.append(i.string)

        k = 0
        daylist = []
        for i in range(int((len(dateandtimes)/12))):
            daylist.append(dateandtimes[k:(k+12)])
            k += 12
        Database.create_database(daylist,month=month)

    def spring_clean(offender):
        offender = str(offender)[1:-1]
        return offender

    def create_database(dtlist,month):
        conn = sqlite3.connect("timetable.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS %s(Day TEXT, Date TEXT, FajrStart TEXT, FajrJamat TEXT, Sunrise TEXT, DhuhrStart TEXT, DhuhrJamat TEXT, AsrStart TEXT, AsrJamat TEXT, Maghrib TEXT, IshaStart TEXT, IshaJamat TEXT)" %month)

        for i in dtlist:
            c.execute("INSERT INTO %s (Day, Date, FajrStart, FajrJamat, Sunrise, DhuhrStart, DhuhrJamat, AsrStart, AsrJamat, Maghrib, IshaStart, IshaJamat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" %month,
                            (i[0], (i[1][:-2]), i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11]))
        conn.commit()
        conn.close()


class todaysDate():

    def today():
        date = datetime.date.today().strftime("%#d")
        month = datetime.date.today().strftime("%B")
        return todaysDate.currentdaydata(date,month)

    def currentdaydata(date,month):
        conn = sqlite3.connect("timetable.db")
        c = conn.cursor()
        c.execute("SELECT * FROM %s WHERE Date = ?" %month, (date))
        return c.fetchone()


if __name__ == '__main__':
    Database.get_data("November")
    print(todaysDate.today())
    print("Finished")