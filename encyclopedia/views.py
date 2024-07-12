import re
import markdown2

from django.shortcuts import render, redirect
from .models import Entry

from . import util


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


def page(request, topic):
    title, content = convert_md_to_html("entries/" + topic + ".md")

    return render(request, "encyclopedia/page.html", {
        "page": util.get_entry(topic),
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
        return redirect("page", topic=query)

    # Find entries containing the query as a substring
    matching_entries = []

    for entry in entries:
        if query in entry.lower():
            matching_entries.append(entry)

    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "entries": matching_entries
    })
