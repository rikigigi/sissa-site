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

import pickle
#print (resource.getrlimit(resource.RLIMIT_STACK))
print (sys.getrecursionlimit())

max_rec = 20000

# May segfault without this line. 0x100 is a guess at the size of each stack frame.
# resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
sys.setrecursionlimit(max_rec)

