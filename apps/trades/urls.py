from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter


from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("stock", views.StockViewSet, basename="stock")
router.register("", views.TransactionViewSet, basename="transaction")

urlpatterns = [

]

urlpatterns += router.urls
