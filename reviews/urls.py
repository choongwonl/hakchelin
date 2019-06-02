from django.urls import path
from django.views.generic.detail import DetailView

from reviews.views import *
from reviews.models import CustomReview, CustomCheck

app_name = 'reviews'

urlpatterns = [
    path('', home, name='home'),
    path('today/', today, name='today'),
    path('upload/', ReviewUploadView.as_view(), name='review_upload'),
    path('reviews/', lastreviews, name='lastreviews'),
    path('ranking/', ranking, name='ranking'),
    path('check/', check, name='check'),
    path('detail/', detailView, name='detailView'),
    path('mypage/', mypage, name='mypage'),
    path('myreviews/', myreviews, name='myreviews'),
    path('howtoearnpoint/', howtoearnpoint, name='howtoearnpoint'),
]