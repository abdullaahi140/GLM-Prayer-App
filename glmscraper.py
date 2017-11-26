import requests
from bs4 import BeautifulSoup as bs 
import lxml
import sqlite3

class Timetable():

    def main():
        r = requests.get("http://www.greenlanemasjid.org/prayer-times/november-2017/")
        soup = bs(str(r.text), "lxml")
        dirtydata = soup.find_all('ol')
        dirtydata = Timetable.spring_clean(dirtydata)

        soup = bs(dirtydata, "lxml")
        dateandtimes = []
        for i in soup.select("[class~=p-prayer-table-row__cell]"):
            dateandtimes.append(i.string)

        daylist = []
        k=0
        for i in range(int((len(dateandtimes)/12))):
            daylist.append(dateandtimes[k:(k+12)])
            k+=12

        Timetable.create_database(daylist)

    def spring_clean(offender):
        offender = str(offender)[1:-1]
        return offender

    def create_database(dtlist):
        conn = sqlite3.connect("timetable.db") 
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS October(Day TEXT, FajrStart TEXT, FajrJamat TEXT, Sunrise TEXT, DhuhrStart TEXT, DhuhrJamat TEXT, AsrStart TEXT, AsrJamat TEXT, Maghrib TEXT, IshaStart TEXT, IshaJamat TEXT)")

        for i in dtlist:
            c.execute("INSERT INTO October (Day, FajrStart, FajrJamat, Sunrise, DhuhrStart, DhuhrJamat, AsrStart, AsrJamat, Maghrib, IshaStart, IshaJamat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10]))
        conn.commit()

if __name__ == '__main__':
    Timetable.main()

print("Finished")