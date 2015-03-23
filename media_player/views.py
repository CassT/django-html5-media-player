from django.shortcuts import render
import os
from yattag import Doc
from django.contrib.auth.decorators import login_required
from models import MediaServer


supported_formats = ['.mp3','.wav','.ogg','.mp4','.webm']
url_paths = {'V':'/media_player/video/',
             'A':'/media_player/audio/'}
def urlpath(server,path):
    return url_paths[server.media_type] + server.name + path[len(server.directory_path):]
def display_directory(path, server, doc, n=0):
    tag = doc.tag
    text = doc.text
    asis = doc.asis
    if os.path.isdir(path):
        cssid = path[len(server.directory_path):]
        asis('<label for="'+cssid+'" style="padding-left:'+str(n)+'em">')
        text(os.path.basename(path))
        asis('</label>')
        asis('<input type="checkbox" id="'+cssid+'">')
        with tag('ul', klass='collapsibleList'):
            for x in sorted(os.listdir(path)):
                with tag('li'):
                    display_directory(os.path.join(path,x), server, doc, n=n+1)
    elif os.path.splitext(path)[1].lower() in supported_formats:
        with tag('a', href=urlpath(server,path), style='padding-left:'+str(n)+'em;'):
            text(os.path.splitext(os.path.basename(path))[0])

@login_required
def media_player(request, media_src=''):
    doc, tag, text = Doc().tagtext()
    types = {'video':'V', 'audio':'A'}
    requested_type = media_src.split('/')[0]
    media_servers = MediaServer.objects.filter(media_type=types[requested_type])
    image_src = ''
    next_path = ''
    if len(media_src.split('/')) >= 2:
        requested_server = media_src.split('/')[1]
    else:
        requested_server = ''
    for server in media_servers:
        if server.name == requested_server:
            media_src = server.server_url + media_src[len(requested_type + '/' + requested_server):]
            parent_dir = server.directory_path + os.path.split(media_src)[0][len(server.server_url):]
            plist = sorted(os.listdir(parent_dir))
            media_path = server.directory_path + media_src[len(server.server_url):]
            media_base = os.path.basename(media_path)
            for item in os.listdir(parent_dir):
                if os.path.splitext(item)[1].lower() in ['.jpg','.png']:
                    image_src = os.path.join(os.path.split(media_src)[0],item)
            if len(plist)-1 > plist.index(media_base):
                next_path = urlpath(server, os.path.join(parent_dir, plist[plist.index(media_base)+1]))
        display_directory(server.directory_path, server, doc)
    ml = media_src.split('/')
    context = { 'medialisting':doc.getvalue(), 
                'mediasource':media_src, 
                'mediatype':requested_type, 
                'imagesource':image_src,
                'heading':os.path.splitext(ml[len(ml)-1])[0],
                'nextmedia': next_path,
              }
    return render(request, 'media_player/media_player.html', context)
