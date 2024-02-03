from django.contrib import admin
from django.urls import path
from templeapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
#ADMIN
    path('adminhome',views.adminhome,name="adminhome"),
    path('expensesearch',views.expensesearch),
    path('expensemaster',views.expensemaster),
    path('usermaster',views.usermaster),
    path('userprofile',views.userprofile),
    path('donationmaster',views.donationmaster),
    path('donationsearch',views.donationsearch),
    path('sevadisplay',views.sevadisplay),
    path('sevamster',views.sevamasters),
    path('sevasearch',views.sevasearch),
    path('admsevaserach',views.admsevaserach),
    path('admdevoteeprintreceipt',views.admdevoteeprintreceipt),
    path('admsearchpaymentmaode',views.admsearchpaymentmaode),
    path('admdevoteepaymentprintreceipt',views.admdevoteepaymentprintreceipt),
    path('admchangepassword',views.admchangepassword),
    path('admchangepassword',views.admchangepassword),
    path('admexpensereport',views.admexpensereport),
    path('admbalancesheet',views.admbalancesheet),
    path('admdonationsearch',views.admdonationsearch),
    path('admdonationsearchprint',views.admdonationsearchprint),
    path('admdonationtypesearch',views.admdonationtypesearch),
    path('admdonationtypedonationreceipt',views.admdonationtypedonationreceipt),

    

#OPERATOR

    path('operatorhome',views.operatorhome,name='operatorhome'),
    path('optexpensehead',views.optexpensehead,name='optexpensehead'),
    path('optexpenseheadsearch',views.optexpenseheadsearch),
    path('optchangepassword',views.optchangepassword),
    path('optsevaentry',views.optsevaentry),
    path('optsevasearch',views.optsevasearch),
    path('optdevoteeprintreceipt',views.optdevoteeprintreceipt),
    path('optbalancesheet',views.optbalancesheet),
    path('optdonationregister',views.optdonationregister),
    path('optdonationsearch',views.optdonationsearch),
    path('optdonationsearchprint',views.optdonationsearchprint),
    path('optdonationtypesearch',views.optdonationtypesearch),
    path('optdonationtypedonationreceipt',views.optdonationtypedonationreceipt),




]



    
