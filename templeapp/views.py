from templeapp.common import * 
from templeapp.adminapp import * 
from templeapp.operator import * 
from django.conf import settings

def adminhome(request):
    sevacount=""
    totalsevacount=""
    todaysevacount=""
    tommorowsevacount=""
    yearlysevacount=""
    totalcollectedsevaamout=""
    totalcollectedexpenseamout=""
    dl=request.session["adminreceiptlanguage"]

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    year_start = datetime(today.year, 1, 1).date()
    year_end = datetime(today.year, 12, 31).date()

    todaysevacount = DevoteeDetails.objects.filter(devoteesevadate=today,softdelete=0).count()
    tommorowsevacount = DevoteeDetails.objects.filter(devoteesevadate=tomorrow,softdelete=0).count()
    yearlysevacount = DevoteeDetails.objects.filter(devoteesevadate__range=[year_start,year_end],softdelete=0).count()
    totalsevacount = DevoteeDetails.objects.all().count()
    

    todaydonationcount=DonationRegister.objects.filter(donatedon=today,softdelete=0).count()
    tommorowdonationcount=DonationRegister.objects.filter(donatedon=tomorrow,softdelete=0).count()
    yearlydonationcount=DonationRegister.objects.filter(donatedon__range=[year_start,year_end],softdelete=0).count()
    totaldonationcount=DonationRegister.objects.filter(softdelete=0).count()


    devoteedata=DevoteeDetails.objects.all()
    totalcollectedsevaamout = devoteedata.filter(softdelete=0).aggregate(collections=Sum("devoteetotalamount"))
    if not all(totalcollectedsevaamout.values()):
        totalcollectedsevaamout=0
    else:
        totalcollectedsevaamout=totalcollectedsevaamout["collections"]

    todaycollectedsevaamout = devoteedata.filter(devoteesevadate=today,softdelete=0).aggregate(collections=Sum("devoteetotalamount"))
    if not all(todaycollectedsevaamout.values()):
        todaycollectedsevaamout=0
    else:
        todaycollectedsevaamout=todaycollectedsevaamout["collections"]

    tommorowcollectedsevaamout = devoteedata.filter(devoteesevadate=tomorrow,softdelete=0).aggregate(collections=Sum("devoteetotalamount"))
    if not all(tommorowcollectedsevaamout.values()):
        tommorowcollectedsevaamout=0
    else:
        tommorowcollectedsevaamout=tommorowcollectedsevaamout["collections"]

    yearlycollectedsevaamout = devoteedata.filter(devoteesevadate__range=[year_start,year_end],softdelete=0).aggregate(collections=Sum("devoteetotalamount"))
    if not all(yearlycollectedsevaamout.values()):
        yearlycollectedsevaamout=0
    else:
        yearlycollectedsevaamout=yearlycollectedsevaamout["collections"]

    expensedata=ExpenseDetails.objects.all()
    totalcollectedexpenseamout = expensedata.filter(softdelete=0).aggregate(expenses=Sum("amountpaid"))
    if not all(totalcollectedexpenseamout.values()):
        totalcollectedexpenseamout=0
    else:
        totalcollectedexpenseamout=totalcollectedexpenseamout["expenses"]

    todaycollectedexpenseamout = expensedata.filter(paymentdate=today,softdelete=0).aggregate(expenses=Sum("amountpaid"))
    if not all(todaycollectedexpenseamout.values()):
        todaycollectedexpenseamout=0
    else:
        todaycollectedexpenseamout=todaycollectedexpenseamout["expenses"]

    tommorowcollectedexpenseamout = expensedata.filter(paymentdate=tomorrow,softdelete=0).aggregate(expenses=Sum("amountpaid"))
    if not all(tommorowcollectedexpenseamout.values()):
        tommorowcollectedexpenseamout=0
    else:
        tommorowcollectedexpenseamout=tommorowcollectedexpenseamout["expenses"]

    yealrycollectedexpenseamout = expensedata.filter(paymentdate__range=[year_start,year_end],softdelete=0).aggregate(expenses=Sum("amountpaid"))
    if not all(yealrycollectedexpenseamout.values()):
        yealrycollectedexpenseamout=0
    else:
        yealrycollectedexpenseamout=yealrycollectedexpenseamout["expenses"]

    return render(request,"admin/adminhome.html",{"dl":dl,
        "totalcollectedexpenseamout":totalcollectedexpenseamout,
        "todaycollectedexpenseamout":todaycollectedexpenseamout,
        "tommorowcollectedexpenseamout":tommorowcollectedexpenseamout,
        "yealrycollectedexpenseamout":yealrycollectedexpenseamout,
        "todaycollectedsevaamout":todaycollectedsevaamout,
        "tommorowcollectedsevaamout":tommorowcollectedsevaamout,
        "yearlycollectedsevaamout":yearlycollectedsevaamout,
        "todaydonationcount":todaydonationcount,
        "tommorowdonationcount":tommorowdonationcount,
        "yearlydonationcount":yearlydonationcount,
        "todaysevacount":todaysevacount,
        "tommorowsevacount":tommorowsevacount,
        "yearlysevacount":yearlysevacount,
        "totalcollectedsevaamout":totalcollectedsevaamout,
        "totalsevacount":totalsevacount,"sevacount":sevacount,
        "totalcollectedsevaamout":totalcollectedsevaamout,
        "totaldonationcount":totaldonationcount}) 


def operatorhome(request):
    sevacount=""
    totalsevacount=""
    todaysevacount=""
    tommorowsevacount=""
    yearlysevacount=""
    totalcollectedsevaamout=""
    totalcollectedexpenseamout=""
    dl=request.session["receiptlanguage"]

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    year_start = datetime(today.year, 1, 1).date()
    year_end = datetime(today.year, 12, 31).date()

    todaysevacount = DevoteeDetails.objects.filter(createdby_id=request.session['userid'],devoteesevadate=today,softdelete=0).count()
    tommorowsevacount = DevoteeDetails.objects.filter(createdby_id=request.session['userid'],devoteesevadate=tomorrow,softdelete=0).count()
    yearlysevacount = DevoteeDetails.objects.filter(createdby_id=request.session['userid'],devoteesevadate__range=[year_start,year_end],softdelete=0).count()
    totalsevacount = DevoteeDetails.objects.filter(createdby_id=request.session['userid'],softdelete=0).count()
    

    todaydonationcount=DonationRegister.objects.filter(createdby_id=request.session['userid'],donatedon=today,softdelete=0).count()
    tommorowdonationcount=DonationRegister.objects.filter(createdby_id=request.session['userid'],donatedon=tomorrow,softdelete=0).count()
    yearlydonationcount=DonationRegister.objects.filter(createdby_id=request.session['userid'],donatedon__range=[year_start,year_end],softdelete=0).count()
    totaldonationcount=DonationRegister.objects.filter(createdby_id=request.session['userid'],softdelete=0).count()


    devoteedata=DevoteeDetails.objects.all()
    totalcollectedsevaamout = devoteedata.filter(createdby_id=request.session['userid'],softdelete=0).aggregate(collections=Sum("devoteetotalamount"))
    if not all(totalcollectedsevaamout.values()):
        totalcollectedsevaamout=0
    else:
        totalcollectedsevaamout=totalcollectedsevaamout["collections"]

    todaycollectedsevaamout = devoteedata.filter(createdby_id=request.session['userid'],devoteesevadate=today,softdelete=0).aggregate(collections=Sum("devoteetotalamount"))
    if not all(todaycollectedsevaamout.values()):
        todaycollectedsevaamout=0
    else:
        todaycollectedsevaamout=todaycollectedsevaamout["collections"]

    tommorowcollectedsevaamout = devoteedata.filter(createdby_id=request.session['userid'],devoteesevadate=tomorrow,softdelete=0).aggregate(collections=Sum("devoteetotalamount"))
    if not all(tommorowcollectedsevaamout.values()):
        tommorowcollectedsevaamout=0
    else:
        tommorowcollectedsevaamout=tommorowcollectedsevaamout["collections"]

    yearlycollectedsevaamout = devoteedata.filter(createdby_id=request.session['userid'],devoteesevadate__range=[year_start,year_end],softdelete=0).aggregate(collections=Sum("devoteetotalamount"))
    if not all(yearlycollectedsevaamout.values()):
        yearlycollectedsevaamout=0
    else:
        yearlycollectedsevaamout=yearlycollectedsevaamout["collections"]

    expensedata=ExpenseDetails.objects.all()
    totalcollectedexpenseamout = expensedata.filter(createdby_id=request.session['userid'],softdelete=0).aggregate(expenses=Sum("amountpaid"))
    if not all(totalcollectedexpenseamout.values()):
        totalcollectedexpenseamout=0
    else:
        totalcollectedexpenseamout=totalcollectedexpenseamout["expenses"]

    todaycollectedexpenseamout = expensedata.filter(createdby_id=request.session['userid'],paymentdate=today,softdelete=0).aggregate(expenses=Sum("amountpaid"))
    if not all(todaycollectedexpenseamout.values()):
        todaycollectedexpenseamout=0
    else:
        todaycollectedexpenseamout=todaycollectedexpenseamout["expenses"]

    tommorowcollectedexpenseamout = expensedata.filter(createdby_id=request.session['userid'],paymentdate=tomorrow,softdelete=0).aggregate(expenses=Sum("amountpaid"))
    if not all(tommorowcollectedexpenseamout.values()):
        tommorowcollectedexpenseamout=0
    else:
        tommorowcollectedexpenseamout=tommorowcollectedexpenseamout["expenses"]

    yealrycollectedexpenseamout = expensedata.filter(createdby_id=request.session['userid'],paymentdate__range=[year_start,year_end],softdelete=0).aggregate(expenses=Sum("amountpaid"))
    if not all(yealrycollectedexpenseamout.values()):
        yealrycollectedexpenseamout=0
    else:
        yealrycollectedexpenseamout=yealrycollectedexpenseamout["expenses"]

    return render(request,"operator/operatorhome.html",{"dl":dl,
        "totalcollectedexpenseamout":totalcollectedexpenseamout,
        "todaycollectedexpenseamout":todaycollectedexpenseamout,
        "tommorowcollectedexpenseamout":tommorowcollectedexpenseamout,
        "yealrycollectedexpenseamout":yealrycollectedexpenseamout,
        "todaycollectedsevaamout":todaycollectedsevaamout,
        "tommorowcollectedsevaamout":tommorowcollectedsevaamout,
        "yearlycollectedsevaamout":yearlycollectedsevaamout,
        "todaydonationcount":todaydonationcount,
        "tommorowdonationcount":tommorowdonationcount,
        "yearlydonationcount":yearlydonationcount,
        "todaysevacount":todaysevacount,
        "tommorowsevacount":tommorowsevacount,
        "yearlysevacount":yearlysevacount,
        "totalcollectedsevaamout":totalcollectedsevaamout,
        "totalsevacount":totalsevacount,"sevacount":sevacount,
        "totalcollectedsevaamout":totalcollectedsevaamout,
        "totaldonationcount":totaldonationcount}) 


def index(request):
    msg = ''
    userpassword=""
    if request.method == 'POST':
        usermobilenumber = request.POST['txtmobilenumber']
        userpassword = request.POST['txtpassword']
        ur=UserRegister.objects.filter(softdelete=0)
        if UserRegister.objects.filter(mobilenumber=usermobilenumber,softdelete=0,password=userpassword,designation=1).exists():
            data=UserRegister.objects.get(mobilenumber=usermobilenumber,password=userpassword,softdelete=0,designation=1)
            request.session["optmobilenumber"]=request.POST['txtmobilenumber']
            request.session["userid"]=data.id
            request.session["receiptlanguage"]=data.receiptlanguage
            return redirect("operatorhome")

            msg="Loged in Successfully"
        elif UserRegister.objects.filter(mobilenumber=usermobilenumber,password=userpassword,designation=2, softdelete=0).exists():
            data=UserRegister.objects.get(mobilenumber=usermobilenumber,password=userpassword,designation=2, softdelete=0)
            request.session["adminuserid"]=data.id
            request.session["adminreceiptlanguage"]=data.receiptlanguage
            request.session["mobilenumber"]=request.POST['txtmobilenumber']
            return redirect("adminhome")
        else:
            msg="Invalid Login Details"
    return render(request, 'index.html', {'msg': msg})



