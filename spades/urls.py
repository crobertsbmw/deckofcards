from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from deck.views import doc_page
urlpatterns = [
    url(r'^$', doc_page, name="docs"),
    url(r'^api/', include("deck.urls")),
    url(r'^admin/', admin.site.urls),
    # url(r'^$', TemplateView.as_view(template_name='docs.html'), name='docs'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
