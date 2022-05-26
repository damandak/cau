from django.contrib import admin
from django.urls import include, path
from avisos.views.base import IndexView
from avisos.views.account import UpdateAccountView, UpdateMedicalView, CarsView, CreateCarView, UpdateCarView, DeleteCarView, EmergencyContactsView, CreateEmergencyContactView, UpdateEmergencyContactView, DeleteEmergencyContactView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('acceso/', include('django.contrib.auth.urls')),
    path('', include('avisos.urls')),
    path('', IndexView.as_view(), name='index'),
    path('cuenta/panel', UpdateAccountView.as_view(), name='account_data'),
    path('cuenta/salud/', UpdateMedicalView.as_view(), name='medical_data'),
    path('cuenta/vehiculos/', CarsView.as_view(), name='cars_data'),
    path('cuenta/vehiculos/nuevo', CreateCarView.as_view(), name='new_car'),
    path('cuenta/vehiculos/<int:pk>/', UpdateCarView.as_view(), name='edit_car'),
    path('cuenta/vehiculos/<int:pk>/eliminar', DeleteCarView.as_view(), name='delete_car'),
    path('cuenta/contactos/', EmergencyContactsView.as_view(), name='emergencycontacts_data'),
    path('cuenta/contactos/nuevo', CreateEmergencyContactView.as_view(), name='new_emergencycontact'),
    path('cuenta/contactos/<int:pk>/', UpdateEmergencyContactView.as_view(), name='edit_emergencycontact'),
    path('cuenta/contactos/<int:pk>/eliminar', DeleteEmergencyContactView.as_view(), name='delete_emergencycontact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
