import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django.settings')

import django

django.setup()
from rango.models import Category, Page
from random import randint


def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.

    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/",
         "views": randint(50, 100),},
        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/",
         "views": randint(50, 100),},
        {"title": "Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/",
         "views": randint(50, 100),}]

    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
         "views": randint(50, 100),},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/",
         "views": randint(50, 100),},
        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/",
         "views": randint(50, 100),}]

    other_pages = [
        {"title": "Bottle",
         "url": "http://bottlepy.org/docs/dev/",
         "views": randint(50, 100),},
        {"title": "Flask",
         "url": "http://flask.pocoo.org",
         "views": randint(50, 100),}]

    unity_pages = [
        {"title": "Official Unity3D Manual",
         "url": "https://docs.unity3d.com/Manual/index.html",
         "views": randint(50, 100),},
        {"title": "Official Unity3D Scripting API",
         "url": "https://docs.unity3d.com/ScriptReference/index.html",
          "views": randint(50, 100),},
        {"title": "Official Unity3D Tutorial",
         "url": "https://unity3d.com/learn/tutorials",
         "views": randint(50, 100),}]

    cats = {"Python": {"pages": python_pages},
            "Django": {"pages": django_pages},
            "Other Frameworks": {"pages": other_pages},
            "Unity": {"pages": unity_pages}
            }

    for cat, cat_data in cats.items():
        if cat == "Python":
            views = 128
            likes = 64
        elif cat == "Django":
            views = 64
            likes = 32
        elif cat == "Other Frameworks":
            views = 32
            likes = 16
        elif cat == "Unity":
            views = 16
            likes = 8
        c = add_cat(cat, views, likes)
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


# Start execution here!
if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()