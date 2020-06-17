import urllib.request as URL
from bs4 import BeautifulSoup
import re
import sys

from common import *


def make_key(y1,y2):
    return norm_y(y1)+'-'+norm_y(y2)

def massage_content(b, add_class=''):
    for e in b():
        del (e['style'])
    for e in b('tbody'):
        e.unwrap()
    for e in b('tr'):
        e.unwrap()
    for e in b('td'):
        e.unwrap()
    for e in b('img'):
        e.decompose()
    for e in b('span'):
        e.unwrap()
    for e in b('p'):
        e.unwrap()
    for e in b('span'):
        e.unwrap()
    for e in b('p'):
        e.unwrap()
    for e in b():
        if len(e.contents)==1 and ( e.contents[0].rstrip()=='' or e.contents[0].rstrip()=='<br>'):
            e.decompose()
    b.name='div'
    b['class']='block '+add_class
    eprint(b)
    return
    tds=b('td')
    nt=len(tds)
    if nt>=1:
        idx=1
        if nt==2:
            tds[0].decompose()
        elif nt==1:
            idx=0
        d = tds[idx]
        d.name='div'
        d['class']='block'
        eprint(d)
        b.replace_with(d)
    else:
        trs=b('tr')
        if len(trs)==1:
            d=trs[0]
            eprint('d=')
            eprint(d)
            d.name='div'
            d['class']='block'
            b.replace_with(d)

def parse(grants, url, find_all, elaborate_entry,class_=''):
    response=URL.urlopen(url)
    html=response.read() 
    s=BeautifulSoup(html,'html.parser')
    absolutize_urls(url,s)
    l=s.find_all(**find_all)
    for b in l:
        res=elaborate_entry(url,b)
        if res is not None:
            key,h,title,link=res
            massage_content(h,class_)
            grants.setdefault(key,[]).append({'class':class_,'content':h,'title':title, 'link':link})

grants={}


#statphys
def elaborate_sp(url,b):
    res=re.search(r"([0-9]{4}).([0-9]{4})", b.__str__())
    if res is not None:
        key=make_key(res.group(1),res.group(2))
    else:
        key='?'
    img=b.find('div',class_='blockimg')
    img.decompose()
    title=b.find('div',class_='blockTextTitle')
    if title is None:
        return
    title.extract()
    return key,b,title, None
parse(grants,'https://www.statphys.sissa.it/wordpress/?page_id=4912',{'name':'div','class_':'block'},elaborate_sp,class_='sp')


#tpp
def elaborate_tpp(url,b):
    res=re.search(r"[a-zA-Z]{0,3} *([0-9]{2,4}) */ *[a-zA-Z]{0,3} *([0-9]{2,4})", b.__str__())
    if res is not None:
        key=make_key(res.group(1),res.group(2))
    else:
        key='?'
    title=b.find('strong')
    link=b.find('span')
    if title is None:
        return
    title.extract()
    link.extract()
    return key,b,title, link
parse(grants,'https://www.sissa.it/tpp/research/projects.php',{'name':'tbody'},elaborate_tpp,class_='tpp')


#app
h2_found=False
def elaborate_app(url,b):
    global h2_found
    if b.find_all('h2'):
        #print('found <h2>: breaking')
        h2_found=True
    if h2_found:
        return
    title=b.find('strong')
    if title is None:
        return
    title.extract()
    link=b.find('a')
    #check for words that indicate that it is a grant -- are they all grants?
    res=re.search(r"€|\$|[Gg]grant|ERC|PRINN", b.__str__())
    if True: # res is not None:
        return '?',b,title,link
parse(grants,'https://www.sissa.it/app/research/projects.php',{'name':'tbody'},elaborate_app,class_='app')


#cm
def elaborate_cm(url,b):
    #check for words that indicate that it is a grant
    #res=re.search(r"€|\$|[Gg]grant|ERC", b.__str__())
    #if res is not None:
    title=b.find('strong')
    if title is None:
        return
    title.extract()
    link=b.find('a')
    if link is not None:
        link.extract()
    return '?',b,title,link
parse(grants,'https://www.cm.sissa.it/research/projects',{'name':'tbody'},elaborate_cm,class_='cm')


#ap
ap=r'''ASI-COSMOS (2016/21, posizione RTDa + missioni)                                        --> Baccigalupi
ASI-LiteBIRD (2020/23, assegnista + missioni)                                                  --> Baccigalupi
ASI-Euclid (2018/21, missioni)                                                                            --> Baccigalupi
INFN-INDARK (2020/23, missioni)                                                                     --> Baccigalupi
EU-H2020-MSCA/ITN "BiD4BEST" (2020/24, studente Ph.D. + missioni)           --> Lapi
PRIN2017-MIUR (2019/21, assegnista + missioni)                                          --> Lapi/Bressan
FSE-FVG (2020/22, assegnista)                                                                           --> Lapi/Bressan
INFN-QGSKY (2020/23, missioni)                                                                      --> Salucci/Valdarnini'''
for b in ap.splitlines():
    res=re.search(r"\(([0-9]{2,4}) */ *([0-9]{2,4}) *, *[a-zA-Z \-+]*\)",b
)
    bb={'class':'ap','content':r'<div class="block ap"><p>'+b+r'</p></div>'}
    if res is not None:
        key=make_key(res.group(1),res.group(2))
        grants.setdefault(key,[]).append(bb)
    else:
        grants.setdefault('?',[]).append(bb)

#sbp: ??
for k in grants.keys():
    for e in grants[k]:
        print ('<div class="grant_m {}"><div class="grant_c">'.format(e['class']+'_outer'))
        if 'title' in e:
            print ('<div class="grant_title"><p>{}</p></div>'.format(e['title'].string))
        if 'year' in e:
            print ('<div class="grant_year">{}</div>'.format(e['year']))
        print ('{}</div><div class="grant_f"></div></div>'.format(e['content']))

