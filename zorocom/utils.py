import cookielib
from random import randint
import random
import re
import time
import traceback
from urllib2 import HTTPError
import requests
from lxml import html
import mechanize
from requests.adapters import HTTPAdapter
from requests.auth import HTTPProxyAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import warnings
import urllib3

warnings.simplefilter('ignore', urllib3.exceptions.SecurityWarning)
br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

proxies = [['184.75.209.130','userxxxxx','xxxxxxxxx','6060'],
           ['184.75.208.10','userxxxxx','xxxxxxxxx','6060'],
           ['96.47.226.34','userxxxxx','xxxxxxxxx','6060'],
           ['96.47.226.98','userxxxxx','xxxxxxxxx','6060'],
           ['96.47.226.130','userxxxxx','xxxxxxxxx','6060'],
           ['96.47.226.138','userxxxxx','xxxxxxxxx','6060'],
           ['96.44.147.34','userxxxxx','xxxxxxxxx','6060'],
           ['96.44.147.122','userxxxxx','xxxxxxxxx','6060'],
           ['96.44.147.138','userxxxxx','xxxxxxxxx','6060'],
           ['96.44.146.106','userxxxxx','xxxxxxxxx','6060'],
           #['web.proxy.torguard.org','userxxxxx','xxxxxxxxx','6060'],
           ]
credentials = {'lawsonproducts': {'username':'kexxxxx2','password':'xxxxx**xxxx'},
               'acklandsgrainger': {'username':'kexxxxxxxxxx@xxxxx.com', 'password':'xxxx**xxxx'}
               }

def request_html_source_url(url):
    tries = 0
    req_proxy = {}
    source = None
    # if proxy and proxies:
    while tries < 5:
        PROXY = random.choice(['au.torguardvpnaccess.com:6060',
                            'melb.au.torguardvpnaccess.com:6060',
                            'fin.torguardvpnaccess.com:6060',
                            'ca.torguardvpnaccess.com:6060',
                            'vanc.ca.west.torguardvpnaccess.com:6060',
                            'ire.torguardvpnaccess.com:6060',
                            #'in.torguardvpnaccess.com:6060',
                            'jp.torguardvpnaccess.com:6060',
                            'nl.torguardvpnaccess.com:6060',
                            'uk.torguardvpnaccess.com:6060',
                            
                            'ro.torguardvpnaccess.com:6060',
                            #'mos.ru.torguardvpnaccess.com:6060',
                            'swe.torguardvpnaccess.com:6060',
                            'swiss.torguardvpnaccess.com:6060',
                            'bg.torguardvpnaccess.com:6060',
                            'hk.torguardvpnaccess.com:6060',
                            'cr.torguardvpnaccess.com:6060',
                            'hg.torguardvpnaccess.com:6060'
                            ])
        print "USING", PROXY
        req_proxy = {'http': 'http://userxxxxx:xxxxxxxxx' + '@' +  PROXY+'/',
                    'https': 'https://userxxxxx:xxxxxxxxx' + '@' +  PROXY+'/'}
    
        try:
            source = requests.get(url,proxies=req_proxy).content
            try:
                source = source.encode('ascii','ignore').decode('utf8','ignore')
            except:
                source = source.decode('ascii','ignore').encode('utf8','ignore')
            tries = 6
        except HTTPError:
            print "http error"
            return None
            tries += 1
        except:
            tries += 1
            print traceback.print_exc()
            print "sleeping for 1 seconds after timeout"
            time.sleep(1)
    return source
    
    # tries = 0
    # source =0
    # while tries < 5:
    #     try:
    #         source = br.open(url,timeout=30).get_data()
    #         try:
    #             source = source.encode('ascii','ignore').decode('utf8','ignore')
    #         except:
    #             source = source.decode('ascii','ignore').encode('utf8','ignore')
    #         tries = 6
    #     except HTTPError:
    #         print "http error"
    #         return None
    #         tries += 1
    #     except:
    #         tries += 1
    #         print traceback.print_exc()
    #         print "sleeping for 1 seconds after timeout"
    #         time.sleep(1)
    # return source

def request_parse_source_url(url, source_url,proxy=True):
    tries = 0
    req_proxy = {}
    source = None
    # if proxy and proxies:
    while tries < 5:
        PROXY = random.choice(['au.torguardvpnaccess.com:6060',
                            'melb.au.torguardvpnaccess.com:6060',
                            'fin.torguardvpnaccess.com:6060',
                            'ca.torguardvpnaccess.com:6060',
                            'vanc.ca.west.torguardvpnaccess.com:6060',
                            'ire.torguardvpnaccess.com:6060',
                            #'in.torguardvpnaccess.com:6060',
                            'jp.torguardvpnaccess.com:6060',
                            'nl.torguardvpnaccess.com:6060',
                            'uk.torguardvpnaccess.com:6060',
                            
                            'ro.torguardvpnaccess.com:6060',
                            #'mos.ru.torguardvpnaccess.com:6060',
                            'swe.torguardvpnaccess.com:6060',
                            'swiss.torguardvpnaccess.com:6060',
                            'bg.torguardvpnaccess.com:6060',
                            'hk.torguardvpnaccess.com:6060',
                            'cr.torguardvpnaccess.com:6060',
                            'hg.torguardvpnaccess.com:6060'
                            ])
        print "USING", PROXY
        req_proxy = {'http': 'http://userxxxxx:xxxxxxxxx' + '@' +  PROXY+'/',
                    'https': 'https://userxxxxx:xxxxxxxxx' + '@' +  PROXY+'/'}
    
        try:
            source = requests.get(url,proxies=req_proxy).content
            try:
                source = source.encode('ascii','ignore').decode('utf8','ignore')
            except:
                source = source.decode('ascii','ignore').encode('utf8','ignore')
            tries = 6
        except HTTPError:
            print "http error"
            return None
            tries += 1
        except:
            tries += 1
            print traceback.print_exc()
            print "sleeping for 1 seconds after timeout"
            time.sleep(1)

    try:
        parsed_source = html.fromstring(source, source_url)
        try:
            parsed_source.make_links_absolute()
        except:
            pass
    except Exception as e:
        print "error in parsing"
        print traceback.print_exc()
        parsed_source = None
    return parsed_source,source

def getCrawleraParsedSource(url, source_url, crawlera):

	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
	}

	tryout = 1

	while True:

		proxy_auth = HTTPProxyAuth("xxxxx", "")

		proxy = {
			"https": "https://xxxx:@proxy.crawlera.com:8010",
			"http": "http://xxxx:@proxy.crawlera.com:8010"
			}

		headers = {
			'User-Agent': 'Mozilla/5.0',
			'X-Crawlera-Use-HTTPS': '1'
		}

		s = requests.Session()
		s.mount('http://', HTTPAdapter(max_retries=1))
		s.mount('https://', HTTPAdapter(max_retries=1))

		try:
			if crawlera is True:
				r = s.get(url, headers=headers, timeout=50, proxies=proxy, verify='xxx-ca.crt')
				# r = s.get(url, headers=headers, timeout=30, proxies=proxy, auth=proxy_auth, verify='xxxx-ca.crt')
			else:
				r = s.get(url, headers=headers, timeout=30, verify=False)

			print(r.status_code, url)
			if r.status_code == 200:
				content = (r.content).decode('UTF-8', 'ignore')
				ps = html.fromstring(content, source_url)
				ps.make_links_absolute()
				return ps, content #html.fromstring(content)
			elif r.status_code == 404:
				return None, None
			else:
				pass

		except Exception as E:
			print(E)
			return None, None

		tryout += 1

		if crawlera is False:
			if tryout == 3:
				return None, None
    
def get_parsed_source(url, source_url,proxy=False):
    tries = 0
    if proxy and proxies:
        proxy = proxies[randint(0,len(proxies)-1)]
        br.set_proxies({"http": proxy[0] + ":" +proxy[3]})
        br.add_proxy_password(proxy[1], proxy[2])
    while tries < 5:
        try:
            source = br.open(url,timeout=30).get_data()
            try:
                source = source.encode('ascii','ignore').decode('utf8','ignore')
            except:
                source = source.decode('ascii','ignore').encode('utf8','ignore')
            tries = 6
        except HTTPError:
            print "http error"
            return None
            tries += 1
        except:
            tries += 1
            print traceback.print_exc()
            print "sleeping for 1 seconds after timeout"
            time.sleep(1)

    try:
        parsed_source = html.fromstring(source, source_url)
        try:
            parsed_source.make_links_absolute()
        except:
            pass
    except Exception as e:
        print "error in parsing"
        print traceback.print_exc()
        parsed_source = None
    return parsed_source

def getDescription(parsed_source, xpath_str):
    try:
        text_list = parsed_source.xpath(xpath_str)
        if len(text_list) == 0:
            return ''
        else:
            text_list = [x.replace('\n','').replace('\t','').replace('\r','').strip() for x in text_list]
            content = " ".join(text_list).strip()
            return content
    except:
        print traceback.format_exc()
        return ''


def getText(parsed_source, xpath_str):
    try:
        text = parsed_source.xpath(xpath_str)
        if len(text) == 0:
            return ''
        else:
            return text[0].replace('\n','').replace('\t','').replace('\r','').strip()
    except:
        return ""


def getPrice(parsed_source, xpath_str):
    text = parsed_source.xpath(xpath_str)
    if len(text) == 0:
        return 0
    else:
        text = text[0].split('per',1)[0]
        price = re.findall("\d+",text.replace(",",""))
        if price:
            return ".".join(price)
        else:
            return ""
def get_parsed_source_from_source(source, source_url):
    try:
        parsed_source = html.fromstring(source, source_url)
        try:
            parsed_source.make_links_absolute()
        except:
            pass
    except Exception as e:
        print "error in parsing"
        print traceback.print_exc()
        parsed_source = None
    
    return parsed_source
