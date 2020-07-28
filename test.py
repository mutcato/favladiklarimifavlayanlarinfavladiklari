class User:
    def __init__(self, userNames):
        """
        param: {"a":cookies}
        param: {headers}
        param: [userNames] list of strings
        """
        self.userNames = userNames

    def favoritedPosts(self):
        """
        return: [{post}], favladığı entryleri döndürür
        """
        result = []
        for userName in self.userNames:
            posts = [{"id":"111", "topic": "topic 1", "content": "content 1"},{"id":"112", "topic": "topic 2", "content": "content 2"},{"id":"113", "topic": "topic 3", "content": "content 3"}]

            for t in posts:
                entry = Entry(t["id"])
                result.append(entry)
        return result

    def favladiklariniFavlayanlar(self):
        """
        param: [{entries}] array of object
        return [ids]
        """
        favsifavs = []
        favs = self.favladiklari()
        for entry in favs: favsifavs = favsifavs + favlayan(entry["id"])
        # To make the list contains only unique values convert to set then convert back to list
        return list(set(favladiklarimiFavlayanlar))

class Entry:
    def __init__(self, entryIds):
        """
        param: {"a":cookies}
        param: {headers}
        param: [entryIds] list of integers
        """
        self.entryIds = entryIds
        self.topic = self.get_topic()

    def favlayanlar(self):
        """
        param: int, entry id alır.
        return: [string] list of users, favlayanların usernamelerini döndürür. (Çaylaklar hariç)
        """
        susers = []
        for entryId in self.entryIds:
            url = "https://eksisozluk.com/entry/favorileyenler?entryId={entryId}".format(entryId=str(entryId))
            response = requests.get(url, cookies=self.cookies, headers=self.headers)
            webpage = response.text
            soup = BeautifulSoup(webpage, "html.parser")
            susers = susers + [li.find("a").get('href').replace("/biri/","") for li in soup.find_all("li")][:-1]
        return susers

    def get_topic(self):
        return "topic of post with id "+self.entryIds

user = User("comolokko")
print(user.favoritedPost()[0].topic)