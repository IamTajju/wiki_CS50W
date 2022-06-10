from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from django.core.exceptions import ViewDoesNotExist
from . import util
import random
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    pageContent = util.get_entry(title)
    markdowner = Markdown()
    pageContent = markdowner.convert(pageContent)
    if not pageContent:
        raise Http404

    return render(request, "encyclopedia/entry.html", {
        "pageContent": pageContent,
        "title": title
    })


def search(request):
    try:
        title = request.GET['title']
    except:
        return render(request, "encyclopedia/search.html", {
            "message": "Please enter a title query in the search box"
        })

    if(util.get_entry(title) == None):
        results = []
        entries = util.list_entries()
        for stored_title in entries:
            if title in stored_title:
                results.append(stored_title)

        return render(request, "encyclopedia/search.html", {
            "results": results
        })

    return entry(request, title)


def createPage(request):
    message = ""
    markdownContent = ""

    if request.method == "POST":
        title = request.POST['title']
        markdownContent = request.POST['markdownContent']

        if (util.get_entry(title) != None):
            message = "An entry with this title already exists!"

        else:
            util.save_entry(title, markdownContent)
            return entry(request, title)

    return render(request, "encyclopedia/create.html", {
        "message": message,
        "markdownContent": markdownContent
    })


def editPage(request, title):

    pageContent = util.get_entry(title)
    if not pageContent:
        raise Http404

    if request.method == 'POST':
        util.save_entry(title, request.POST['markdownContent'])
        return entry(request, title)

    return render(request, "encyclopedia/edit.html", {
        "pageContent": pageContent,
        "title": title
    })


def randomizePage(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return entry(request, title)


# 404 Exception Handler
def ResponseNotFoundHandler(request, exception):
    return render(request, 'encyclopedia/404.html', status=404)
