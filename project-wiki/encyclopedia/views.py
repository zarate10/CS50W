from operator import ne
from django.shortcuts import render, redirect
from markdown2 import Markdown
from django import forms
import random as rn
from . import util

markdowner = Markdown()

class newEntry(forms.Form):
    title_entry = forms.CharField(label="Article title", max_length=50)
    body = forms.CharField(widget=forms.Textarea(attrs={'name':'body', 'placeholder':'# Head 1\n## Head 2\n### Head 3\nI just love **bold text**.\nThis is [an example](https://www.example.com)	'}))

class Search(forms.Form):
    search = forms.CharField(label="Search", max_length=50)

def index(req):
    return render(req, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(req):
    searched = req.GET['q']
    names = util.list_entries()

    flag = True

    for i in range(0, len(names)): 

        if searched.upper() == names[i].upper():
            return redirect("wiki", title=searched)
        else: 
            flag = False
    
    if not flag:
        results = [i for i in util.list_entries() if searched.upper() in i.upper()]
        return render(req, "encyclopedia/search.html", {
            "results": results
        })

def create(req):

    entries = util.list_entries()
    print(entries)

    if req.method == "POST": 
        form = newEntry(req.POST)
        if form.is_valid(): 
            titulo = form.cleaned_data['title_entry'].strip()
            contenido = form.cleaned_data['body']
            
            flag_title = False

            for i in range(len(entries)):
                if entries[i].upper() == titulo.upper():
                    flag_title = True 
                    break
            
            if flag_title == True:
                return render(req, "encyclopedia/create.html", {
                    "form": form,
                    "error": 'The entry already exists, change the name or modify it.'
                })
            else: 
                util.save_entry(titulo, contenido)
                return redirect("wiki", title=titulo)
                
        else:
            return render(req, "encyclopedia/create.html")

    return render(req, "encyclopedia/create.html", {
        "form": newEntry()
    })

def edit(req, title):

    content = util.get_entry(title)
    
    if not content: 
        return render(req, "encyclopedia/404.html")
    else:
        if req.method == "GET":
            return render(req, "encyclopedia/edit.html", {
                "title": title,
                "content": newEntry(initial={'title_entry': title, 'body':content})
            })
        else: 
            form_content = newEntry(req.POST)

            if form_content.is_valid():
                titulo = title
                body = form_content.cleaned_data["body"]
                util.save_entry(titulo, body)

                return wiki(req, title)

def wiki(req, title):
    entry = util.get_entry(title)

    if not entry: 
        return render(req, "encyclopedia/404.html", {
            "entry": title 
        })
    else: 
        return render(req, "encyclopedia/wiki.html", {
            "title": title,
            "entry": Markdown().convert(entry)
        })

def random(req):

    entries = util.list_entries()
    nrandom = rn.randint(0, len(entries) - 1)
    
    return wiki(req, entries[nrandom])
    