from eksiapi import *
import eksiapi
from notion.client import NotionClient
from notion.block import TextBlock
from notion.block import ToggleBlock
import random
from settings import *

def sayfayiTemizle(page):
    for block in page.children:
        block.remove()

ben = Suser(cookies, headers, kullanici_adi)

#favladığım entryler. array of objects
favladiklarim_objarr = ben.favladiklari()


favladiklarimiFavlayanlar_objarr = [obj.favlayanlar() for obj in favladiklarim_objarr]
# entry objelerinde oluşan 2D list 
favladiklarimiFavlayanlarinFavladiklari_objarr = [f.favladiklari() for sub in favladiklarimiFavlayanlar_objarr for f in sub]
favladiklarimiFavlayanlarinFavladiklari = [e for sub in favladiklarimiFavlayanlarinFavladiklari_objarr for e in sub]
# entry objelerinin listesini karıştır
random.shuffle(favladiklarimiFavlayanlarinFavladiklari)
# ilk 50 entry objesini al
favladiklarimiFavlayanlarinFavladiklari = favladiklarimiFavlayanlarinFavladiklari[:100]

# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in session on Notion.so
client = NotionClient(token_v2=notion_token)

# Replace this URL with the URL of the page you want to edit
page = client.get_block("https://www.notion.so/mutlucan/Favlad-klar-m-favlayanlar-n-favlad-klar-0890092c2d504b318df6237856379b87")

# Halihazırda Notion sayfasında varolan etryleri siler.
sayfayiTemizle(page)

for entry_obj in favladiklarimiFavlayanlarinFavladiklari:
    entry_link = "https://eksisozluk.com/entry/{id}".format(id=entry_obj.entryId)
    entry_topic = entry_obj.get_topic()
    entry_content = entry_obj.get_content() + "\n" + entry_link + "\n" + "fav sayısı=" + str(entry_obj.get_favorites_count())
    
    new_topic = page.children.add_new(ToggleBlock, title=entry_topic)
    new_content = new_topic.children.add_new(TextBlock, title=entry_content)
    print(new_content)

