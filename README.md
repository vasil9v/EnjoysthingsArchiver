# EnjoysthingsArchiver

EnjoysthingsArchiver is a python script that allows you to download all the items in your http://enjoysthin.gs/ account. They are saved as a single JSON data file. This file contains links to the images you've enjoyed on the original sites, no actual images are downloaded. Enjoyed items of type image, page, video and selected text are stored.

We will miss you enjoysthin.gs!

-vasil9v

## Requirements

You need to have python installed on your machine.

## Using it

Open up a terminal and run
```
    python archive.py <username>
```
where &lt;username&gt; is replaced with your username from enjoysthings. For example:
```
    python archive.py vasil9v
```
The archive will be saved in a set of files in the same folder named "&lt;username&gt;.all.items.N.json" with N starting at 0 and increasing by 1 for each 1000-item file needed until all the items are saved.

Each item's JSON looks like this:
```
{
  "description": "",
  "title": "Tower Bridge forced to open for 50 foot rubber duck | London - ITV News",
  "imageurl": "http://news.images.itv.com/image/file/132966/article_ccbbf53440fc2fac_1355230425_9j-4aaqsk.jpeg",
  "pageurl": "http://www.itv.com/news/london/2012-12-11/london-bridge-forced-to-open-for-50-foot-rubber-duck/",
  "type": "image",
  "id": "622159"
}
```
For items like selected text, the description field is populated with the text and the imageurl field will be empty.

## Disclaimer

I'm not employed or associated with enjoysthings in any official capacity.

I counld't figure out how to get JSON from the server so this script has to parse HTML. Please don't ridicule me.

## TODO

I guess i should provide a way to dump the items as a more readable format like CSV. Maybe even a way to download the image files from their sites.

The script still chokes when trying to serialize the JSON for very large numbers of items. Still trying to figure that out. Could be wild UTF in some URLs.