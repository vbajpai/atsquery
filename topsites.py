#!/usr/bin/env/ python

"""query requests to alexa top sites web service
usage: python topsites.py ACCESS_KEY_ID SECRET_ACCESS_KEY [COUNTRY_CODE]
"""

__author__ = "Vaibhav Bajpai (contact@vaibhavbajpai.com)"
__date__ = "$Date: 2012/12/16 15:45:39 $"
__copyright__ = "Copyright (c) 2012 Vaibhav Bajpai"
__license__ = "Python"

import sys

def get(access_key_id, secret_access_key, country_code=None):
  """docstring for get"""

def main(args):
  """parses command line arguments and calls get(...)"""
  access_key_id = args[0]
  secret_access_key = args[1]
  country_code = len(args) > 2 and args[2] or None
  get(access_key_id, secret_access_key, country_code)

if __name__ == '__main__':

  def usage():
    """echoes the usage and exits"""
    print __doc__
    sys.exit(2)

  if len(sys.argv) < 3: usage()
  else: main(sys.argv[1:])
