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
The archive will be saved in a file in the same folder named "all.items.json".

## Disclaimer

I'm not employed or associated with enjoysthings in any official capacity.

I counld't figure out how to get JSON from the server so this script has to parse HTML. Please don't ridicule me.

## TODO

I guess i should provide a way to dump the items as a more readable format like CSV. Maybe even a way to download the image files from their sites.

The script chokes when trying to serialize the JSON for very large numbers of items. A workaround is to limit the number of 30-item chunks it downloads before saving the file.
