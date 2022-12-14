import urllib.request as ul
from bs4 import BeautifulSoup as soup

url = 'https://circuit.rocks/new'
req = ul.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
client = ul.urlopen(req)
htmldata = client.read()
client.close()

pagesoup = soup(htmldata, "html.parser")
itemlocator = pagesoup.findAll('div', {"class":"product-grid-item xs-100 sm-50 md-33 lg-25 xl-20"})

filename = "new items.csv"
f = open(filename, "w", encoding="utf-8")
headers = "Item Name, Price\n"
f.write(headers)

for items in itemlocator:   
    namecontainer = items.findAll("h4",{"class":"name"})
    names = namecontainer[0].text

    pricecontainer = items.findAll("p",{"class":"price"})
    prices = pricecontainer[0].text.strip()

    print("Item Name: "+ names)
    print("Price: " + prices)   

    f.write(names.replace(","," ") + "," + prices.replace(",", " ") + "\n")
f.write("Total number of items: " + "," + str(len(itemlocator)))
f.close()
