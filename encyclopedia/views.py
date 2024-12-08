from django.shortcuts import render
from django.http import Http404
from markdown2 import Markdown
from django import forms

from . import util

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    content = util.get_entry(name)
    if content is None:
        return render(request, "encyclopedia/error.html",{
            "message": "The requested page was not found"
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "name": name,
            "content": markdowner.convert(content)
        })

def search (request):
    query = request.GET.get("q", "").strip()
    entries = util.list_entries()
    if query in entries:
        return entry(request, query)
    else:
        results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html",{
            "query": query,
            "results": results
        })
