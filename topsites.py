#!/usr/bin/env/ python

"""query requests to alexa top sites web service
usage: python topsites.py ACCESS_KEY_ID SECRET_ACCESS_KEY [COUNTRY_CODE]
"""

__author__ = "Vaibhav Bajpai (contact@vaibhavbajpai.com)"
__date__ = "$Date: 2012/12/16 15:45:39 $"
__copyright__ = "Copyright (c) 2012 Vaibhav Bajpai"
__license__ = "Python"

import sys
import requests
import datetime
import hmac
import hashlib
import base64
import urllib
import collections
import lxml.etree

host = 'ats.amazonaws.com'
action = 'TopSites'
access_key_id = None
timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
response_group = "Country"
start = 1
count = 100
country_code = ''
signature_version = 2
signature_method = 'HmacSHA1'

def http_get(access_key_id, secret_access_key, country_code='', signature=''):
  """sends a HTTP GET to alexa top sites web service using requests;
     parses the XML response using lxml; filters the response XML for domain
     names and returns the list of domain entries"""

  query = {
      "Action"             :     action
    , "AWSAccessKeyId"     :     access_key_id
    , "Timestamp"          :     timestamp
    , "ResponseGroup"      :     response_group
    , "Start"              :     start
    , "Count"              :     count
    , "CountryCode"        :     country_code
    , "SignatureVersion"   :     signature_version
    , "SignatureMethod"    :     signature_method
  }

  query = collections.OrderedDict(sorted(query.items()))
  req = requests.Request (
                            method='GET'
                          , url='http://%s'%(host)
                          , params=query
                         )
  try: prep = req.prepare()
  except Exception as e: print e

  string_to_sign = '\n'.join([prep.method, host, '/', prep.path_url[2:]])
  signature = hmac.new (
                          key=secret_access_key
                        , msg=bytes(string_to_sign)
                        , digestmod=hashlib.sha1
                       ).digest()
  signature = base64.b64encode(signature)
  prep.url = '%s&Signature=%s'%(prep.url, signature)
  s = requests.Session()
  try: res = s.send(prep)
  except Exception as e: print e
  else:
    try:
      if res.status_code is not requests.codes.ok: res.raise_for_status()
    except Exception as e:
      print e
      print res.text

  xml = res.text
  try: tree = lxml.etree.fromstring(xml)
  except Exception as e: print e
  NSMAP = {'aws' : 'http://ats.amazonaws.com/doc/2005-11-21'}
  try: entries = tree.xpath('//aws:DataUrl', namespaces = NSMAP)
  except Exception as e: print e
  entries = [entry.text for entry in entries]
  return entries

def main(args):
  """parses command line arguments and calls http_get(...); 
     retrieves the list of entries and prints them out"""
  access_key_id = args[0]
  secret_access_key = args[1]
  country_code = len(args) > 2 and args[2] or ''
  try:
    entries = http_get(access_key_id, secret_access_key, country_code)
    for entry in entries: print entry
  except TypeError as e: print e

if __name__ == '__main__':

  def usage():
    """echoes the usage and exits"""
    print __doc__
    sys.exit(2)

  if len(sys.argv) < 3: usage()
  else: main(sys.argv[1:])
