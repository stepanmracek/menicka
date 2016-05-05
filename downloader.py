import datetime
from bs4 import BeautifulSoup
import urllib.request


class DownloaderBase(object):
    """docstring for DownloaderBase"""

    def __init__(self):
        super(DownloaderBase, self).__init__()

    def pipe(self):
        downloadContent = self.download()
        soup = self.parse(downloadContent)
        weekSoup = self.getWeekMenuContent(soup)
        menu = self.getTodayMenu(weekSoup, self.getWeekDay())
        return menu

    def download(self):
        agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0'
        request = urllib.request.Request(self.getUrl(), data=None, headers={
            'User-Agent': agent
            })
        response = urllib.request.urlopen(request)
        return response.read()

    def parse(self, downloadContent):
        soup = BeautifulSoup(downloadContent, "lxml")
        return soup

    def getName(self):
        raise "Abstract method called"

    def getUrl(self):
        raise "Abstract method called"

    def getWeekMenuContent(self, soup):
        raise "Abstract method called"

    def getTodayMenuContent(self, weekSoup, weekDay):
        raise "Abstract method called"

    def getWeekDay(self):
        return datetime.datetime.now().weekday()


class KlubCestovatelu(DownloaderBase):
    def __init__(self):
        super(KlubCestovatelu, self).__init__()

    def getName(self):
        return "Klub cestovatelů"

    def getUrl(self):
        return "http://www.hedvabnastezka.cz/klub-cestovatelu-brno/poledni-menu-2/"

    def getWeekMenuContent(self, soup):
        return soup.findAll("div", {"class": "article-content"})[0]

    def getTodayMenu(self, weekSoup, weekDay):
        today = weekSoup.findAll("p")[weekDay]
        items = today.findAll("strong")

        soupName = items[1].string[0] + items[1].string[1:].lower()
        meals = [items[i].string[3:] for i in range(2, 5)]
        mealDescriptions = [items[i].next_sibling[2:] for i in range(2, 5)]

        return {
            "soup": soupName,
            "meals": [{
                "name": meals[0],
                "description": mealDescriptions[0],
                "price": 89
            }, {
                "name": meals[1],
                "description": mealDescriptions[1],
                "price": 95
            }, {
                "name": meals[2],
                "description": mealDescriptions[2],
                "price": 99
            }]
        }


class Racek(DownloaderBase):
    def __init__(self):
        super(Racek, self).__init__()

    def getName(self):
        return "Racek"

    def getUrl(self):
        return "http://www.restaurace-racek.cz/sluzby/denni-menu/"

    def getWeekMenuContent(self, soup):
        return soup.findAll("tbody")[0]

    def getTodayMenu(self, weekSoup, weekDay):
        items = weekSoup.findAll("tr")
        startIndex = 5 + weekDay * 9

        soupName = items[startIndex].findAll("td")[1].strong.string
        mealIndicies = [startIndex + i for i in range(2, 6)]
        meals = [items[i].findAll("td")[1].strong.string for i in mealIndicies]

        return {
            "soup": soupName,
            "meals": [{
                "name": meals[0],
                "description": "",
                "price": 79
            }, {
                "name": meals[1],
                "description": "",
                "price": 84
            }, {
                "name": meals[2],
                "description": "",
                "price": 106
            }, {
                "name": meals[3],
                "description": "",
                "price": 140
            }]
        }


class KralovskaCesta(DownloaderBase):
    def __init__(self):
        super(KralovskaCesta, self).__init__()

    def getName(self):
        return "Královská cesta"

    def getUrl(self):
        return "http://www.kralovskacesta.com/"

    def getWeekMenuContent(self, soup):
        return soup.findAll("div", {"class": "denni-menu"})[0]

    def getTodayMenu(self, weekSoup, weekDay):
        items = weekSoup.findAll("li")
        soupName = items[0].string[9:]
        mealIndicies = [1, 2, 3, 4, 5]
        meals = [items[i].span.text[3:] for i in mealIndicies]

        pricesItems = weekSoup.findAll("span", {"class": "cena-jidla"})
        prices = [int(p.string.split(' ')[0]) for p in pricesItems]

        return {
            "soup": soupName,
            "meals": [{
                "name": m[0],
                "description": "",
                "price": m[1]
            } for m in zip(meals, prices)]
        }


def getMenus():
    restaurants = [KlubCestovatelu(), Racek(), KralovskaCesta()]
    return[{"name": r.getName(), "menu": r.pipe()} for r in restaurants]

if __name__ == '__main__':
    print(getMenus())
