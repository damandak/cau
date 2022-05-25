from django.urls import path
from avisos.views import IndexView, MyNoticesView, AllNoticesView, DetailNoticeView, CreateShortNoticeView, UpdateShortNoticeView, MemberAutocomplete, CarsAutocomplete,SendNoticeView

app_name = 'avisos'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('avisos/', AllNoticesView.as_view(), name='avisos'),
    path('avisos/misavisos/', MyNoticesView.as_view(), name='myavisos'),
    path('avisos/nuevo_rapido/', CreateShortNoticeView.as_view(), name='new_shortnotice'),
    path('avisos/<int:pk>/editar', UpdateShortNoticeView.as_view(), name='edit_shortnotice'),
    path('avisos/<int:pk>/enviar', SendNoticeView.as_view(), name='send_shortnotice'),
    path('avisos/<int:pk>/', DetailNoticeView.as_view(), name='detail_notice'),
    path('avisos/member_autocomplete/', MemberAutocomplete.as_view(), name='member_autocomplete'),
    path('avisos/cars_autocomplete/', CarsAutocomplete.as_view(), name='cars_autocomplete'),
]