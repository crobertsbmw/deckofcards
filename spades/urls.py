from django.conf.urls import include
from django.urls import path, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from deck.views import doc_page


urlpatterns = [
    path('', doc_page, name="docs"),  # Root URL without regex
    path('api/', include("deck.urls")),  # API URLs
    path('admin/', admin.site.urls),  # Admin URLs
    # path('', TemplateView.as_view(template_name='docs.html'), name='docs'),  # Converted if needed
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
