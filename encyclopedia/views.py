from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util
from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        "class": "search",
        "placeholder": "Search MD Wiki"
    }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchForm": SearchForm()
    })

def entry(request, title):
    argument = util.get_entry(title)
    if argument is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "searchForm": SearchForm()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": Markdown().convert(argument),
            "searchForm": SearchForm()
        })

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        argument = util.get_entry(title)
        if argument is None:
            related = util.relatedTitles(title)
            return render(request, "encyclopedia/search.html", {
                "title": title,
                "relatedTitles": related,
                "searchForm": SearchForm()
            })
        else:
            return redirect(entry, title)
 
    return redirect(index)
