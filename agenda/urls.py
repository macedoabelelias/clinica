from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.agenda_view,
        name='agenda'
    ),

     path(
        'novo/',
        views.novo_agendamento,
        name='novo_agendamento'
    ),

]