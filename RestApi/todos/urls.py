from django.conf.urls import url
from todos import views

urlpatterns = [
    url(r'^api/todos$', views.todo_list),
    url(r'^api/todos/(?P<pk>[0-9]+)$', views.todo_detail),
    url(r'^api/todos/finished$', views.todo_list_finished)
]
