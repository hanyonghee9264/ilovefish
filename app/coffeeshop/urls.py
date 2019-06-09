from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'coffeeshop'

urlpatterns = [
    path('starbucks/', views.starbucks_list, name='starbucks')
]

urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)