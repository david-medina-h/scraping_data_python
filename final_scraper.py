from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

counter = 0  

filename = "products2.csv"
f = open(filename, "w")
headers = "item_title, company_name, item_price, item_shipping\n"
f.write(headers) 

base_url = "https://www.newegg.com/Xbox-360-Games/SubCategory/ID-516/Page-{}?Order=BESTSELLING&PageSize=96"
new_url = ""
for i in range(4):

	new_url = base_url.format(str(i + 1))

	uClient = uReq(new_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	containers = page_soup.find_all("div", {"class":"item-container"})


	for container in containers:
		# item title
		title_container = container.find_all("a", {"class":"item-title"})
		product_name = title_container[0].text

		# company name
		company_container = container.find_all("a", {"class":"item-brand"})
		if not company_container:
			company_name = "NA"
		else:
			company_name = company_container[0].img["title"]

		# price
		price_container = container.find_all("li", {"class":"price-current"})
		price_name = price_container[0]
		dollar = str(price_name.strong)
		cents = str(price_name.sup)
		price_char = remove_tags(dollar + cents)

		# shipping
		shipping_container = container.find_all("li", {"class":"price-ship"})
		if shipping_container[0].text.strip() == "Free Shipping":
			shipping_price = "0"
		elif shipping_container[0].text.strip() == "Special Shipping":
			shipping_price = "Special Shipping"
		else:
			shipping_price = shipping_container[0].text.strip().split(" ", 1)[0].replace("$", "")

		f.write(product_name.replace(",", "|") + "," + company_name.replace(",", "|") + "," + price_char + "," + shipping_price + "\n")

		print("product name: " + product_name)
		print("brand: " + company_name)
		print("price: " + price_char)
		print("shipping price: " + shipping_price)
		print(counter)
		print(new_url)
		counter += 1

f.close()
