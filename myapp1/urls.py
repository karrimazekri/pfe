from django.urls import path, include 
from .views import  index, get_token 
from .views import   PatientViewSet , UserViewSet, SharedCasViewSet,CasListView,CasCreateView,SharedCasListView,CasViewSet
from rest_framework import routers
from .import views
router = routers.DefaultRouter()
router.register("users" ,UserViewSet, basename="users")
router.register("patient" ,PatientViewSet, basename="patient")
router.register("cas", CasViewSet, basename="cas")
router.register('sharedcase', SharedCasViewSet, basename='sharedcase')
#router.register("sharedcaseDetail/<str:pk>",SharedCaseDetail,basename="sharedcaseDetail")

urlpatterns = [
    path('myapp1/', include(router.urls)),
    path('api/', include(router.urls)),
    path('home/', index, name="home"),
    path('token/', get_token, name="token"),
    #path('myapp/api/sharedcaseDetail/<str:pk>/',sharedcaseDetail,name="sharedcaseDetail")
    path('caslist/', CasListView.as_view(), name='caslist'),
    path('casCreate/', CasCreateView.as_view(), name='casCreate'),
    path('sharedcaslist/', SharedCasListView.as_view(), name='sharedcaslist'),
    path('api/create-notification/', views.create_notification, name='create-notification'),
   
   
]