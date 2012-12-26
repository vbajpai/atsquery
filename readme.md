Python Sample for Alexa Top Sites
---------------------------------

This sample will make a request to the Alexa Top Sites web service 
using your Access Key ID and Secret Access Key.

Requirements:
  * Python v2.7.x
  * Requests: HTTP for Humans, v1.0.3
  * lxml: XML and HTML with Python, v3.0.2

Steps:
1. Sign up for an Amazon Web Services account at http://aws.amazon.com
2. Get your Access Key ID and Secret Access Key
3. Sign up for Alexa Top Sites at http://aws.amazon.com/alexatopsites
4. Install all requirements using pip
5. Run topsites.py

    $ pip install requirements.txt
    $ python topsites.py ACCESS_KEY_ID SECRET_ACCESS_KEY [COUNTRY_CODE]

If you are getting "Not Authorized" messages, 
you probably have one of the following problems:

1. Your access key or secret key were not entered properly.  
2. You did not sign up for [Alexa Top Sites](http://aws.amazon.com/alexatopsites)
3. Your credit card was not valid.
