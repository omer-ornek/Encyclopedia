from django.shortcuts import render
from .md_to_html import md_to_html
from . import util
from django import forms
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(), label="Content")
class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    cont = util.get_entry(title)
    if cont == None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": md_to_html(util.get_entry(title))
    })

def search(request):
    if request.method == "POST":
        query = request.POST["q"]
        if util.get_entry(query):
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": md_to_html(util.get_entry(query))
            })
        else:
            matches = []
            for e in util.list_entries():
                if query in e:
                    matches.append(e)
            return render(request, "encyclopedia/search.html", {
                "entries": matches,
                "query": query
            })
        
def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/error.html", {
                    "message": "The page already exists."
                })
            util.save_entry(title, content)
            return entry(request, title)
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)  
            return entry(request, title)
    else:
        initial_content = util.get_entry(title) or ""
        form = EditForm(initial={"title": title, "content": initial_content})
    
    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title
    })

def random_page(request):
    entries = util.list_entries()
    if not entries:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries available."
        })
    n = random.randint(0, len(entries) - 1)
    return entry(request, entries[n])
