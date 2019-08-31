import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
my_url = 'http://midas.iiitd.edu.in/'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html,"html.parser")
print(page_soup.findAll("p"))
print(page_soup.findAll("img"))
print(page_soup.findAll("a"))
print(page_soup.findAll("ul"))
