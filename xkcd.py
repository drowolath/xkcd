#!/usr/bin/env python
#-*-coding: utf-8-*-

import requests
import gtk

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

COMICS = 'http://imgs.xkcd.com/comics/'

def geturl(drawing_id=None):
    u"""Get URL of a drawing given its ID.
    If no ID is given, then it gets a random URL.
    """
    if not drawing_id:
        response = requests.get('http://dynamic.xkcd.com/random/comic/')
        content = response.text
        image = content.split(COMICS)[1].split('"')[0]
        url = ''.join([COMICS, image])
    else:
        url = 'http://xkcd.com/{0}'.format(drawing_id)
    return url

def downloadimage(url):
    u"""Download drawing at given URL and write its
    informations to a GTK Buffer
    """
    result = requests.get(url)
    picturebuffer = gtk.gdk.PixbufLoader()
    #should try to really download the picture
    #pass it using gtk.gdk.pixbuf_new_from_file()
    #maybe it'd be faster, and easier to deal with
    #the drawings size
    picturebuffer.write(result.content)
    picturebuffer.close()
    image = gtk.Image()
    image.set_from_pixbuf(picturebuffer.get_pixbuf())
    return image

if __name__ == '__main__':

    if len(sys.argv) < 2:
        url = geturl()
    else:
        url = sys.argv[1]

    image = downloadimage(url)

    #Creating the canvas of the window
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.connect("destroy", gtk.main_quit)
    window.set_border_width(5)
    window.set_title(url)

    #Drawing the content of the buffer
    window.add(image)
    image.show()
    window.show()

    gtk.main()

#EOF
