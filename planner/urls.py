from django.urls import path
from . import views

app_name = 'planner'

urlpatterns = [
    path('create/', views.planner_form, name='create'),
    path('result/<str:share_code>/', views.result, name='result'),
    path('share/<str:share_code>/', views.share, name='share'),
    path('reaction/<str:share_code>/', views.add_reaction, name='add_reaction'),
    path('letter/generate/<str:share_code>/', views.generate_letter, name='generate_letter'),
    path('letter/<str:share_code>/', views.view_letter, name='view_letter'),
    path('anonymous/<str:share_code>/', views.make_anonymous, name='make_anonymous'),
    path('reveal/<str:share_code>/', views.reveal_sender, name='reveal_sender'),
]
