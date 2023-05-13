from django.urls import path
from . import views

app_name = 'app1'
urlpatterns = [
    path('' , views.index , name='home'),
    path('services/' , views.services , name='services'),
    path('product/<str:slug>' , views.SelectOption.as_view() , name='select_option'),
    path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
    path('checkout/' , views.checkout , name='checkout'),
    path('checkout-complete/' , views.checkout_complete , name='success_order'),
    path('checkout-completed/' , views.finish_checkout , name='finish_checkout'),
    path('process/' , views.our_process , name='process'),
    path('login/', views.login_view, name='login'),
    path('register/', views.registration, name='register'),
    path('about/', views.about, name='about'),
    path('about/equipment/', views.equipment, name='equipment'),
    path('about/opportunities/', views.opportunity, name='opportunities'),
    path('funding/', views.fund, name='fund'),
    path('contact/', views.contact, name='contact'),
     # learn
    path('learn/', views.learn, name="learn"),
    path('learn/database/', views.database, name="database"),
    path('software/', views.software, name="software"),
    path('research/', views.research, name="research"),
    path('FAQ/', views.FAQ, name="FAQ"),
    path('testimonials/', views.testimonials, name="testimonials"),
    path('awards/', views.awards, name="awards"),
    path('quality/', views.quality, name="quality"),
    path('news/', views.news, name="news"),
    path('spinoff/', views.spinoff, name="spin"),
    path('workshops/', views.workshop, name="workshop"),
    path('metabolomics/', views.metabolomics, name="metabolomics"),
    path('videos/', views.videos, name="videos"),
    path('impact/', views.impact, name="impact"),
    path('publications/', views.publications, name="publications"),
]
