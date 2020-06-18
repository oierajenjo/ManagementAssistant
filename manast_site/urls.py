from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

from manast_site import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('calendar', views.calendar, name='calendar'),

    path('login/', views.login_register, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile_view, name='profile_view'),
    path('edit_user/', views.edit_user, name='edit_user'),

    path('shop/<int:pk>/', views.shop_view, name='shop'),
    path('shop/<int:pk>/upload/', views.data_upload, name='data_upload'),
    path('shop/<int:pk>/edit_shop/', views.edit_shop, name='edit_shop'),
    path('shop/<int:pk>/holiday/', views.holiday, name='holiday'),
    path('shop/new_shop', views.new_shop, name='new_shop'),
    path('shop/<int:pk>/delete_shop/', views.delete_shop, name='delete_shop'),

    path('shop/<int:pk>/sales/', views.sales_table, name='sales'),
    path('shop/<int:pk>/expenses/', views.expenses_table, name='expenses'),
    path('shop/<int:pk>/stats/', views.stats_table, name='stats'),
    path('shop/<int:pk>/predictions/', views.predictions_table, name='predictions'),

    # path('export', views.download_csv, name='download_csv'),

    url(r'^password_reset/$',
        auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),
        name='password_reset'),
    url(r'^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),
        name='password_reset_confirm'),
    url(r'^reset/done/$',
        auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
        name='password_reset_complete'),
]