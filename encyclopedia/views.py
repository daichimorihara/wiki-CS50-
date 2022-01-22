from pyexpat.errors import messages
from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util
from django import forms
import random
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect

class SearchForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        "class": "search",
        "placeholder": "Search MD Wiki"
    }))

class CreateForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
        "placeholder": "Page Title"}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
        "placeholder": "Enter Page Content using Github Markdown"
    }))

class EditForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
        "placeholder": "Edit this page's content"
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

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
            "createForm": CreateForm(),
            "invalidInputOrAlreadyExist": False,
            "searchForm": SearchForm()
        })
    elif request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]

            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/create.html", {
                    "createForm": CreateForm(),
                    "invalidInputOrAlreadyExist": True,
                    "searchForm": SearchForm()
                 })
            util.save_entry(title, text)
            return redirect(entry, title)
        else:
            return render(request, "encyclopedia/create.html", {
                "createForm": CreateForm(),
                "invalidInputOrAlreadyExist": True,
                "searchForm": SearchForm()
            })

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            return redirect(entry, title)
    
    else:
        form = EditForm({'text': util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {
            "editForm": form,
            "searchForm": SearchForm(),
            "title": title

        })

def randomly(request):
    titles = util.list_entries()
    title = random.choice(titles)
    return redirect(entry, title)
