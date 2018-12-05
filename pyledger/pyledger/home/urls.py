from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('expense/add/',views.addexpense, name="addexpense"),
    path('expense/delete',views.deleteexpense, name="deleteexpense"),
    path('split/create/', views.createsplit, name="createsplit"),
    path('splits/manage/<int:pk>', views.managesplits, name="managesplits"),
    path('splits/transaction/add/<int:pk>',views.addsplittrans, name="addsplittrans"),
    path('splits/transaction/delete',views.deletesplittrans, name="deletesplittrans"),
    path('splits/deletemember',views.deletemember, name="deletemember")
]
