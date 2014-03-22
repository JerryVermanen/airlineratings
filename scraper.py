import scraperwiki
import requests
import lxml.html
import mechanize

letterList=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
linkList=[]


#GET LINKS OF INDIVIDUAL AIRLINES

def getLinks(url):
    html = requests.get(url).text
    br = mechanize.Browser()
    br.set_handle_robots(False)
    root = lxml.html.fromstring(html)
    for letter in letterList:
        url2 = url+letter
        html2 = requests.get(url2).text
        br = mechanize.Browser()
        br.set_handle_robots(False)
        root2 = lxml.html.fromstring(html2)
        for el in root2.cssselect("div[class= 'span3  airlinelogo'] a"):
            link= el.attrib['href']
            linkList.append(el.attrib['href'])

#GET INFORMATION FROM EACH AIRLINE COMPANY
def getInfo(url):
    html = requests.get(url).text
    br = mechanize.Browser()
    br.set_handle_robots(False)
    root = lxml.html.fromstring(html)
    #country also gets the url: to clean with refine
    data = {
        'Airline' : [name.text_content() for name in root.cssselect("h1[class= 'ratingairname']")],
        'Safety Rating' : [rating.text_content() for rating in root.cssselect("div[style= 'display:block; margin:10px 0 0 0']")],
        'Logo' : [logo.attrib['src'] for logo in root.cssselect("img[class= 'pull-right img-polaroid']")],
        'Quality' : [quality.text_content() for quality in root.cssselect("span[class= 'label label-info']")],
        'Country of Origin and URL': [country.text_content() for country in root.cssselect("div[class= 'smalldeets']")][0],
        'Airline Ratings Link' : url,
            }
    scraperwiki.sqlite.save(unique_keys = ['Airline'], data=data)

url= 'http://www.airlineratings.com/airlines-ratings.php?l='
getLinks(url)
for link in linkList:
    getInfo(link)



    