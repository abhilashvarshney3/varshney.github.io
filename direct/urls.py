from django.urls import path
from direct.views import inbox, Directs, SendDirect, NewConversation

urlpatterns = [
    path('', inbox, name='inbox'),
    path('directs/<username>', Directs, name='directs'),
    path('send/', SendDirect, name='send_direct'),
    path('new/<username>', NewConversation, name='newconversation'),
    
]
