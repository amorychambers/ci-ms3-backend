import requests

async def check_cover(i):
    cover = await requests.get(f'https://covers.openlibrary.org/b/isbn/{i}-L.jpg').status_code
    if cover == "200":
        return i
    else:
        return 0
    