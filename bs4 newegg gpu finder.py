#finding in stock products on websites. for this example, graphics card on Newegg
#prints out price, name, and link of all products from search
from bs4 import BeautifulSoup
import requests
import re

search_term = input("What product do you want to search for?: ")

url = f"https://www.newegg.com/p/pl?d={search_term}&N=413"
page = requests.get(url).text
doc = BeautifulSoup(page,"html.parser")


#page changes url
page_text = doc.find(class_="list-tool-pagination-text").strong
print(page_text,end="\n\n")

#grab the total # of pages - turn results into string, split string, find what is on right side of slash, split string again, grab the 4
pages_v1 = str(page_text).split("/")[-2]
print(pages_v1,end="\n\n")

pages_v2=pages_v1.split(">")
print(pages_v2,end="\n\n")

pages_v3=pages_v2[-1][:1]
print (pages_v3,end="\n\n")

pages = int(pages_v3)

items_found = {}

for page in range(1, pages+1):
    url = f"https://www.newegg.com/p/pl?d={search_term}&N=413&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page,"html.parser")
    
    #limit html return to subdivider in Inspect that is only for search results. otherwise will retrieve things like search bar
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")


#grab items that say 3080. not all of them are. create filter
    items = div.find_all(text=re.compile(search_term)) #re allows matches any text that contains search term, extra characters are okay.
    for item in items:
        print(item,end="\n\n")
    
    print("\n"*3)

#look at parent of text to find link for this particular website
    for item in items:
        parent = item.parent
        if parent.name != "a": #remvoes None and all results that dont fit
            continue

        else:
            link = parent['href'] #href tag
#            print(link)

        #find parent of parent to get item-container to find all relevant info in product
            next_parent = item.find_parent(class_="item-container") #locate a specific parent

            try:
                price = next_parent.find(class_="price-current").find("strong").string
                items_found[item] = {"price": int(price.replace(",","")),"link": link}
            except:
                pass


print(f"\n\n{items_found}\n\n")

#sorting a dictionary. covert to list then back to dictionary
sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price']) #gives tuple. sorting by price in dictionary

for item in sorted_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("----------------------")
