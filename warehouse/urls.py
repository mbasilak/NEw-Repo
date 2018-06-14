from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from warehouse.models import Warehouse

urlpatterns = [
                url(r'^$', ListView.as_view(
                                    queryset=Warehouse.objects.all().order_by("-date")[:25],
                                    template_name="warehouse/warehouse.html")),
            ]
