import requests
from bs4 import BeautifulSoup
import urllib2


def FirstCrawl():
    r  = requests.get("http://www.hawes.com/pastlist.htm")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    
    links = [] 
    
    for link in soup.find_all('a'):
        links.append(link.get('href'))

    NewLinks = []

    for i in range(len(links)):
        if len(links[i])== 13:
            NewLinks.append(links[i])

    NewLinks = list(set(NewLinks))

    years = []
    for i in range(len(NewLinks)):
        years.append(NewLinks[i][0:4])

    #print(years)
    for i in range(len(NewLinks)):
        NewLinks[i] = "http://www.hawes.com/" + NewLinks[i]

    return(NewLinks, years)

def GetFileNames(Link):

    year = requests.get(Link)
    data = year.text
    soup = BeautifulSoup(data, "html.parser")

    names = [] 

    for name in soup.find_all('a'):
        names.append(name.get('href'))

    del names[0:4]
    del names[-13:-1]
    del names[-1]

    return names
    

def SecondCrawl(Link, years):

    year = requests.get(Link)
    data = year.text
    soup = BeautifulSoup(data, "html.parser")

    links = [] 

    for link in soup.find_all('a'):
        links.append(link.get('href'))

    del links[0:4]
    del links[-13:-1]
    del links[-1]
    
    for i in range(len(links)):
        links[i] = "http://www.hawes.com/" + years + "/"+ links[i]
    
    return links

def DownloadPDF(url, filename):
    
    rq = urllib2.Request(url)
    res = urllib2.urlopen(rq)
    pdf = open( "C:\\Users\srema\\Documents\\Master Thesis\\NYT\\" + filename, 'wb')
    pdf.write(res.read())
    pdf.close()


def main():

    [FirstLinks, years] = FirstCrawl()
    
    #print(FirstLinks)
    
    
    for i in range(len(FirstLinks)):
        SecondLink = SecondCrawl(FirstLinks[i], years[i])
        Filenames = GetFileNames(FirstLinks[i])
        for j in range(len(SecondLink)):
            DownloadPDF(SecondLink[j], Filenames[j])
        print('Year: ', years[i])
  

if __name__ == '__main__':
    main()
    print("Done")
