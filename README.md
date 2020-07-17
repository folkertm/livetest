Fork Notes, 2020/07/17; 12:15 MESZ:

Writing the setup script for Python Release 3.7.

Read https://packaging.python.org/guides/making-a-pypi-friendly-readme/

Change the license to WTFPL.


Fork Notes, 2020/07/11; 12:35 MESZ:

First, the links to the pythonpaste.org website are dead. Second, the original is incompatible with Python Release 3, https://www.python.org/download/releases/3.0/. This issue is well known https://github.com/storborg/livetest/issues/8. On the English Wikipedia you can find the following article https://en.wikipedia.org/wiki/Python_Paste. There Ian Bicking is mentioned as developer.

Readme created by Scott Torborg, untouched:

LiveTest - Like WebTest, but on a live site
===========================================

Inspired by Ian Bicking's excellent `WebTest <http://pythonpaste.org/webtest/>`_, this is an extension to allow the same sort of simple pythonic testing to be used against running sites. Many tests written for WebTest will be able to be used directly on LiveTest.

This enables the full platform (app servers, load balancers, routing, DNS, etc) to be tested rather than just the internal WSGI application.

Installation
------------

Simple as::

    $ easy_install livetest

Or with pip::

    $ pip install livetest

Or grab the development version::

    $ easy_install livetest==dev


Usage
-----

Setup an app to test against with just a hostname:

>>> import livetest
>>> app = livetest.TestApp('www.google.com')

Make requests just like WebTest:

>>> resp = app.get('/')

Grab forms:

>>> resp.forms
{0: <webtest.Form object at 0x10118ac50>}
>>> form = resp.forms[0]
>>> form.fields
{'btnI': [<webtest.Submit object at 0x10118ae10>],
 'btnG': [<webtest.Submit object at 0x10118add0>],
 'q': [<webtest.Text object at 0x10118ad90>],
 'source': [<webtest.Hidden object at 0x10118ad10>],
 'hl': [<webtest.Hidden object at 0x10118acd0>],
 'ie': [<webtest.Hidden object at 0x10118ad50>]}

Submit forms:

>>> form['q'] = 'python testing'
>>> resp = form.submit()

Test stuff in the response:

>>> resp.mustcontain('Agile', 'unittest', 'PyUnit')
>>> resp
<200 OK text/html body='<!doctype...v>  '/25498>
>>> resp.status
'200 OK'


Credits
-------
Thanks to Edward Dale (scompt) for various fixes.


Links
-----
* `website <https://github.com/storborg/livetest>`_
* `WebTest home <http://pythonpaste.org/webtest>`_
* `development version <https://github.com/storborg/livetest/zipball/master#egg=livetest-dev>`_


License
-------

Livetest is released under the MIT License. See the LICENSE file for more information.


.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround
