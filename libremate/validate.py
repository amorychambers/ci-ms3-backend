import grequests

def check_cover(i):
    urls = [f'https://covers.openlibrary.org/b/isbn/{i}-L.jpg']
    covers = (grequests.get(u) for u in urls)
    test = grequests.map(covers)
    if test[0]:
        return i
    else:
        return 0
    