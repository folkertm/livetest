"""
LiveTest3 - Like WebTest, but on a live site.

Setup an app to test against with just a hostname:

>>> import livetest3
>>> app = livetest3.TestApp('pypi.python.org')

Make requests just like WebTest:

>>> resp = app.get('/pypi')

Grab forms:

>>> resp.forms # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{0: <webtest.Form object at 0x...>,
 1: <webtest.Form object at 0x...>,
 u'searchform': <webtest.Form object at 0x...>}
>>> form = resp.forms[0]
>>> form.fields # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
{u'term': [<webtest.Text object at 0x...>],
 u':action': [<webtest.Hidden object at 0x...>],
 u'submit': [<webtest.Submit object at 0x...>]}

Submit forms:

>>> form['term'] = 'python testing'
>>> resp = form.submit()

Test stuff in the response:

>>> resp.mustcontain('livetest3', 'Index', 'Package')
>>> resp.status
'200 OK'

"""

__author__ = 'folkert.meeuw@googlemail.com'
__version__ = '0.1.0'

import sys
import webtest
import http.client
from urllib.parse import urlparse
from urllib.parse import urlsplit, urlunsplit, urljoin
from http.cookies import BaseCookie, CookieError
from http.cookiejar import CookieJar

conn_classes = {'http': http.client.HTTPConnection,
                'https': http.client.HTTPSConnection}


class TestApp(webtest.TestApp):
    def _load_conn(self, scheme):
        if scheme in conn_classes:
            self.conn[scheme] = conn_classes[scheme](self.host)
        else:
            raise ValueError("Scheme '%s' is not supported." % scheme)

    def __init__(self, host, scheme='http', relative_to=None, cookiejar=None):
        self.host = host
        self.relative_to = relative_to
        self.conn = {}
        self._load_conn(scheme)
        self.extra_environ = {}
        if cookiejar is None:
            self.cookiejar = CookieJar()
        else:
            self.cookiejar = cookiejar
        self.reset()

    def _do_httplib_request(self, req):
        "Convert WebOb Request to httplib request."
        headers = dict((name, val) for name, val in req.headers.items()
                       if name != 'Host')
        if req.scheme not in self.conn:
            self._load_conn(req.scheme)

        conn = self.conn[req.scheme]
        conn.request(req.method, req.path_qs, req.body, headers)

        webresp = conn.getresponse()
        res = webtest.TestResponse()
        res.status = '%s %s' % (webresp.status, webresp.reason)
        res.body = webresp.read()
        res.headerlist = webresp.getheaders()
        res.errors = ''
        return res

    def do_request(self, req, status, expect_errors):
        """
        Override webtest.TestApp's method so that we do real HTTP requests
        instead of WSGI calls.
        """
        headers = {}
        if self.cookies:
            c = BaseCookie()
            for name, value in self.cookies.items():
                c[name] = value
            hc = '; '.join(['='.join([m.key, m.value]) for m in c.values()])
            req.headers['Cookie'] = hc

        res = self._do_httplib_request(req)
        # Set these attributes for consistency with webtest.
        res.request = req
        res.test_app = self

        if not expect_errors:
            self._check_status(res.status_int, res)
            self._check_errors(res)
        res.cookies_set = {}

        for header in res.headers.getall('set-cookie'):
            try:
                c = BaseCookie(header)
            except CookieError as e:
                raise CookieError(
                    "Could not parse cookie header %r: %s" % (header, e))
            for key, morsel in c.items():
                self.cookies[key] = morsel.value
                res.cookies_set[key] = morsel.value
        return res


def goto(self, href, method='get', **args):
    """
    Monkeypatch the TestResponse.goto method so that it doesn't wipe out the
    scheme and host.
    """
    scheme, host, path, query, fragment = urlsplit(href)
    # We
    fragment = ''
    href = urlunsplit((scheme, host, path, query, fragment))
    href = urljoin(self.request.url, href)
    method = method.lower()
    assert method in ('get', 'post'), (
        'Only "get" or "post" are allowed for method (you gave %r)'
        % method)
    if method == 'get':
        method = self.test_app.get
    else:
        method = self.test_app.post
    return method(href, **args)

webtest.TestResponse.goto = goto
