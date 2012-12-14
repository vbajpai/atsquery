#!/usr/bin/ruby

require "cgi"
require "base64"
require "openssl"
require "digest/sha1"
require "uri"
require "net/https"
require "rexml/document"
require "time"

#
# Sample request to Alexa Top Sites
#

if ARGV.length < 2
  $stderr.puts "Usage: topsites.rb ACCESS_KEY_ID SECRET_ACCESS_KEY [COUNTRY_CODE]"
  exit(-1)
else
  access_key_id = ARGV[0]
  secret_access_key = ARGV[1]
  country_code = ARGV.length > 2 ? ARGV[2] : ""
end

SERVICE_HOST = "ats.amazonaws.com"

# escape str to RFC 3986
def escapeRFC3986(str)
  return URI.escape(str,/[^A-Za-z0-9\-_.~]/)
end

action = "TopSites"
responseGroup = "Country"
start = 1
count = 100

timestamp = ( Time::now ).utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")

query = {
  "Action"           => action,
  "AWSAccessKeyId"   => access_key_id,
  "Timestamp"        => timestamp,
  "ResponseGroup"    => responseGroup,
  "Start"              => start,
  "Count"            => count,
  "CountryCode"      => country_code,
  "SignatureVersion" => 2,
  "SignatureMethod"  => "HmacSHA1"
}

query_str = query.sort.map{|k,v| k + "=" + escapeRFC3986(v.to_s())}.join('&')

sign_str = "GET\n" + SERVICE_HOST + "\n/\n" + query_str 

puts "String to sign:"
puts sign_str

signature = OpenSSL::HMAC.digest( OpenSSL::Digest::Digest.new( "sha1" ), 
                                  secret_access_key, sign_str )
query_str += "&Signature=" + escapeRFC3986(Base64.encode64(signature).strip)

url = URI.parse("http://" + SERVICE_HOST + "/?" + query_str)

puts
puts "Making request to #{url}"

xml  = REXML::Document.new( Net::HTTP.get(url) )

puts
puts "Sites:"
puts

REXML::XPath.each(xml,"//aws:DataUrl"){|el| puts el.text}
