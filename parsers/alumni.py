import urllib.request as URL
from bs4 import BeautifulSoup
import re
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def norm_y(y):
    if len(y)==2:
        return '20'+y
    else:
        return y

def parse(alumni, url, find_all, elaborate_entry,class_='', **kwargs):
    response=URL.urlopen(url)
    html=response.read() 
    s=BeautifulSoup(html,'html.parser')
    l=s.find_all(**find_all)
    for b in l:
        res=elaborate_entry(url,b,class_,**kwargs)
        if res is not None:
            key,h=res
            alumni.setdefault(key,[]).append(h)

alumni={}

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
                res['affiliation']='?'
    except:
        eprint('failed to parse:')
        eprint(b)
        return
    return key,res

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

#TODO: sbp (not in a table format)

#table output
print('<table><thead><tr><th>Name</th><th>Year</th><th>Supervisor</th><th>Thesis</th><th>Position</th></tr></thead><tbody>')
for y in alumni.keys():
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
        print('</tr>')
print('</tbody></table>')


