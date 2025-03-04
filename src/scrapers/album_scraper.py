from requests_html import HTMLSession

session = HTMLSession()
url = 'https://open.spotify.com/album/0hvT3yIEysuuvkK73vgdcW'
r = session.get(url)
r.html.render(sleep=3, keep_page = True, scrolldown=1)

print(len(r.html.find('a[data-testid="internal-track-link"]')))
# can't i get album links from spotify api?