import simplejson as json
import urllib2
import sys

S1 = '<div class="content-container'
S2 = 'background-image: url('
S3 = 'id="content-container-'
S4 = '?play=1'

def getPage(url, theheaders, thedata):
  if not theheaders: theheaders = {}
  theheaders['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30'
  if thedata:
    theheaders['Connection'] = 'Close'
    theheaders['Content-Length'] = len(thedata)
  #print(url)
  req = urllib2.Request(url, data=thedata, headers=theheaders)
  res = urllib2.urlopen(req)
  #print(res.headers)
  if res.getcode() == 200:
    x = res.read()
    return x
  return None

def save(f, b): (open(f, 'w')).write(b)
def load(f):
  try:
    return (open(f, 'r')).read()
  except IOError:
    return None

def sliceitx(s, s1, s2):
  print("s", s)
  return sliceit(s, s1, s2)

def sliceit(s, s1, s2):
  idx = s.find(s1)
  if idx != -1:
    if s2:
      edx = s.find(s2, idx+1)
      if edx != -1:
        return s[idx:edx]
    return s[idx:]
  return None

def parseChunk(c):
  itemdata = []
  idx = 0
  done = False
  c = sliceit(c, '<style>', '<div class="content-container" id="content-container-loader" >')
  while not done:
    item = sliceit(c[idx:], S1, '</script>')
    if item != None:
      idx += len(item)
      itemdata.append(parseItem(item))
    else:
      done = True
  return itemdata

def parseItem(c):
  item = {
    "type": "", # page, image, text, video
    "id": "", # id of item in enjoysthin.gs
    "title": "",
    "imageurl": "",
    "pageurl": "",
    "description": ""
  }

  imageurl = sliceit(c, S1, ">")
  imageurl = sliceit(imageurl, S2, ')')
  if imageurl:
    item['type'] = 'image'
    item['imageurl'] = imageurl[len(S2):]
  else:
    item['type'] = 'page'  

  # identify video types
  if c.find(S4) != -1:
    item['type'] = 'video'

  theid = sliceit(c, S3, '" ')
  if theid:
    item['id'] = theid[len(S3):]

  # <div class="title" id="title-619679"><a rel="nofollow" href="http://enjoysthin.gs/clicker?url=http%3A%2F%2Fwww.mymodernmet.com%2Fprofiles%2Fblogs%2Fdavid-orias-waves">Gorgeous Long-Exposure Photographs of Golden Waves - My Modern Metropolis</a></div>
  s = sliceit(c, 'class="title"', '</a>')
  link = sliceit(s, 'href="', '</a>')
  title = sliceit(link, '">', '</a>')
  link = sliceit(link, 'url=', '">')
  if link:
    link = link[4:]
    link = urllib2.unquote(link)
    item['pageurl'] = link
  title = title[2:]
  item['title'] = title

  # highlighted text
  s = sliceit(c, 'class="highlight"', '</span>')
  if s:
    s = sliceit(s, '">', None)[2:]
    item['description'] = s
    if item['title'] != item['description']:
      item['type'] = 'text'

  #print(item['id'], item['type'])
  return item

def getUserIdByUsername(username):
  url = 'http://'+username+'.enjoysthin.gs/'
  c = getPage(url, None, None)
  s1 = "/?c=user-"
  return sliceit(c, s1, '">')[len(s1):]

def archiveUser(username):
  # curl -i -X POST --data 'type=user-1168%3A30' http://vasil9v.enjoysthin.gs/api/get.things.html

  userid = getUserIdByUsername(username)

  outfile = username + ".all.items.%d.json"
  offset = 0
  idcache = {}
  itemlist = []
  done = False
  while not done:
    print("Downloading items at offset %d" % (offset))
    c = getPage('http://'+username+'.enjoysthin.gs/api/get.things.html', None, 'type=user-'+userid+':'+str(offset))
    items = parseChunk(c)
    itemlist = itemlist + items
    if len(items) < 30:
      done = True
    offset += 30
    # debug: if offset > 70: done = True
    for i in items:
      if i['id'] in idcache:
        print("already in: " + str(i['id']))
      idcache[i['id']] = i['id']
  print("Downloaded %d items" % (len(itemlist)))
  filecount = 0
  while len(itemlist) > 0:
    items1k = itemlist[0:1000]
    fname = outfile % (filecount)
    save(fname, json.dumps(items1k))
    itemlist = itemlist[1000:]
    print("Saved to %s items" % (fname))
    filecount += 1

if len(sys.argv) > 1:
  archiveUser(sys.argv[1])
else:
  print("usage: python archive <username>")