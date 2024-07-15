import re
import markdown2

from django.shortcuts import render, redirect
from django import forms

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'style': "display:flex"}))
    content = forms.CharField(
        widget=forms.Textarea(attrs={'style': "vertical-align: top; display:flex; height: 300px; width: 500px"}))


class EditPageForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'style': "vertical-align: top; display:flex; height: 300px; width: 500px"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def convert_md_to_html(filename):
    with open(filename, "r") as f:
        tempMd = f.read()

    # Finds the heading of the content in order to use as the title of the page
    title = re.search(r'^# (.*)$', tempMd, re.MULTILINE)
    if title:
        title = title.group(1)

    # Translates the markdown text into HTML
    content = markdown2.markdown(tempMd)

    return title, content


def page(request, entry):
    title, content = convert_md_to_html("entries/" + entry + ".md")

    return render(request, "encyclopedia/page.html", {
        "page": util.get_entry(entry),
        "title": title,
        "content": content
    })


def search(request):
    query = request.GET.get('q').lower()
    entries = util.list_entries()

    # Find the exact match of the query
    lower_entries = []

    for entry in entries:
        lower_entries.append(entry.lower())

    if query in lower_entries:
        return redirect("encyclopedia:page", entry=query)

    # Find entries containing the query as a substring
    matching_entries = []

    for entry in entries:
        if query in entry.lower():
            matching_entries.append(entry)

    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "entries": matching_entries
    })


def new(request):
    # Handles when the user submits the form
    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # Check if entry with the provided title already exists
            if util.get_entry(title):
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error": "This title already exists."
                })

            # Save the entry if it doesn't exist
            util.save_entry(title, content)
            return redirect("encyclopedia:page", entry=title)

    # Handles when the user visits the page
    else:
        form = NewPageForm()

    return render(request, "encyclopedia/new_page.html", {
        "form": form
    })


def edit(request):

    return render(request, "encyclopedia/edit_page.html", {
        "form": EditPageForm()
    })
