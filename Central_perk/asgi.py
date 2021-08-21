"""
ASGI config for photoshare project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""



import os
from django.conf.urls import url
from chat.consumers import ChatConsumer
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter , URLRouter
from django.core.asgi import get_asgi_application
application = ProtocolTypeRouter({ 
    "http": get_asgi_application(),
    'websocket':AllowedHostsOriginValidator(
     AuthMiddlewareStack(
         URLRouter([
            url(r"^messages/(?P<username>[\w.@+-]+)", ChatConsumer.as_asgi()),
         ]
         )
     )
    )
})



# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# import chat.routing


# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     )
# })
# import os

# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photoshare.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     # Just HTTP for now. (We can add other protocols later.)
# })




# import os

# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     # Just HTTP for now. (We can add other protocols later.)
# })


# from django.conf.urls import url
# from channels.routing import ProtocolTypeRouter , URLRouter
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator , OrigniValidator
# from django.core.asgi import get_asgi_application
# from chat.consumers import ChatConsumer

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     # Just HTTP for now. (We can add other protocols later.)
#     'websocket':AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(
#                 [
#                     url(r"^messages(?P<username>[\w.@+-]+)/$", ChatConsumer),
#                 ]
#             )
#         )
#     )
# })









# import os
# import django

# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from channels.routing import get_default_applications
# import chat.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photoshare.settings')
# django.setup()
# application = get_default_applications()
# application = get_asgi_application()
# application = ProtocolTypeRouter({
#    "http": get_asgi_application(),
#   "websocket": AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     ),
# })