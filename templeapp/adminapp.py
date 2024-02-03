from templeapp.common import * 




def admdonationtypedonationreceipt(request):
	donationdata=""
	msg=""
	dl=request.session["adminreceiptlanguage"]
	if request.method == 'POST':
		donationid=request.POST["did"]
		donationdata=DonationRegister.objects.filter(softdelete=0,id=donationid)
		scount=donationdata.count()
		dispcount=5-scount;
		dispcount=range(1,dispcount)
		slno=1;
		print(dispcount)
		i=1;
	return render(request,"admin/admdonationtypedonationreceipt.html",{"dl":dl,"donationdata":donationdata,"slno":slno,"dispcount":dispcount})


def admdonationtypesearch(request):
	msg=""
	donationdata=""
	dl=request.session["adminreceiptlanguage"]
	if request.method=="POST":
		action=request.POST['btnsubmit']
		if action=="Cancel":
			did=request.POST["did"]
			if DonationRegister.objects.filter(id=did).exists():
				donationdata=DonationRegister.objects.filter(id=did)
				donationdata.update(softdelete=1,updatedby=request.session["userid"])
				msg="Donation Removed"
				return render(request,"admin/admdonationtypesearch.html",{"dl":dl,"donationdata":donationdata,"msg":msg})
		else:
			search=request.POST["txtsearch"]
			if DonationRegister.objects.filter(softdelete=0,donateditem_id=search).exists():
				donationdata=DonationRegister.objects.filter(donateditem_id=search,softdelete=0)
			else:
				msg="No Donation On this Day"
	if DonationTypeMaster.objects.filter(softdelete=0).exists():
		donationdatatype=DonationTypeMaster.objects.filter(softdelete=0)
	return render(request,"admin/admdonationtypesearch.html",{"dl":dl,"donationdatatype":donationdatatype,"donationdata":donationdata,"msg":msg})


def admdonationsearchprint(request):
	donationdata=""
	msg=""
	dl=request.session["adminreceiptlanguage"]
	if request.method == 'POST':
		donationid=request.POST["did"]
		donationdata=DonationRegister.objects.filter(softdelete=0,id=donationid)
		scount=donationdata.count()
		dispcount=5-scount;
		dispcount=range(1,dispcount)
		slno=1;
		print(dispcount)
		i=1;
	return render(request,"admin/admdonationsearchprint.html",{"dl":dl,"donationdata":donationdata,"msg":msg})


def admdonationsearch(request):
	msg=""
	donationdata=""
	dl=request.session["adminreceiptlanguage"]
	if request.method=="POST":
		action=request.POST['btnsubmit']
		if action=="Cancel":
			did=request.POST["did"]
			if DonationRegister.objects.filter(id=did).exists():
				donationdata=DonationRegister.objects.filter(id=did)
				donationdata.update(softdelete=1,updatedby=request.session["adminuserid"])
				msg="Donation Seva Disabled"
				return render(request,"admin/admsevasearch.html",{"dl":dl,"donationdata":donationdata,"msg":msg})
		else:
			fromdate=request.POST["fromdate"]
			todate=request.POST["todate"]
			if DonationRegister.objects.filter(softdelete=0,donatedon__range=[fromdate,todate]).exists():
				donationdata=DonationRegister.objects.filter(donatedon__range=[fromdate,todate],softdelete=0)
			else:
				msg="No Donation On These Days"
	return render(request,"admin/admdonationsearch.html",{"dl":dl,"donationdata":donationdata,"msg":msg})





def admbalancesheet(request):
    msg = ""
    data = ""
    totalcollectedsum=""
    totalbalance=""
    totalexpensesum=""
    dl=request.session["adminreceiptlanguage"]
    if request.method == "POST":
        fdate= request.POST["fromdate"].replace("/","-").split("-")
        fromdate=date(int(fdate[0]),int(fdate[1]),int(fdate[2]))

        tdate = request.POST["todate"].replace("/","-").split("-")
        todate=date(int(tdate[0]),int(tdate[1]),int(tdate[2]))

        devoteedata = DevoteeDetails.objects.filter(devoteesevadate__range=[fromdate, todate], softdelete=0)
        expensedata = ExpenseDetails.objects.filter(paymentdate__range=[fromdate, todate], softdelete=0)
        totaldata = Temptabletotalamount.objects.all()
        
        Temptabletotalamount.objects.all().delete()

        while fromdate <= todate:
        	if devoteedata.filter(devoteesevadate=fromdate,softdelete=0).exists():
        		collectionsum = devoteedata.filter(devoteesevadate=fromdate,softdelete=0).aggregate(collections=Sum("devoteetotalamount"))
	        	if not all(collectionsum.values()):
	        		collectionsum=0
        		else:
        			collectionsum=collectionsum["collections"]
        	else:
        		collectionsum=0
        	if expensedata.filter(paymentdate=fromdate,softdelete=0).exists():
        		expensesum = expensedata.filter(paymentdate=fromdate,softdelete=0).aggregate(expenses=Sum("amountpaid"))
        		if not all(expensesum.values()):
        			expensesum=0
	        	else:
	        		expensesum=expensesum["expenses"]
        	else:
        		expensesum=0
        	balancesum=float(collectionsum)-float(expensesum)
        	tt = Temptabletotalamount()
        	tt.totalamount = collectionsum
        	tt.expenseamount = expensesum
        	tt.balanceamount=balancesum
        	tt.fromdate = fromdate.strftime("%d-%m-%Y")
        	tt.createdby = request.session["adminuserid"]
        	tt.save()
        	fromdate += timedelta(days=1)

        data = Temptabletotalamount.objects.all()
        if totaldata.all().exists():
        	totalcollectedsum = totaldata.all().aggregate(totalcollection=Sum("totalamount"))
        	if not all(totalcollectedsum.values()):
        		totalcollectedsum=0
        	else:
        		totalcollectedsum=totalcollectedsum["totalcollection"]
        if totaldata.all().exists():
        	totalexpensesum = totaldata.all().aggregate(totalexpense=Sum("expenseamount"))
        	if not all(totalexpensesum.values()):
        		totalexpensesum=0
        	else:
        		totalexpensesum=totalexpensesum["totalexpense"]
        totalbalance=float(totalcollectedsum)-float(totalexpensesum)
        print(data)
    return render(request, "admin/admbalancesheet.html", {
    	"dl":dl,
        "data": data,
        "msg": msg,
        "totalcollectedsum":totalcollectedsum,
        "totalexpensesum":totalexpensesum,
        "totalbalance":totalbalance
    })

def admexpensereport(request):
	msg=""
	expensedata=""
	expensesum=""
	dl=request.session["adminreceiptlanguage"]
	if request.method=="POST":
		action=request.POST['btnsubmit']
		if action=="Cancel":
			eid=request.POST["eid"]
			if ExpenseDetails.objects.filter(id=eid).exists():
				expensedata=ExpenseDetails.objects.filter(id=eid)
				expensedata.update(softdelete=1,updatedby=request.session["adminuserid"])
				msg="Devotee Seva Disabled"
				return render(request,"admin/admexpensereport.html",{"expensedata":expensedata,"dl":dl,"msg":msg})
		else:
			fromdate=request.POST["fromdate"]
			todate=request.POST["todate"]
			if ExpenseDetails.objects.filter(softdelete=0,paymentdate__range=[fromdate,todate]).exists():
				expensedata=ExpenseDetails.objects.filter(paymentdate__range=[fromdate,todate],softdelete=0)
			else:
				msg="No Payment On These Days"
			if ExpenseDetails.objects.filter(paymentdate__range=[fromdate,todate],softdelete=0).exists():
				expensesum = expensedata.filter(paymentdate__range=[fromdate,todate],softdelete=0).aggregate(expenses=Sum("amountpaid"))
				if not all(expensesum.values()):
					expensesum=0
				else:
					expensesum=expensesum["expenses"]
	return render(request,"admin/admexpensereport.html",{"expensesum":expensesum,"msg":msg,"dl":dl,"expensedata":expensedata})


def admchangepassword(request):
    msg=""
    dl=request.session["adminreceiptlanguage"]
    if request.method=="POST":
        usernumber=request.session["mobilenumber"]
        print(usernumber)
        currentpassword=request.POST["txtcurrentpassword"]
        newpassword=request.POST["txtnewpassword"]
        confirmpassword=request.POST["txtconfirmpassword"]
        if newpassword != confirmpassword:
            msg=" new password & confirm new password  must be same"
        else:
            if UserRegister.objects.filter(mobilenumber=usernumber,password=currentpassword,softdelete=0).exists():
                data=UserRegister.objects.filter(mobilenumber=usernumber,password=currentpassword,softdelete=0)
                data.update(password=newpassword)
                msg="change password successfully"
            else:
                msg="current password  does not match"
    return render(request,"admin/admchangepassword.html",{"msg":msg,"dl":dl})

def expensesearch(request):
    msg=""
    expensedata=""
    dl=request.session["adminreceiptlanguage"]
    if request.method=="POST":
    	action=request.POST['btnsubmit']
    	if action=="Disable":
    		eid=request.POST["eid"]
    		if ExpenseHead.objects.filter(id=eid).exists():
    			expensedata=ExpenseHead.objects.filter(id=eid)
    			expensedata.update(softdelete=1,updatedby=request.session["adminuserid"])
    			msg="Expense Disabled Successfully"
    			return render(request,"admin/expensesearch.html",{"expensedata":expensedata,"dl":dl,"msg":msg})
    	else:
	    	search=request.POST['txtsearch']
    		if ExpenseHead.objects.filter(expensehead=search,softdelete=0).exists():
    			expensedata=ExpenseHead.objects.filter(expensehead=search,softdelete=0)
    		elif ExpenseHead.objects.filter(expensehead_kn=search,softdelete=0).exists():
    				expensedata=ExpenseHead.objects.filter(expensehead_kn=search,softdelete=0)
    		else:
    			msg="Record Not Found"
    return render(request,"admin/expensesearch.html",{"expensedata":expensedata,"dl":dl,"msg":msg})



def expensemaster(request):
	msg=""
	dl=request.session["adminreceiptlanguage"]
	if request.method=="POST":
		if ExpenseHead.objects.filter(expensehead=request.POST["expensehead"],softdelete=0).exists():
			msg = 'Already Exists'
		else:
			eh=ExpenseHead()
			eh.expensehead=request.POST["expensehead"]
			eh.expensehead_kn=request.POST["expense_kn"]
			eh.createdon=(datetime.now().date())
			eh.createdby_id=request.session["adminuserid"]
			eh.save()
			msg="Expense Added"
	return render(request,"admin/expensemaster.html",{"msg":msg,"dl":dl})

def donationmaster(request):
	msg=""
	dl=request.session["adminreceiptlanguage"]
	if request.method=="POST":
		if DonationTypeMaster.objects.filter(donamtiontype=request.POST["donamtiontype"],softdelete=0).exists():
			msg = 'Already Exists'
		else:
			dm=DonationTypeMaster()
			dm.donamtiontype=request.POST["donamtiontype"]
			dm.donamtiontype_kn=request.POST["donamtiontype_kn"]
			dm.createdon=(datetime.now().date())
			dm.createdby_id=request.session["adminuserid"]
			dm.save()
			msg="Donation Type Added"
	return render(request,"admin/donationmaster.html",{"msg":msg,"dl":dl})

def donationsearch(request):
    msg=""
    donationdata=""
    dl=request.session["adminreceiptlanguage"]
    if request.method=="POST":
    	action=request.POST['btnsubmit']
    	if action=="Disable":
    		did=request.POST["did"]
    		if DonationTypeMaster.objects.filter(id=did).exists():
    			donationdata=DonationTypeMaster.objects.filter(id=did)
    			donationdata.update(softdelete=1,updatedby=request.session["adminuserid"])
    			msg="Donation Type Disabled Successfully"
    			return render(request,"admin/donationsearch.html",{"donationdata":donationdata,"dl":dl,"msg":msg})
    	else:
	    	search=request.POST['txtsearch']
    		if DonationTypeMaster.objects.filter(donamtiontype=search,softdelete=0).exists():
    			donationdata=DonationTypeMaster.objects.filter(donamtiontype=search,softdelete=0)
    		else:
    			msg="Record Not Found"
    return render(request,"admin/donationsearch.html",{"donationdata":donationdata,"dl":dl,"msg":msg})

def sevamasters(request):
	msg=""
	dl=request.session["adminreceiptlanguage"]
	if request.method=="POST":
		if SevaMaster.objects.filter(sevaname_en=request.POST["sevaname_en"],sevaname_kn=request.POST["sevaname_kn"],softdelete=0).exists():
			msg = 'Already Exists'
		else:
			sm=SevaMaster()
			sm.sevaname_en=request.POST["sevaname_en"]
			sm.sevaname_kn=request.POST["sevaname_kn"]
			sm.amount=request.POST["amount"]
			sm.createdon=(datetime.now().date())
			sm.createdby_id=request.session["adminuserid"]
			sm.save()
			msg="Seva Added"
	return render(request,"admin/sevamaster.html",{"msg":msg,"dl":dl})


def sevasearch(request):
    msg=""
    sevadata=""
    dl=request.session["adminreceiptlanguage"]
    if request.method=="POST":
    	action=request.POST['btnsubmit']
    	if action=="Disable":
    		sid=request.POST["sid"]
    		if SevaMaster.objects.filter(id=sid).exists():
    			sevadata=SevaMaster.objects.filter(id=sid)
    			sevadata.update(softdelete=1,updatedby=request.session["adminuserid"])
    			msg="Seva Disabled Successfully"
    			return render(request,"admin/sevasearch.html",{"sevadata":sevadata,"msg":msg,"dl":dl})
    	else:
	    	search=request.POST['txtsearch']
    		if SevaMaster.objects.filter(sevaname_en__contains=search,softdelete=0).exists():
    			sevadata=SevaMaster.objects.filter(sevaname_en__contains=search,softdelete=0)
    		elif SevaMaster.objects.filter(sevaname_kn=search,softdelete=0).exists():
    			sevadata=SevaMaster.objects.filter(sevaname_kn=search,softdelete=0)
    		else:
    			msg="Record Not Found"
    return render(request,"admin/sevasearch.html",{"sevadata":sevadata,"msg":msg,"dl":dl})


def usermaster(request):
	msg=""
	dl=request.session["adminreceiptlanguage"]
	if request.method=="POST":
		if UserRegister.objects.filter(fullname=request.POST["fullname"],mobilenumber=request.POST["Mobile"],designation=request.POST["designation"],softdelete=0).exists():
			msg = 'Already Registered'
		else:
			ur=UserRegister()
			ur.fullname=request.POST["fullname"]
			ur.mobilenumber=request.POST["Mobile"]
			ur.designation=request.POST["designation"]
			ur.password=request.POST["Password"]
			ur.address=request.POST["address"]
			ur.receiptlanguage=request.POST["receiptlanguage"]
			ur.createdon=(datetime.now().date())
			ur.save()
			msg="User Successfully Added"
	return render(request,"admin/usermaster.html",{"msg":msg,"dl":dl} )

def userprofile(request):
    msg=""
    Userdata=""
    dl=request.session["adminreceiptlanguage"]
    if request.method=="POST":
    	action=request.POST['btnsubmit']
    	if action=="Disabled":
    		uid=request.POST["uid"]
    		if UserRegister.objects.filter(id=uid).exists():
    			Userdata=UserRegister.objects.filter(id=uid)
    			Userdata.update(softdelete=1)
    			msg="User Disabled Successfully"
    			return render(request,"admin/userprofile.html",{"dl":dl,"Userdata":Userdata,"msg":msg})
    	else:
	    	search=request.POST['txtsearch']
	    	fieldname=request.POST['ddlfield']
	    	if fieldname=="name":
	    		if UserRegister.objects.filter(fullname=search,softdelete=0).exists():
	    			Userdata=UserRegister.objects.filter(fullname=search,softdelete=0)
	    		else:
	    			msg="Record Not Found"
	    	elif fieldname=="mobilenumber":
	    		if UserRegister.objects.filter(mobilenumber=search,softdelete=0).exists():
	    			Userdata=UserRegister.objects.filter(mobilenumber=search,softdelete=0)
	    		else:
	    			msg="Record Not Found"
    return render(request,"admin/userprofile.html",{"dl":dl,"Userdata":Userdata,"msg":msg})

def sevadisplay(request):
	devoteedata=""
	sevadetails=""
	sevadetails=DevoteeSevaDetails.objects.filter(softdelete=0)
	devoteedata=DevoteeDetails.objects.filter(softdelete=0)
	return render(request,"admin/sevadisplay.html",{"dl":dl,"devoteedata":devoteedata,"sevadetails":sevadetails})


def admdevoteeprintreceipt(request):
	devoteedata=""
	totalamount=""
	sevadetails=""
	dl=request.session["adminreceiptlanguage"]
	if request.method == 'POST':
		receiptid=request.POST["rid"]
		if DevoteeDetails.objects.filter(softdelete=0,id=receiptid).exists():
			devoteedata=DevoteeDetails.objects.filter(softdelete=0,id=receiptid)
		if DevoteeSevaDetails.objects.filter(softdelete=0,devoteeid_id=receiptid).exists():
			sevadetails=DevoteeSevaDetails.objects.filter(softdelete=0,devoteeid_id=receiptid)
			scount=sevadetails.count()
			dispcount=12-scount;
			dispcount=range(1,dispcount)
			slno=1;
			print(dispcount)
			i=1;
	return render(request,"admin/admdevoteeprintreceipt.html",{"dl":dl,"sevadetails":sevadetails,"devoteedata":devoteedata,"slno":slno,"dispcount":dispcount})

def admdevoteepaymentprintreceipt(request):
	devoteedata=""
	totalamount=""
	sevadetails=""
	slno=""
	dispcount=""
	dl=request.session["adminreceiptlanguage"]
	if request.method == 'POST':
		receiptid=request.POST["rid"]
		if DevoteeDetails.objects.filter(softdelete=0,id=receiptid).exists():
			devoteedata=DevoteeDetails.objects.filter(softdelete=0,id=receiptid)
		if DevoteeSevaDetails.objects.filter(softdelete=0,devoteeid_id=receiptid).exists():
			sevadetails=DevoteeSevaDetails.objects.filter(softdelete=0,devoteeid_id=receiptid)
			scount=sevadetails.count()
			dispcount=12-scount;
			dispcount=range(1,dispcount)
			slno=1;
			print(dispcount)
			i=1;
	return render(request,"admin/admdevoteepaymentprintreceipt.html",{"dl":dl,"sevadetails":sevadetails,"devoteedata":devoteedata,"slno":slno,"dispcount":dispcount})


def admsearchpaymentmaode(request):
	sevadetails=""
	msg=""
	devoteedata=""
	collectionsum=""
	dl=request.session["adminreceiptlanguage"]
	if request.method=="POST":
		action=request.POST['btnsubmit']
		if action=="Cancel":
			did=request.POST["did"]
			if DevoteeDetails.objects.filter(id=did).exists():
				devoteedata=DevoteeDetails.objects.filter(id=did)
				devoteedata.update(softdelete=1,updatedby=request.session["adminuserid"])
				msg="Payment Deleted"
				return render(request,"admin/admsearchpaymentmaode.html",{"dl":dl,"devoteedata":devoteedata,"msg":msg})
		else:
			search=request.POST["txtsearch"]
			if DevoteeDetails.objects.filter(softdelete=0,dpaymentmode=search).exists():
				devoteedata=DevoteeDetails.objects.filter(dpaymentmode=search,softdelete=0)
			else:
				msg="No Seva On These Days"
			if devoteedata.filter(dpaymentmode=search,softdelete=0).exists():
				collectionsum = devoteedata.filter(dpaymentmode=search,softdelete=0).aggregate(collections=Sum("devoteetotalamount"))
				if not all(collectionsum.values()):
					collectionsum=0
				else:
					collectionsum=collectionsum["collections"]
	return render(request,"admin/admsearchpaymentmaode.html",{"collectionsum":collectionsum,"dl":dl,"sevadetails":sevadetails,"msg":msg,"devoteedata":devoteedata})

def admsevaserach(request):
	sevadetails=""
	msg=""
	devoteedata=""
	collectionsum=""
	dl=request.session["adminreceiptlanguage"]
	if request.method=="POST":
		action=request.POST['btnsubmit']
		if action=="Cancel":
			did=request.POST["did"]
			if DevoteeDetails.objects.filter(id=did).exists():
				devoteedata=DevoteeDetails.objects.filter(id=did)
				devoteedata.update(softdelete=1,updatedby=request.session["adminuserid"])
				msg="Devotee Seva Disabled"
				return render(request,"admin/admsevasearch.html",{"dl":dl,"devoteedata":devoteedata,"msg":msg})
		else:
			fromdate=request.POST["fromdate"]
			todate=request.POST["todate"]
			if DevoteeDetails.objects.filter(softdelete=0,devoteesevadate__range=[fromdate,todate]).exists():
				devoteedata=DevoteeDetails.objects.filter(devoteesevadate__range=[fromdate,todate],softdelete=0)
			else:
				msg="No Seva On These Days"
			if devoteedata.filter(devoteesevadate__range=[fromdate,todate],softdelete=0).exists():
				collectionsum = devoteedata.filter(devoteesevadate__range=[fromdate,todate],softdelete=0).aggregate(collections=Sum("devoteetotalamount"))
				if not all(collectionsum.values()):
					collectionsum=0
				else:
					collectionsum=collectionsum["collections"]
	return render(request,"admin/admsevasearch.html",{"collectionsum":collectionsum,"dl":dl,"sevadetails":sevadetails,"msg":msg,"devoteedata":devoteedata})

def expensesearch(request):
    msg=""
    expensedata=""
    dl=request.session["adminreceiptlanguage"]
    if request.method=="POST":
    	action=request.POST['btnsubmit']
    	if action=="Disable":
    		eid=request.POST["eid"]
    		if ExpenseHead.objects.filter(id=eid).exists():
    			expensedata=ExpenseHead.objects.filter(id=eid)
    			expensedata.update(softdelete=1,createdby_id=request.session["adminuserid"])
    			msg="Expense Disabled Successfully"
    			return render(request,"admin/expensesearch.html",{"expensedata":expensedata,"msg":msg})
    	else:
	    	search=request.POST['txtsearch']
    		if ExpenseHead.objects.filter(expensehead=search,softdelete=0).exists():
    			expensedata=ExpenseHead.objects.filter(expensehead=search,softdelete=0)
    		else:
    			msg="Record Not Found"
    return render(request,"admin/expensesearch.html",{"expensedata":expensedata,"msg":msg,"dl":dl})