from django.urls import path
from petapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('details/<rid>', views.showPetDetails),
    path('register/', views.registerUser),
    path('login/',views.userLogin),
    path('logout/', views.userLogout),
    path('addtocart/<petid>',views.addToCart),
    path('showcart/',views.showUserCart),
    path('removepet/<cartid>',views.removeCart),
    path('updatecart/<opr>/<cartid>',views.updateCart),
    path('search/<pet_type>',views.searchByType),
    path('range',views.searchByRange),
    path('sort/<dir>',views.sortByPrice),
    path('confirmorder/',views.confirmOrder),
    path('makepayment/', views.makepayment),
    path('placeorder/',views.placeOrder),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
