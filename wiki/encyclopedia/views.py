from tkinter import Widget
from django.shortcuts import redirect, render
from django import forms
from django.urls import reverse
import logging
from . import util
import random

from markdown2 import Markdown

logger = logging.getLogger(__name__)
markdowner = Markdown()


class searchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Search Encyclopedia'}))


form = searchForm()


class newPageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(
        attrs={'placeholder': 'Title'}))
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={'placeholder': 'Enter the information in Markdown format'}))


class editPageForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={'placeholder': 'Enter the information in Markdown format'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": form,
    })


def entryPage(request, title):
    if util.get_entry(title):
        logger.warning(util.get_entry(title))
        return render(request, "encyclopedia/entry-page.html", {
            "title": title.capitalize(),
            "contents": markdowner.convert(util.get_entry(title)),
            "form": form
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error": "Page Not Found",
            "form": form
        })


def search(request):
    if request.method == 'POST':
        title = request.POST.get('q')
        if util.get_entry(title):
            return redirect(f'/wiki/{title}')
        else:
            lower_case_title = title.lower()
            lists = filter(
                lambda entry: entry.lower().__contains__(lower_case_title),
                util.list_entries())
            return render(request, "encyclopedia/search-result.html", {
                "lists": lists,
                "form": form
            })


def newPage(request):
    new_form = newPageForm()
    logger.warning('New Page')
    logger.warning(request.method)
    if request.method == 'POST':
        new_form = newPageForm(request.POST)
        if new_form.is_valid():
            title = new_form.cleaned_data['title']
            content = new_form.cleaned_data['content']
            lower_case_title = title.lower()
            entries = util.list_entries()
            for entry in entries:
                if entry.lower() == lower_case_title:
                    return render(request, "encyclopedia/error.html", {
                        "error": "Page of this title already existed.",
                        "form": form
                    })
            util.save_entry(title, content)
            return redirect(f'/wiki/{title}')
    return render(request, "encyclopedia/new-page.html", {
        "new_form": new_form,
        "form": form
    })


def editPage(request, title):
    text = util.get_entry(title)
    logger.warning(text)
    if request.method == 'POST':
        edit_form = editPageForm(request.POST)
        if edit_form.is_valid():
            content = edit_form.cleaned_data['content']
            util.save_entry(title, content)
            return redirect(f'/wiki/{title}')
    return render(request, "encyclopedia/edit-page.html", {
        "title": title.capitalize(),
        "form": form,
        "edit_form": editPageForm(initial={'content': text})
    })


def randomPage(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return render(request, "encyclopedia/entry-page.html", {
        "title": title.capitalize(),
        "contents": markdowner.convert(util.get_entry(title)),
        "form": form
    })
