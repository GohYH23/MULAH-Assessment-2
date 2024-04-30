from django.shortcuts import render
from dateutil.parser import parse
import feedparser
from titles import __sites


def get_titles(rss):

    feed = feedparser.parse(rss)
    titles = []
    for entry in feed['entries'][:6]:
        desc = ''
        if 'description' in entry:
            desc = entry.description.split('</a>')[-1]
            desc = desc.split('<')[0]
        elif 'summary' in entry:
            desc = entry.summary.split('</a>')[-1]
            desc = desc.split('<')[0]
        if desc == '':
            desc = entry.title

        published = parse(entry.published) if 'published' in entry else parse(entry.pubDate)

        data = {'heading': entry.title, 'summary': desc, 'date': published.day, 'month': published.month, 'publish_date': published, 'url': entry.link}
        titles.append(data)
    return titles


def index(request):
    sites = []
    chk_boxes = []
    if request.method == ' POST':
        for site in __sites:
            isChecked = ''
            if request.POST.get(site.short_name + '-titles-chkbox'):
                sites.append({'name': site.name, 'url': site.url, 'titles_list': get_titles(site.rss_link)})
                isChecked = 'checked'
            chk_boxes.append({'name': site.name, 'shrt_name': site.short_name, 'isChecked': isChecked})
    else:
        for site in __sites:
            sites.append({'name': site.name, 'url': site.url, 'titles_list': get_titles(site.rss_link)})
            chk_boxes.append({'name': site.name, 'shrt_name': site.short_name, 'isChecked': 'checked'})

    return render(request, 'titles.html', {'sites': sites, 'chk_boxes': chk_boxes})
