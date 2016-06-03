#! /usr/bin/env python3

import re
import datetime
from bs4 import BeautifulSoup
import urllib.request


def dayNumberToName(number):
    dayNames = {
        0: "pondělí",
        1: "úterý",
        2: "středa",
        3: "čtvrtek",
        4: "pátek",
        5: "sobota",
        6: "neděle"
    }
    return dayNames[number]


class DownloaderBase(object):
    """docstring for DownloaderBase"""

    def __init__(self):
        super(DownloaderBase, self).__init__()

    def pipe(self):
        #try:
            downloadContent = self.download()
            soup = self.parse(downloadContent)
            weekSoup = self.getWeekMenuContent(soup)
            menu = self.getTodayMenu(weekSoup, self.getWeekDay())
            return menu
        #except:
            return {
                "soup": "",
                "meals": []
            }

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

    def getLogo(self):
        return ""

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
        return soup.find("div", {"class": "article-content"})

    def getTodayMenu(self, weekSoup, weekDay):
        items = weekSoup.findAll("p")
        startIndex = -1
        for i in range(len(items)):
            if dayNumberToName(weekDay) in items[i].text.lower():
                startIndex = i

        if startIndex == -1:
            raise "menu data for given day %d not available" % weekDay

        items = items[startIndex:]
        soupName = items[1].string[0] + items[1].string[1:].lower()
        meals = [items[i].find("strong").text[3:] for i in range(2, 5)]
        mealDescriptions = [items[i].find("strong").next_sibling.string for i in range(2, 5)]

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

    def getLogo(self):
        return "klub_cestovatelu.png"


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

        startIndex = -1
        for i in range(len(items)):
            if dayNumberToName(weekDay) in items[i].findAll("td")[1].text.lower():
                startIndex = i

        if startIndex == -1:
            raise "menu data for given day %d not available" % weekDay

        items = items[startIndex:]
        soupName = items[2].findAll("td")[1].text
        meals = [items[i].findAll("td")[1].text for i in range(4, 8)]

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

    def getLogo(self):
        return "racek.png"


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

    def getLogo(self):
        return "kralovska_cesta.png"


class Yvy(DownloaderBase):
    def __init__(self):
        super(Yvy, self).__init__()

    def getName(self):
        return "YVY"

    def getUrl(self):
        return "http://www.yvy.cz/denni-menu/"

    def getWeekMenuContent(self, soup):
        return soup.findAll("tbody")[0]

    def getTodayMenu(self, weekSoup, weekDay):
        items = weekSoup.findAll("tr")
        startIndex = weekDay * 8 + 2

        soupName = items[startIndex].findAll("td")[1].text
        r = range(startIndex + 1, startIndex + 6)
        meals = [items[i].findAll("td")[1].text for i in r]
        prices = [int(items[i].findAll("td")[3].text[:-2]) for i in r]

        return {
            "soup": soupName,
            "meals": [{
                "name": m[0],
                "description": "",
                "price": m[1]
            } for m in zip(meals, prices)]
        }

    def getLogo(self):
        return "yvy.png"


class LaBotte(DownloaderBase):
    def __init__(self):
        super(LaBotte, self).__init__()

    def getName(self):
        return "la Botte"

    def getUrl(self):
        return "https://www.zomato.com/cs/brno/pizzeria-la-botte-kr%C3%A1lovo-pole-brno-sever"

    def getWeekMenuContent(self, soup):
        return soup.findAll("div", {"class": "tmi-group"})[0]

    def removeAlergens(self, input):
        input = re.sub(r'A-(\d+,*)+', '', input)
        return input.strip()

    def getTodayMenu(self, weekSoup, weekday):
        soupName = weekSoup.find("div", {"class": "tmi-name"}).string
        soupName = soupName.strip()[9:]
        soupName = self.removeAlergens(soupName)

        meals = []
        items = weekSoup.findAll("div", {"class": "tmi-daily"})
        for i in items[1:]:
            if "hidden" in i["class"]:
                continue

            meal = i.find("div", {"class": "tmi-name"}).string.strip()[8:]
            meal = self.removeAlergens(meal)

            price = int(i.find("div", {"class": "tmi-price"}).string.strip()[:-3])
            meals.append((meal, price))

        return {
            "soup": soupName,
            "meals": [{
                "name": m[0],
                "description": "",
                "price": m[1]
            } for m in meals]
        }

    def getLogo(self):
        return "la_botte.png"


def getMenus():
    restaurants = [KlubCestovatelu(),
                   Racek(),
                   KralovskaCesta(),
                   Yvy(),
                   #LaBotte()
                   ]
    return[{"name": r.getName(),
            "url": r.getUrl(),
            "logo": r.getLogo(),
            "menu": r.pipe()
            } for r in restaurants]

if __name__ == '__main__':
    print(getMenus())
