from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home),
    path('home', views.home,name='home'),
    path('Sofa1-detail/<int:pk>', views.Sofa1DetailView.as_view(), name='Sofa1-detail'),
    path('Lamp-detail/<int:pk>', views.LampsDetailView.as_view(), name='Lamp-detail'),
    path('Kitchen-detail/<int:pk>', views.KitchenDetailView.as_view(), name='Kitchen-detail'),
    path('Kids-detail/<int:pk>', views.KidsDetailView.as_view(), name='Kids-detail'),
    path('Indoor-detail/<int:pk>', views.IndoorPlantDetailView.as_view(), name='Indoor-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('contactus/', views.Contact_Us, name='contactus'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('Sofa/', views.Sofa, name='Sofa'),
    path('Lamps/', views.Lamps, name='Lamps'),
    path('Kitchen/', views.Kitchen, name='Kitchen'),
    path('Kids/', views.Kids, name='Kids'),
    path('IndoorPlants/', views.IndoorPlants, name='IndoorPlants'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="login"), name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name ="customerregistration"),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
