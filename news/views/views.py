from django.shortcuts import render
from django.utils.safestring import mark_safe
from . import scrapers

async def news_view(request):

    articles = await scrapers.run_scrapers()
    return render(request, 'news_template.html', articles)
