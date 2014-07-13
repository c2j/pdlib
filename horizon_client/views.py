#encoding = utf-8
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

def retrieve(request):
    term = request.REQUEST["term"] if "term" in request.REQUEST else None

    if term == None:
        return render(request, 'pdlib/index.html')
    else:

        #try:
        books = _query(term)
        #except Exception as e:
        #    print "ERROR when [", term, "]", e
        #    books = []
        #for book in books:
        #    print book.url, book.title, book.authors, book.issuer
        return render(request, 'pdlib/index.html',
                      {"books": books,
                       "term": term,
                       "prev_url":"b",
                       "next_url":"a"}
        )

def detail(request):
    import urllib2
    from urllib import unquote, quote
    import HTMLParser
    PARSER = HTMLParser.HTMLParser()
    encoded_url = request.REQUEST["url"] if "url" in request.REQUEST else None
    if encoded_url == None:
        return render(request, 'pdlib/index.html')
    else:
        print encoded_url
        bookurl = PARSER.unescape(encoded_url) #unquote(encoded_url)
        print bookurl
        content = urllib2.urlopen(bookurl).read()
        from BeautifulSoup import BeautifulSoup, Tag, NavigableString
        soup = BeautifulSoup(content)
        #print soup
        form_full = str(soup.find("form", {"name":"full"}))
        form_details = str(soup.find("form", {"name":"details"}))
        form_navigation = str(soup.find("form", {"name":"navigation"}))

        return render(request, 'pdlib/detail.html',
                          {"form_full": form_full,
                           "form_details": form_details,
                           "form_navigation": form_navigation,
                           }
            )

def _query(term):
    import sys
    import urllib2
    from urllib import unquote, quote
    import HTMLParser
    PARSER = HTMLParser.HTMLParser()
    PDLIB_URL="http://116.236.176.205/ipac20/ipac.jsp?session=14B23F9000669.24596&menu=search&aspect=basic&npp=10&ipp=20&profile=pdlib&ri=&index=.GW&x=16&y=12&aspect=basic"
    #print quote(term.decode(sys.stdin.encoding).encode('utf8'))
    PDLIB_URL=PDLIB_URL+"&term="+quote(term.encode('utf8'))
    content = urllib2.urlopen(PDLIB_URL).read()
    from BeautifulSoup import BeautifulSoup, Tag, NavigableString
    soup = BeautifulSoup(content)
    #print soup
    c = soup.find("center").find("table").find("td")
    alltbs = c.contents
    #print alltbs
    books=[]
    from horizon_client.models import Book
    for tbs in alltbs:
        if tbs.name and tbs.name == "table":
            book = Book()
            htmlbook = tbs.find("tr").contents[1].find("table")
            trurl = htmlbook.contents[0]
            tagurl = trurl.find("a")
            book.url = unquote(tagurl["href"]).split("'")[1]
            book.encoded_url = quote(book.url.encode('utf8'))
            print book.encoded_url
            book.title = PARSER.unescape(tagurl.text)
            trauthor = htmlbook.contents[1]
            tagauthors = trauthor.findAll("i")
            book.authors=[]
            for ia in tagauthors:
                book.authors.append(PARSER.unescape(ia.text))
            trissuer = htmlbook.contents[2]
            book.issuer = PARSER.unescape(trissuer.find("a").text)
            books.append(book)
    return books
