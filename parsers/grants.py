#!/usr/bin/env python3

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Parse and generate html for alumni section of the site')
    parser.add_argument('--parse-url', help="use http requests to scan sector's sites. If not setted, the pickle file is used", action='store_true')
    parser.add_argument('--pickle-data-file', required=False, type=str, help="name of the pickle file where data to generate html tables is written to / readed from",
                         default='grants.pickle', dest='iofile')
    parser=parser.parse_args()




import urllib.request as URL
from bs4 import BeautifulSoup
import re
import sys
if __name__ == "__main__":
    from common import *
else:
    from .common import *


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


def unwrap_stuff(what, grants):
    for g in grants.values():
        for items in g:
            if isinstance(items['content'],str): continue
            ul=items['content'].find(what)
            if ul is not None: ul.unwrap()

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
            try:
                for e in title('strong'):
                    e.unwrap()
                for e in title('p'):
                    e.unwrap()
            except Exception as e:
                eprint(e)
            title='<a class="grant_title_link {}" href="{}">{}</a>'.format(class_,url,str(title))
            grants.setdefault(key,[]).append({'class':class_,'content':h,'title':title, 'link':link})

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
#    if 'LISA' in str(title):
#        import pdb
#        pdb.set_trace()
    link=b.find('a')
    #check for words that indicate that it is a grant -- are they all grants?
    res=re.search(r"€|\$|[Gg]grant|ERC|PRINN", b.__str__())
    if True: # res is not None:
        return '?',b,title,link
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

def elaborate_ap(url,b):
    global h2_found
    if b.find_all('h2'):
        #print('found <h2>: breaking',str(b))
        h2_found+=1
        pass
    if h2_found>=2:
        return
    title=b.find('strong')
    if title is None:
        return
    title.extract()
#    if 'LISA' in str(title):
#        import pdb
#        pdb.set_trace()
    link=b.find('a')
    #check for words that indicate that it is a grant -- are they all grants?
    #res=re.search(r"€|\$|[Gg]grant|ERC|PRINN", b.__str__())
    if True: # res is not None:
        return '?',b,title,link

if __name__ == "__main__" and parser.parse_url:
    grants={}
    
    
    #statphys
    parse(grants,'https://www.statphys.sissa.it/wordpress/?page_id=4912',{'name':'div','class_':'block'},elaborate_sp,class_='sp')
    
    
    #tpp
    parse(grants,'https://www.sissa.it/tpp/research/projects.php',{'name':'tbody'},elaborate_tpp,class_='tpp')
    
    
    #app
    h2_found=False
    parse(grants,'https://www.sissa.it/app/research/projects.php',{'name':'tbody'},elaborate_app,class_='app')
    
    
    #cm
    parse(grants,'https://www.cm.sissa.it/research/projects',{'name':'tbody'},elaborate_cm,class_='cm')
    
    
    #ap
    h2_found=0
    parse(grants,'https://www.sissa.it/ap/research/projects.php',{'name':'tbody'},elaborate_ap,class_='ap')
#sbp: ??

#save pickle
    with open(parser.iofile, 'wb') as out:
        pickle.dump(grants, out)

elif __name__ == "__main__":
    #try to open pickle file
    try:
        with open(parser.iofile, 'rb') as inp:
            grants = pickle.load(inp)
    except Exception as e:
       print ('error unpickling file "{}"'.format(parser.iofile))
       raise
    unwrap_stuff('ul',grants)

def print_table(grants,print=print): 
    for k in grants.keys():
        for e in grants[k]:
            print ('<div class="grant_m {}"><div class="grant_c">'.format(e['class']+'_outer'))
            if 'title' in e:
                print ('<div class="grant_title"><p>{}</p></div>'.format(e['title']))
            if 'year' in e:
                print ('<div class="grant_year">{}</div>'.format(e['year']))
            print ('{}</div><div class="grant_f"></div></div>'.format(e['content']))
if __name__ == "__main__":
    print_table(grants)
