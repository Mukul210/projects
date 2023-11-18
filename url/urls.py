'''
Urls for shortener app urlshortener/urls.py
'''

from django.urls import path

# Import the home view
from .views import *

appname = "shortener"

urlpatterns = [
    # Home view
    path('topic/',  all_topic, name="all_topics"),
    path('topic/<int:topic_id>',  edit_topic, name="edit_topics"),
    path('topic/delete/',  delete_topic, name="delete_topic"),

    path('topic/sl/<slug:slug>', short_links, name="short_links"),
    path('topic/add/',  add_topic, name="add_topic"),

    path('sl/<int:topic_id>',  edit_link, name="edit_link"),
    path('sl/delete/',  delete_link, name="delete_link"),


    path('<str:shortened_part>/', redirect_url_view, name='redirect'),
]
