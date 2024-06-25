from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="Dashboard"),
    path("logged", views.homelogged, name="dashboardlogged"),
    path("aboutUs/", views.aboutus, name="aboutus"),
    path("aboutUslogged", views.aboutUslogged, name="aboutUslogged"),
    path("login/", views.login, name="login"),
    path("explore/", views.explore, name="explore"),
    path("explorelogged/", views.explorelogged, name="explorelogged"),
    path("transaction/<int:umkm_id>/", views.transaction, name="transaction"),
    path("tingkatkanmodal/", views.tingkatkanmodal, name="tingkatkanmodal"),
    path("umkmprofile/<int:umkm_id>/", views.umkmprofile, name="umkmprofile"),
    path("userdetail/", views.userdetail, name="userdetail"),
    path("userdashboard/<int:profile_id>/", views.userdashboard, name="userdashboard"),
    path("investporto/", views.investporto, name="investporto"),
    path("detailporto/", views.detailPorto, name="detailporto"),
    path("growth/", views.growth, name="growth"),
    path("topupOption/", views.topupOption, name="topupOption"),
    path("topupPayment/", views.topupPayment, name="topupPayment"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("withdraw-form/", views.withdrawForm, name="withdraw-form"),
    path("withdraw-success/", views.withdrawSuccess, name="withdraw-success"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)