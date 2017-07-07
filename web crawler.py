import urllib

def get_page(url):
    if url:
        file=urllib.urlopen(url)
        a=file.read()
        return a
    return None
    

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def get_next_target(page):
    start_link = page.find('<a href="http:')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
        
def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]
    
def crawl_web(seed,max_pages):
    tocrawl = [seed]
    crawled = []
    graph = {}  
    index = {}
    try:
        while tocrawl:
            page = tocrawl.pop()
            if page not in crawled:
                content = get_page(page)
                add_page_to_index(index, page, content)
                outlinks = get_all_links(content)
                graph[page] = outlinks
                union(tocrawl, outlinks)
                crawled.append(page)
            if max_pages==len(crawled):
                break;
    except:
        return index, graph
    return index,graph

def hashtable_add(htable,key,value):
    hashtable_get_bucket(htable,key).append([key,value])
    return htable  
    
    
def hashtable_get_bucket(htable,keyword):
    return htable[hash_string(keyword,len(htable))]

def hash_string(keyword,buckets):
    out = 0
    for s in keyword:
        out = (out + ord(s)) % buckets
    return out

def make_hashtable(nbuckets):
    table = []
    for unused in range(0,nbuckets):
        table.append([])
    return table

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

def lucky_search(index, ranks, keyword):
    if keyword not in index:
        return None
    else:
        a=index[keyword]
        c=a[0]
        rank=0
        for i in a:
            if rank<ranks[i]:
                c=i
                rank = ranks[i]
    return c

seed=input("enter the url:")
max_pages=input("enter the max pages:")
crawled=crawl_web(seed,max_pages)
print crawled;

    
    





