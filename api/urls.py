from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'build$', views.build),
    url(r'overview$', views.overview),
    url(r'main$', views.main),
    url(r'ready$', views.ready),
    url(r'sale$', views.sale),
    url(r'trade$', views.tradeApi),
    url(r'account$', views.account),
    url(r'result$', views.result),
    url(r'login$', views.login),
    url(r'auction$', views.auctionApi),
    url(r'myAuctionList$', views.myAuctionList),
    url(r'AuctionList$', views.AuctionList),
    url(r'check$', views.check),
    url(r'dealInit$', views.dealInit),
    url(r'dealMessage$', views.dealMessage),
    url(r'dealOut$', views.dealOut),
    url(r'retDeal$', views.retDeal),
    url(r'next$', views.next),
    url(r'ranking$', views.ranking),
    url(r'produce$', views.produceMaterial),
    url(r'adminin$', views.adminlogin),
    url(r'myProduceList$', views.myProduceList),
    url(r'userSetting$', views.userSetting),
    url(r'deletegame$', views.deletegame),
]
