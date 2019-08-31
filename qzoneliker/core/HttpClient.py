''' HttpClient.py is written by [xqin]: https://github.com/xqin/SmartQQ-for-Raspberry-Pi.

Rewritten by [build2last](https://github.com/build2last/QzoneLiker)
Maked it compatible with python3.
'''

import urllib
import logging
import http.cookiejar as cookielib

logging.basicConfig(
    stream=open('HttpClient.log', 'a+', encoding="utf-8"), level=logging.DEBUG,
    format='%(asctime)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
)

class HttpClient:
    ''' HTTP client for simulating interaction.
    '''
    __cookie = cookielib.CookieJar()
    __req = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(__cookie))
    __req.addheaders = [
        ('Accept', 'application/javascript, */*;q=0.8'),
        ('User-Agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)')
    ]
    urllib.request.install_opener(__req)

    def Get(self, url, refer=None):
        '''HTTP Get method'''
        try:
            req = urllib.request.Request(url)
            if refer is not None:
                req.add_header('Referer', refer)
            return urllib.request.urlopen(req).read()
        except urllib.error.HTTPError as error:
            logging.error(error.read())

    def Post(self, url, data, refer=None):
        '''HTTP post method'''
        try:
            data = urllib.parse.urlencode(data).encode("utf-8")
            req = urllib.request.Request(url, data)
            if refer is not None:
                req.add_header('Referer', refer)
            return urllib.request.urlopen(req).read()
        except urllib.error.HTTPError as http_error:
            logging.error(http_error.read())

    def Download(self, url, file_name):
        try:
            output = open(file_name, 'wb')
            output.write(urllib.request.urlopen(url).read())
            output.close()
        except Exception as e:
            logging.error(e)


    def getCookie(self, key):
        '''return cookie attribute'''
        for c in self.__cookie:
            if c.name == key:
                return c.value
        return ''

    def setCookie(self, key, val, domain):
        ck = cookielib.Cookie(version=0, name=key, value=val,
                    port=None, port_specified=False, domain=domain,
                    domain_specified=False, domain_initial_dot=False,
                    path='/', path_specified=True, secure=False,
                    expires=None, discard=True, comment=None,
                    comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.__cookie.set_cookie(ck)
