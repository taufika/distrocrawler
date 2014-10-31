from bs4 import BeautifulSoup as BS
import urllib, json

itemList = []
accessedLinks = []

#grabbing dari razor
def grabRazor(url,base):
	print 'Fetching ' + url
	html = BS(urllib.urlopen(url).read())
	if len(html.find_all('table', {"class":"displaydetail"})) > 0 :
		for row in html.find_all('table', {"class":"displaydetail"})[0].find_all('tr'):
			namaProduk = None
			image = None
			linkProduk = None
			harga = None
			if row.td.a is not None:
				namaProduk = row.td.a.get('title')
				if row.td.a.img is not None:
					image = base+row.td.a.img.get('src')
				linkProduk = base+row.td.a.get('href')
			if len(row.find_all('td', {"class":"normaltext"})) > 0 :
				col = row.find_all('table', {"class":"normaltext"})[0]
				harga = col.find_all('span', {"class":"product-price"})[0].string
			if namaProduk is not None and image is not None and linkProduk is not None and harga is not None :
				brand = url.split('/')[6]
				cat = 't-shirt'
				if brand.lower().find('sweater') != -1:
					cat = 'sweater'
				item = [namaProduk,cat,harga,brand,linkProduk,image]
				if item not in itemList:
					itemList.append(item)

#grab dari screamous
def grabScr(url,base,title = None):
	print 'Fetching ' + url

	if title is not None:
		cat = title
	else:
		cat = url.split('=')[3]

	html = BS(urllib.urlopen(url).read())
	for card in html.find_all('div', {"id":"produkkartu"}):
		namaProduk = card.find_all('div')[0].string
		linkProduk = base+card.a.get('href')
		image = base+card.a.img.get('src')
		harga = card.find_all('div')[1].string
		item = [namaProduk,cat,harga,'Screamous',linkProduk,image]
		if item not in itemList :
			itemList.append(item)
	#ada yang id nya beda sendiri gitu
	for card in html.find_all('div', {"id":"produkkartu-last"}):
		namaProduk = card.find_all('div')[0].string
		linkProduk = base+card.a.get('href')
		image = base+card.a.img.get('src')
		harga = card.find_all('div')[1].string
		item = [namaProduk,cat,harga,'Screamous',linkProduk,image]
		if item not in itemList :
			itemList.append(item)
	#buka page selanjutnya
	for anchor in html.find_all('a'):
		href = anchor.get('href')
		if href.find('http://') == -1:
			href = base+href
		if href.find('v=produk') != -1 and href not in accessedLinks and href.find('title=') == -1 and ((href.find('halaman=1') == -1 or len(href) > (href.find('halaman=1')+9))):
			accessedLinks.append(href)			
			grabScr(href,base,cat)


print 'Crawling data distro'
print '============================'
print 'Http://www.razordistro.com'
print '============================'
url = 'http://www.razordistro.com'
connection = urllib.urlopen(url)
html = BS(connection.read())
for anchor in html.find_all('a'):
	if anchor.get('href').find('products') != -1 :
		if anchor.get('href').find('razordistro') == -1 :
			grabRazor(url+anchor.get('href'),url)
		else:
			grabRazor(anchor.get('href'),url)

print '============================'
print 'Http://www.screamous.com'
print '============================'
url = 'http://www.screamous.com/'
connection = urllib.urlopen(url)
html = BS(connection.read())
for anchor in html.find_all('a'):
	if anchor.get('href').find('v=produk') != -1 and anchor.get('href').find('MALE') == -1:
		if anchor.get('href').find('http://www.screamous.com') == -1 :
			accessedLinks.append(url+anchor.get('href'))
			grabScr(url+anchor.get('href'),url)
		else:
			accessedLinks.append(anchor.get('href'))
			grabScr(anchor.get('href'),url)


myjson = json.dumps(itemList)
with open('data.json', 'w') as datafile:
	datafile.write(myjson)
