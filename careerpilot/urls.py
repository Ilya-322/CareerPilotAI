from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from core.views import (
    create_simulation,
    register_view,
    profile_view,
    simulation_view,
    results_view,
    save_answer,
    dashboard_view          # ← обязательно
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=False
    ), name='login'),
    path('register/', register_view, name='register'),

    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # Главный дашборд
    path('dashboard/', dashboard_view, name='dashboard'),

    path('profile/', profile_view, name='profile'),
    path('create-simulation/', create_simulation, name='create_simulation'),
    path('select-simulation/', TemplateView.as_view(template_name='select_simulation.html'), name='select_simulation'),

    path('simulation/<uuid:simulation_id>/', simulation_view, name='simulation'),
    path('results/<uuid:simulation_id>/', results_view, name='results'),

    path('save-answer/', save_answer, name='save_answer'),
]