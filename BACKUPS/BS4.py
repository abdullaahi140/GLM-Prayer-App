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