from urllib.parse import urljoin
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def norm_y(y):
    if len(y)==2:
        return '20'+y
    else:
        return y

def absolutize_urls(base_url_,b):
    try:
        bu=b.find('head').find('base',href=True)
        base_url=bu['href']
    except:
        eprint('cannot find <base> tag: using provided base_url={}'.format(base_url_))
        base_url=base_url_
    for a in b('a',href=True):
        relative_url=a['href']
        a['href']=urljoin(base_url,a['href'])


