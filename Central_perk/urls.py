from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from chat import views as chat_views
# from feed import views as feed_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('feed.urls')),
	# path('', include('chat.urls')),
	# TODO : move user related urls to users/urls.py
	path('users/', user_views.users_list, name='users_list'),
	path('users/<slug>/', user_views.profile_view, name='profile_view'),
	path('users/<int:id>/delete/', user_views.profile_delete, name='profile_delete'),
	path('friends/', user_views.friend_list, name='friend_list'),
	# path('<str:room_name>/', chat_views.room,name='room'),
	path('edit-profile/', user_views.edit_profile, name='edit_profile'),
	# path('edit-profile/', user_views.edit_bio_profile, name='edit_bio_profile'),
	
	path('my-profile/', user_views.my_profile, name='my_profile'),
	path('search_users/', user_views.search_users, name='search_users'),
	path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/login.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
	path('follow-list/', user_views.follow_list, name='follow_list'),
	path('users/follow-request/<int:id>/', user_views.follow_request, name='follow_request'),
	path('users/unfollow-request/<int:id>/', user_views.un_follow_request, name='un_follow_request'),
	# path('users/<slug>/', user_views.profile_view_2, name='profile_view_2'),
	# path('chat', chat_views.chat_view, name='chats'),
    # path('chat/<int:sender>/<int:receiver>', chat_views.message_view, name='chat'),
    # path('api/messages/<int:sender>/<int:receiver>', chat_views.message_list, name='message-detail'),
    # path('api/messages', chat_views.message_list, name='message-list'),
	path('messages/', include('chat.urls')),	
]
# messages/

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
