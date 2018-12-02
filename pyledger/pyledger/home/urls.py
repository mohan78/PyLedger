from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('addexpense/',views.addexpense, name="addexpense"),
    path('split/create/', views.createsplit, name="createsplit"),
    path('splits/manage/<int:pk>', views.managesplits, name="managesplits"),
    path('splits/addtransaction',views.addsplittrans, name="addsplittrans"),
]
