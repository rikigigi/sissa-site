#!/usr/bin/env python3

if __name__ == "__main__":
   import argparse
   parser = argparse.ArgumentParser(description='Parse and generate html for alumni section of the site')
   parser.add_argument('--parse-url', help="use http requests to scan sector's sites. If not setted, the pickle file is used", action='store_true')
   parser.add_argument('--pickle-data-file', required=False, type=str, help="name of the pickle file where data to generate html tables is written to / readed from",
                        default='alumni.pickle', dest='iofile')
   parser=parser.parse_args()

import urllib.request as URL
from bs4 import BeautifulSoup
import re
import sys

if __name__ == "__main__":
    from common import *
else:
    from .common import *




def parse(alumni, url, find_all, elaborate_entry,class_='', **kwargs):
    response=URL.urlopen(url)
    html=response.read() 
    s=BeautifulSoup(html,'html5lib')
    absolutize_urls(url,s)
    l=s.find_all(**find_all)
    for b in l:
        res=elaborate_entry(url,b,class_,**kwargs)
        if res is not None:
            key,h=res
            alumni.setdefault(key,[]).append(h)


def elaborate_table(url,b,class_,**kwargs):
    tds=[]
    res={}
    res['class']=class_
    for td in b('td'):
        del(td['style'])
        if 'class' in td:
            td['class']=td['class']+[class_]
        else:
            td['class']=[class_]
        tds.append(td)
    try:
        year=tds[kwargs['y_col']]
        yre=re.search(r"[0-9]{2,4}",str(year))
        if yre is not None:
            key=yre.group()
        else:
            key='?'
        res['name']=tds[kwargs['name_col']]
        res['adv']=tds[kwargs['adv_col']]
        if 'th_col' in kwargs:
            res['thesis']=tds[kwargs['th_col']]
        if 'aff_col' in kwargs:
            try:
                res['affiliation']=tds[kwargs['aff_col']]
            except:
                res['affiliation']='<td class={}>?</td>'.format(class_)
    except Exception as e:
        eprint(e)
        eprint('failed to parse:')
        eprint(b)
        return
    return key,res

if  __name__ == "__main__" and parser.parse_url:
   alumni={}
   #sp
   parse(alumni, 'https://www.statphys.sissa.it/wordpress/?page_id=4704',
           {'name':'tr','class_':'thesis'}, elaborate_table, 'sp',
           name_col=0, y_col=1, adv_col=2, th_col=3,aff_col=5)
   
   #ap
   parse(alumni, 'https://www.sissa.it/ap/phdsection/alumni.php',
           {'name':'tr'},elaborate_table, 'ap',
           name_col=0, y_col=1, adv_col=2, th_col=3,aff_col=5)
   
   #cm
   parse(alumni, 'https://www.cm.sissa.it/phdsection/alumni',
           {'name':'tr'},elaborate_table, 'cm',
           name_col=0, y_col=1, adv_col=2, th_col=3)
   
   #app
   parse(alumni, 'https://www.sissa.it/app/phdsection/alumni.php',
           {'name':'tr'},elaborate_table, 'app',
           name_col=0, y_col=1, adv_col=2, th_col=3,aff_col=5)
   
   #Tpp
   parse(alumni, 'https://www.sissa.it/tpp/phdsection/alumni.php',
           {'name':'tr'},elaborate_table, 'tpp',
           name_col=0, y_col=1, adv_col=2, th_col=3,aff_col=4)
   
   
   import pdb
   
   def elaborate_sbp(url,b,class_,**kwargs):
       res={'class':class_}
       s=str(b)
       yre=re.search(r"Grad\. *Year: *([0-9]{4})",s)
       if yre is not None:
           key=yre.group(1)
       else:
           key='?'
       try:
           def extr_str(k,**kw):
               res[k]='?'
               if 'tag' in kw:
                   n=kw['tag']
                   searchkwlist=['class_']
                   searchkw={}
                   for _ in kw.keys():
                       if _ in searchkwlist:
                           searchkw[_]=kw[_]
                   tag=b(n,**searchkw)#'h6',class_='mdl-card__title-text')
                   if not 'regex' in kw:
                       if len(tag)==1:
                           res[k]=tag[0].string
                   else:
                       for t in tag:
                           s=str(t)
                           yre=re.search(kw['regex'],s)
                           if yre is not None:
                               #pdb
                               #if k=='thesis':
                               #    pdb.set_trace()
                               #end pdb
                               res[k]=yre.group(kw['regex_group'])
                               break
               else:
                   s=str(b)
                   yre=re.search(kw['regex'],s)
                   if yre is not None:
                       res[k]=yre.group(kw['regex_group'])
                   else:
                       res[k]='?regex fail?'
               res[k]='<td class="{}">'.format(class_)+res[k]+'</td>'
   
           extr_str('name',tag='h6',class_='mdl-card__title-text')
           extr_str('adv',regex=r'Supervisor: *([A-Za-z .]+)',regex_group=1)
           extr_str('thesis',tag='li', regex=r'(?m)Thesis *Title: *<strong>((.+)\n*((?:\n.+)*))</strong>',regex_group=1)
           extr_str('affiliation',tag='li', regex=r'(?m)First *Position *after *PhD: *<strong>((.+)\n*((?:\n.+)*))</strong>',regex_group=1)
       except Exception as e:
           eprint(e)
           eprint('failed to parse:')
           eprint(b)
           return
       return key,res
   
   
   parse(alumni, 'https://www.sissa.it/sbp/phdsection/alumni.php',
           {'name':'div','class':'alumni-card'}, elaborate_sbp, 'sbp')
   
   
   # save pickle file
   
   with open(parser.iofile, 'wb') as out:
       pickle.dump(alumni, out)
elif  __name__ == "__main__":
    #try to open pickle file
    try:
        with open(parser.iofile, 'rb') as inp:
            alumni = pickle.load(inp)
    except Exception as e:
       print ('error unpickling file "{}"'.format(parser.iofile))
       raise

#table output
def print_table(alumni,print=print):
    print('<table><thead><tr><th>Name</th><th>Year</th><th>Supervisor</th><th>Thesis</th><th>Position</th><th>Curriculum</th></tr></thead><tbody>')
    for y in reversed(sorted(list(alumni.keys()))):
        for n in alumni[y]:
            print('<tr>')
            print(n['name'])
            print('<td class="{}">{}</td>'.format(n['class'],y))
            print(n['adv'])
            if 'thesis' in n:
                print(n['thesis'])
            else:
                print('<td></td>')
            if 'affiliation' in n:
                print(n['affiliation'])
            else:
                print('<td></td>')
            print('<td class="{}" >{}</td>'.format(n['class'],n['class']))
            print('</tr>')
    print('</tbody></table>')

if  __name__ == "__main__":
    print_table(alumni)
