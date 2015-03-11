from django.shortcuts import render
import os
from yattag import Doc
from django.contrib.auth.decorators import login_required
from video.models import VideoDirectory


# Recurse into videos directory, generate html for nested lists
def display_directory(path, server, doc):
    if os.path.isdir(path):
        cssid = path[len(server.vid_dir):]
        doc.asis('<label for="'+cssid+'">')
        doc.text(os.path.basename(path))
        doc.asis('</label>')
        doc.asis('<input type="checkbox" id="'+cssid+'">')
        with doc.tag('ul', klass='collapsibleList'):
            for x in sorted(os.listdir(path)):
                with doc.tag('li'):
                    display_directory(os.path.join(path,x), server, doc)
    else:
        #os.path.join didn't work here for some reason
        video_url = '/video/' + server.name + path[len(server.vid_dir):]
        with doc.tag('a', href=video_url):
            doc.text(os.path.splitext(os.path.basename(path))[0])

@login_required
def index(request, video_src=''):
    doc, tag, text = Doc().tagtext()
    video_servers = VideoDirectory.objects.all()
    for server in video_servers:
        if server.name == video_src[:len(server.name)]:
            video_src = server.vid_url + video_src[len(server.name):]
        display_directory(server.vid_dir, server, doc)
    context = {'videolisting':doc.getvalue(), 'videosource':video_src}
    return render(request, 'video/index.html', context)
