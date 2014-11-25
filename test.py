from config import DEVELOPER_KEY, DEVELOPER_SECRET
import oauth2 as oauth
import urlparse
import urllib
import webbrowser

url = 'http://www.goodreads.com'
request_token_url = '%s/oauth/request_token' % url
auth_url = '%s/oauth/authorize' % url
access_token_url = '%s/oauth/access_token' % url

consumer = oauth.Consumer(key = DEVELOPER_KEY, secret = DEVELOPER_SECRET)
target_list = 'holding'

client = oauth.Client(consumer)

response, content = client.request(request_token_url, 'GET')
if response['status'] != '200':
    raise Exception('Cannot fetch resource: %s' % response['status'] + content)

request_token = dict(urlparse.parse_qsl(content))

auth_link = '%s?oauth_token=%s' % (auth_url, request_token['oauth_token'])
print "Use a browser to visit this link and accept your application: "
print auth_link
webbrowser.open("%s" % auth_link)

accepted = 'n'
while accepted.lower() == 'n':
    #sign in to app
    accepted = raw_input('Have you authorized me? (y/n) ')

token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
client = oauth.Client(consumer, token)
response, content = client.request(access_token_url, 'POST')
if response['status'] != '200':
    raise Exception('Invalid response: %s' % response['status'])

access_token = dict(urlparse.parse_qsl(content))

print 'Save this for later: '
print 'oauth token key:    ' + access_token['oauth_token']
print 'oauth token secret: ' + access_token['oauth_token_secret']
 
token = oauth.Token(access_token['oauth_token'],
                    access_token['oauth_token_secret'])
 
 
#
# As an example, let's add a book to one of the user's shelves
#
add_to_list = True 
 
def addABook():
    client = oauth.Client(consumer, token)
    # the book is: "Generation A" by Douglas Coupland
    body = urllib.urlencode({'name': 'to-read', 'book_id': 6801825})
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response, content = client.request('%s/shelf/add_to_shelf.xml' % url,
                                   'POST', body, headers)
    # check that the new resource has been created
    if response['status'] != '201':
        raise Exception('Cannot create resource: %s' % response['status'])
    else:
        print 'Book added!'
 
 
if add_to_list:
    addABook()
