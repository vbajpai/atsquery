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

host = 'ats.amazonaws.com'
action = 'TopSites'
access_key_id = None
timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
response_group = "Country"
start = 1
count = 10
country_code = ''
signature_version = 2
signature_method = 'HmacSHA1'

def http_get(access_key_id, secret_access_key, country_code='', signature=''):
  """docstring for http_get"""

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
  r = requests.request (
                          method='GET'
                        , url='http://%s'%(host)
                        , params=query
                        , return_response=False
                       )

  request_raw = '\n'.join([r.method, host, '/', r.path_url[2:]])
  request_raw = base64.b64encode(request_raw)
  signature = hmac.new (
                          key=secret_access_key
                        , msg=bytes(request_raw)
                        , digestmod=hashlib.sha1
                       ).digest()
  signature = base64.b64encode(signature)
  query['Signature'] = signature

  r.params = query
  print r.params

  r.send()
  res = r.response
  print res.status_code
  print res.text

def main(args):
  """parses command line arguments and calls get(...)"""
  access_key_id = args[0]
  secret_access_key = args[1]
  country_code = len(args) > 2 and args[2] or ''
  http_get(access_key_id, secret_access_key, country_code)

if __name__ == '__main__':

  def usage():
    """echoes the usage and exits"""
    print __doc__
    sys.exit(2)

  if len(sys.argv) < 3: usage()
  else: main(sys.argv[1:])
