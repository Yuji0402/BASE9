from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


def home_view(request):
    from teams.models import Team
    from matches.models import MatchPost
    return render(request, 'home.html', {
        'latest_matches': MatchPost.objects.filter(status='open').order_by('-created_at')[:6],
        'latest_teams': Team.objects.order_by('-created_at')[:6],
        'stats': {
            'teams': max(Team.objects.count(), 1),
            'matches': max(MatchPost.objects.count(), 0),
        },
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('teams/', include('teams.urls')),
    path('matches/', include('matches.urls')),
    path('recruitment/', include('recruitment.urls')),
    path('chat/', include('chat.urls')),
    path('grounds/', include('grounds.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
