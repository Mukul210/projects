
from django.shortcuts import render, get_object_or_404  # We will use it later
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
# Model
from .models import Shortener, Category
from .forms import TopicForm

from django.contrib import messages
from .forms import ShortenerForm


# Create your views here.

# def home_view(request):
#     template = 'urlshortener/home.html'
#
#     context = {}
#
#     # Empty form
#     context['form'] = ShortenerForm()
#
#     if request.method == 'GET':
#         return render(request, template, context)
#
#     elif request.method == 'POST':
#
#         used_form = ShortenerForm(request.POST)
#
#         if used_form.is_valid():
#             shortened_object = used_form.save()
#
#             new_url = request.build_absolute_uri('/') + shortened_object.short_url
#
#             long_url = shortened_object.long_url
#
#             context['new_url'] = new_url
#             context['long_url'] = long_url
#
#             return render(request, template, context)
#
#         context['errors'] = used_form.errors
#
#         return render(request, template, context)
#
#

def all_topic(request):
    return render(request, 'topics/list.html')



@login_required(login_url='login')
def add_topic(request):
    topic_form = TopicForm()

    if request.method == "POST":
        topic_form = TopicForm(request.POST)

        if topic_form.is_valid():
            topic = topic_form.save(commit=False)
            topic.user = request.user
            topic.save()
            messages.success(request,f'Topic "{topic.category_name}" has been created.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'form' : topic_form
    }
    return render(request, 'topics/add.html', context)


@login_required(login_url='login')
def edit_topic(request, topic_id):

    topic = get_object_or_404(Category, pk=topic_id )
    topic_form = TopicForm(instance=topic)

    if request.method == "POST":
        topic_form = TopicForm(request.POST, instance=topic)
        if topic_form.is_valid():
            topic_form.save()
            messages.success(request, f'Topic "{topic.category_name}" has been updated.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'form': topic_form
    }
    return render(request, 'topics/edit.html', context)


@login_required(login_url='login')
def delete_topic(request):
    if request.method == "POST":
        topic_id = request.POST.get('topic_id')
        topic = get_object_or_404(Category, pk=topic_id)
        topic.delete()
        messages.success(request, f'{topic.category_name} has been deleted.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))




@login_required(login_url='login')
def edit_link(request, topic_id):

    shortener = get_object_or_404(Shortener, pk=topic_id )
    shortener_form = ShortenerForm(instance=shortener)

    if request.method == "POST":
        shortener_form = ShortenerForm(request.POST, instance=shortener)
        if shortener_form.is_valid():
            shortener_form.save()
            messages.success(request, f'Link has been created.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'form': shortener_form
    }
    return render(request, 'shorturls/edit.html', context)


@login_required(login_url='login')
def delete_link(request):
    if request.method == "POST":
        link_id = request.POST.get('link_id')
        shortener = get_object_or_404(Shortener, pk=link_id)
        shortener.delete()
        messages.success(request, 'Link has been deleted.')
    return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='login')
def short_links(request, slug):
    short_links = None
    topic = Category.objects.get(slug=slug)
    q = request.GET.get('s', False)

    try:
        if q:
            short_links = Shortener.objects.filter(category=topic).filter(title__icontains=q)

        else:
            short_links = Shortener.objects.filter(category=topic)


        paginator = Paginator(short_links, 50)  # Show 25 contacts per page.

        page_number = request.GET.get('page')
        short_links = paginator.get_page(page_number)
    except Shortener.ObjectDoesNotExist:
        pass

    context = {
        'short_links':short_links,
        'host':request.build_absolute_uri('/'),
        'topic': topic,
    }

    return render(request, 'shorturls/list.html', context)



def redirect_url_view(request, shortened_part):
    try:
        shortener = Shortener.objects.get(short_url=shortened_part)

        shortener.times_followed += 1

        shortener.save()

        return HttpResponseRedirect(shortener.long_url)

    except:
        raise Http404('Sorry this link is broken :(')