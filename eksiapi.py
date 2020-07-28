import random
import requests
import json
from bs4 import BeautifulSoup


class Suser:
    def __init__(self, cookies, headers, userName):
        """
        param: {"a":cookies}
        param: {headers}
        param: [userNames] list of strings
        """
        self.cookies = cookies
        self.headers = headers
        self.userName = userName

    def favladiklari(self):
        """
        param: userName -> string, ekşi kullanıcı adını alır
        return: list, favladığı entryleri döndürür
        """
        result = []
        url = "https://eksisozluk.com/favori-entryleri?nick={userName}&p=1".format(userName=self.userName)
        response = requests.get(url, cookies=self.cookies, headers=self.headers)
        webpage = response.text
        soup = BeautifulSoup(webpage, "html.parser")
        topic_items = soup.find_all("div", attrs={"class": "topic-item"})

        for t in topic_items:
            e_id = t.find("a", attrs={"class": "permalink"}).get("href").replace("/entry/", "")
            entry = Entry(self.cookies, self.headers, e_id)
            result.append(entry)
        return result


class Entry:
    def __init__(self, cookies, headers, entryId):
        """
        param: {"a":cookies}
        param: {headers}
        param: [entryIds] list of integers
        """
        self.cookies = cookies
        self.headers = headers
        self.entryId = entryId
        self.url = "https://eksisozluk.com/entry/"+str(self.entryId)
        self.topic = "TOPPIC"

    def favlayanlar(self):
        """
        param: int, entry id alır.
        return: [string] list of users, favlayanların usernamelerini döndürür. (Çaylaklar hariç)
        """
        _url = "https://eksisozluk.com/entry/favorileyenler?entryId={entryId}".format(entryId=str(self.entryId))
        soup = self._get_html(_url)
        suser_names = [li.find("a").get('href').replace("/biri/", "") for li in soup.find_all("li")][:-1]
        susers = [Suser(self.cookies, self.headers, s_name) for s_name in suser_names]
        return susers

    def _get_html(self, url):
        response = requests.get(url, cookies=self.cookies, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_topic(self):
        soup = self._get_html(self.url)
        return soup.find("h1").find("a").get_text().strip()

    def get_content(self):
        soup = self._get_html(self.url)
        return soup.find("ul", attrs={"id": "entry-item-list"}).find("li").find("div", attrs={"class": "content"}).get_text().strip()
        
    def get_favorites_count(self):
        soup = self._get_html(self.url)
        return int(soup.find("ul", attrs={"id": "entry-item-list"}).find("li").get("data-favorite-count"))


def favFavFav(usernames, num, order_by=None):
    """
    param: list [usernames]
    param: int, num -> toplam entrylerden ilk kaç tanesini döndürecek
    param: string, order_by -> ASC, DESC, none. Default none
    return: list of dictionaries [{id,topic,content}]
    Kullanıcı isimlerini alır favladıkları entryleri döndürür
    """
    result = []
    for user in usernames:
        result = result + favladiklari(user)

    if order_by == "ASC":
        result = sorted(result, key=lambda result: result["favorite_count"])
    elif order_by == "DESC":
        result = sorted(result, key=lambda result: result["favorite_count"], reverse=True)
    else:
        random.shuffle(result)
    return result[num:]

