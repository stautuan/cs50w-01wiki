import re
import markdown2

from django.shortcuts import render

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
