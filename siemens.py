import json
import urllib.request
from bs4 import BeautifulSoup
import urllib
from txt_read import readFile
from unidecode import unidecode
class SiemensBot:
    def __init__(self,url):
        self.url = url
    
    def getHtml(self,urunKodu):
        try:
            opener = urllib.request.build_opener()
            opener.addheaders =[('User-agent','Mozilla/5.0')]
            url = (self.url.format(urunKodu))
            page = opener.open(url).read()
            return page
        except:
            print("URL BULUNAMADI : {}".format(self.url.format(urunKodu)))
    
    def getImage(self,htmlString,urunKodu):
        try:
            parsed_html = BeautifulSoup(htmlString,"html.parser")
            inputTag = parsed_html.find(attrs={'class':'js_vp_3'})
            urun_resim = inputTag['data-srcset'].split(',')[0].replace('//','https://')
            return urun_resim
        except:
            print('get image hata')
            return False

    def getTitle(self,htmlString):
        parsed_html = BeautifulSoup(htmlString,"html.parser")
        title = str(parsed_html.title)
        return title.replace('<title>','').replace('</title>','')

    def getDesc(self,htmlString):
        parsed_html = BeautifulSoup(htmlString,"html.parser")
        desc = parsed_html.body.find('div',attrs={'class' : "content containerexpandable-togglelink"}).text.replace('\n\n','<br><br>').replace('Daha az göster','')
        return desc

    def downloadResim(self,urunKodu,url):
        f = open("resimler/siemens/{}.jpg".format(urunKodu),'wb')
        f.write(urllib.request.urlopen(url).read())
        f.close()

urlx = "https://www.siemens-home.bsh-group.com/tr/urun-listesi/{}"
"""
x = SiemensBot(urlx)
y = x.getHtml('BE555LMS0')
img_url = x.getImage(y,'BE555LMS0')
title = x.getTitle(y)
print(img_url)
a = x.downloadResim('BE555LMS0',img_url)
print(title)
"""
def writeText(filename,data):
    with open("outputs/" + filename, 'a') as f:
        f.write(str(data) + '\n')
        f.close()

def doWork(kod):
    x = SiemensBot(urlx)
    y = x.getHtml(kod)
    img_url = x.getImage(y,'BE555LMS0')
    title = x.getTitle(y)
    x.downloadResim(kod,img_url)
    desc = x.getDesc(y)
    seox = title.replace(' - ','-').replace(' ','').replace('-','-%').split('%')
    seo = seox[0] + seox[1][:-1]
    writeText('seo.txt',seo)
    writeText('title.txt',title)
    writeText('desc.txt',desc)
    print('seo : {}'.format(seo))
    print('Tamamlanan ürün : {}'.format(title))

lines = readFile('siemens_data.txt')

for line in lines:
    try:
        correct_kod = line[0:len(line)-1]
        print(correct_kod)
           # print(len(correct_kod))
        doWork(correct_kod)
    except:
        print('Error at for statement Line : {}'.format(line))
        
