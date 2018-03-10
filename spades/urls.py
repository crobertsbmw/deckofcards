from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^api/', include('deck.urls', namespace='deck')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='docs.html'), name='docs'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
