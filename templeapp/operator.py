from templeapp.common import * 

# pip install googletrans==3.1.0a0
import googletrans
from googletrans import Translator


def optdonationtypedonationreceipt(request):
	donationdata=""
	msg=""
	dl=request.session["receiptlanguage"]
	if request.method == 'POST':
		donationid=request.POST["did"]
		donationdata=DonationRegister.objects.filter(createdby_id=request.session["userid"],softdelete=0,id=donationid)
		scount=donationdata.count()
		dispcount=5-scount;
		dispcount=range(1,dispcount)
		slno=1;
		print(dispcount)
		i=1;
	return render(request,"operator/optdonationtypedonationreceipt.html",{"dl":dl,"donationdata":donationdata,"slno":slno,"dispcount":dispcount})


def optdonationtypesearch(request):
	msg=""
	donationdata=""
	dl=request.session["receiptlanguage"]
	if request.method=="POST":
		action=request.POST['btnsubmit']
		if action=="Cancel":
			did=request.POST["did"]
			if DonationRegister.objects.filter(id=did).exists():
				donationdata=DonationRegister.objects.filter(id=did)
				donationdata.update(softdelete=1,updatedby=request.session["userid"])
				msg="Donation Removed"
				return render(request,"operator/optdonationtypesearch.html",{"dl":dl,"donationdata":donationdata,"msg":msg})
		else:
			search=request.POST["txtsearch"]
			if DonationRegister.objects.filter(softdelete=0,createdby_id=request.session["userid"],donateditem_id=search).exists():
				donationdata=DonationRegister.objects.filter(createdby_id=request.session["userid"],donateditem_id=search,softdelete=0)
			else:
				msg="No Donation On this Day"
	if DonationTypeMaster.objects.filter(softdelete=0).exists():
		donationdatatype=DonationTypeMaster.objects.filter(softdelete=0)
	return render(request,"operator/optdonationtypesearch.html",{"dl":dl,"donationdatatype":donationdatatype,"donationdata":donationdata,"msg":msg})


def optdonationsearch(request):
	msg=""
	donationdata=""
	dl=request.session["receiptlanguage"]
	if request.method=="POST":
		action=request.POST['btnsubmit']
		if action=="Cancel":
			did=request.POST["did"]
			if DonationRegister.objects.filter(id=did).exists():
				donationdata=DonationRegister.objects.filter(id=did)
				donationdata.update(softdelete=1,updatedby=request.session["userid"])
				msg="Donation Seva Disabled"
				return render(request,"operator/optdonationsearch.html",{"dl":dl,"donationdata":donationdata,"msg":msg})
		else:
			fromdate=request.POST["fromdate"]
			todate=request.POST["todate"]
			if DonationRegister.objects.filter(softdelete=0,createdby_id=request.session["userid"],donatedon__range=[fromdate,todate]).exists():
				donationdata=DonationRegister.objects.filter(createdby_id=request.session["userid"],donatedon__range=[fromdate,todate],softdelete=0)
			else:
				msg="No Donation On These Days"
	return render(request,"operator/optdonationsearch.html",{"dl":dl,"donationdata":donationdata,"msg":msg})

def optdonationsearchprint(request):
	donationdata=""
	msg=""
	dl=request.session["receiptlanguage"]
	if request.method == 'POST':
		donationid=request.POST["did"]
		donationdata=DonationRegister.objects.filter(softdelete=0,createdby_id=request.session['userid'],id=donationid)
		scount=donationdata.count()
		dispcount=5-scount;
		dispcount=range(1,dispcount)
		slno=1;
		print(dispcount)
		i=1;
	return render(request,"operator/optdonationsearchprint.html",{"dl":dl,"donationdata":donationdata,"msg":msg})



def optdonationregister(request):
	msg=""
	donationdata=""
	dl=request.session["receiptlanguage"]
	if request.method=="POST":
		if DonationRegister.objects.filter(donorname=request.POST["donorname"],
			memoryof=request.POST["memoryof"],donormobilenumber=request.POST["donormobilenumber"],donateditem_id=request.POST["donateditem"],softdelete=0).exists():
			msg = 'Already Exists'
		else:
			dr=DonationRegister()
			dr.donorname=request.POST["donorname"]
			text_to_translate=request.POST.get('donorname', '')
			translator = Translator()
			result = translator.translate(text_to_translate, src='en', dest='kn')
			dr.donorname_kn = result.text
			dr.memoryof=request.POST["memoryof"]
			text_to_translate1=request.POST.get('memoryof', '')
			translator1 = Translator()
			result1 = translator1.translate(text_to_translate1, src='en', dest='kn')
			dr.memoryof_kn = result1.text
			dr.donormobilenumber=request.POST["donormobilenumber"]
			dr.donateditem_id=request.POST["donateditem"]
			dr.donatedon=request.POST["donatedon"]
			donationdate=request.POST["donatedon"].split("-")
			dr.donationindiandate=donationdate[2]+"-"+donationdate[1]+"-"+donationdate[0]
			dr.note=request.POST["note"]
			dr.createdon=(datetime.now().date())
			dr.createdonindiandate=datetime.now().strftime("%d-%m-%Y")
			dr.createdby_id=request.session["userid"]
			dr.save()
			
			newdonationid=DonationRegister.objects.filter(donormobilenumber=request.POST["donormobilenumber"],createdby_id=request.session['userid']).last().id
			donationdata=DonationRegister.objects.filter(id=newdonationid,softdelete=0)
			return render(request,"operator/optdonationregisterreceipt.html",{"dl":dl,"msg":msg,"donationdata":donationdata})

	if DonationTypeMaster.objects.filter(softdelete=0).exists():
		donationdata=DonationTypeMaster.objects.filter(softdelete=0)
	return render(request,"operator/donationregister.html",{"dl":dl,"msg":msg,"donationdata":donationdata})


def optbalancesheet(request):
    msg = ""
    data = ""
    totalcollectedsum=""
    totalbalance=""
    totalexpensesum=""
    dl=request.session["receiptlanguage"]
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
    return render(request, "operator/optbalancesheet.html", {
    	"dl":dl,
        "data": data,
        "msg": msg,
        "totalcollectedsum":totalcollectedsum,
        "totalexpensesum":totalexpensesum,
        "totalbalance":totalbalance
    })

def optexpenseheadsearch(request):
	msg=""
	expensedata=""
	expensesum=""
	dl=request.session["receiptlanguage"]
	if request.method=="POST":
		action=request.POST['btnsubmit']
		if action=="Cancel":
			did=request.POST["did"]
			if ExpenseDetails.objects.filter(id=did).exists():
				expensedata=ExpenseDetails.objects.filter(id=did)
				expensedata.update(softdelete=1)
				msg="Devotee Seva Disabled"
				return render(request,"operatorsevasearch.html",{"devoteedata":devoteedata,"msg":msg})
		else:
			fromdate=request.POST["fromdate"]
			todate=request.POST["todate"]
			if ExpenseDetails.objects.filter(softdelete=0,paymentdate__range=[fromdate,todate],createdby_id=request.session["userid"]).exists():
				expensedata=ExpenseDetails.objects.filter(paymentdate__range=[fromdate,todate],softdelete=0,createdby_id=request.session["userid"])
			else:
				msg="No Payment On These Days"
			if ExpenseDetails.objects.filter(paymentdate__range=[fromdate,todate],softdelete=0).exists():
				expensesum = expensedata.filter(paymentdate__range=[fromdate,todate],softdelete=0).aggregate(expenses=Sum("amountpaid"))
				if not all(expensesum.values()):
					expensesum=0
				else:
					expensesum=expensesum["expenses"]
	return render(request,"operator/optexpensesearch.html",{"expensesum":expensesum,"dl":dl,"msg":msg,"expensedata":expensedata})

def optexpensehead(request):
    msg=""
    heads=""
    dl=request.session["receiptlanguage"]
    if request.method=="POST":
    	eh=ExpenseDetails()
    	eh.expenseheadid_id=request.POST["expensehead"]
    	eh.paidto=request.POST["paidto"]
    	text_to_translate=request.POST.get('paidto', '')
    	translator = Translator()
    	result = translator.translate(text_to_translate, src='en', dest='kn')
    	eh.paidto_kn = result.text
    	eh.paymentdate=request.POST["paymentdate"]
    	paymentdate=request.POST["paymentdate"].split("-")
    	eh.paymentdatedateindian=paymentdate[2]+"-"+paymentdate[1]+"-"+paymentdate[0]
    	eh.amountpaid=request.POST["amountpaid"]
    	eh.paymentmode=request.POST["paymentmode"]
    	eh.paymentdetails=request.POST["paymentdetails"]
    	eh.createdby_id=request.session["userid"]
    	eh.createdon=(datetime.now().date())
    	eh.save()
    	msg="Expense Details Saved"
    else:
        msg=""
        if ExpenseHead.objects.filter(softdelete=0).exists():
        	heads=ExpenseHead.objects.filter(softdelete=0)
    return render(request,"operator/optexpensehead.html",{"dl":dl,"msg":msg,"heads":heads})


def optdevoteeprintreceipt(request):
	devoteedata=""
	totalamount=""
	sevadetails=""
	slno=""
	dispcount=""
	dl=request.session["receiptlanguage"]
	if request.method == 'POST':
		receiptid=request.POST["rid"]
		devoteedata=DevoteeDetails.objects.filter(softdelete=0,createdby_id=request.session['userid'],id=receiptid)
		sevadetails=DevoteeSevaDetails.objects.filter(softdelete=0,createdby_id=request.session['userid'],devoteeid_id=receiptid)
		scount=sevadetails.count()
		dispcount=12-scount;
		dispcount=range(1,dispcount)
		slno=1;
		print(dispcount)
		i=1;
	return render(request,"operator/optdevoteeprintreceipt.html",{"dl":dl,"sevadetails":sevadetails,"devoteedata":devoteedata,"slno":slno,"dispcount":dispcount})



def optsevasearch(request):
	sevadetails=""
	msg=""
	devoteedata=""
	collectionsum=""
	dl=request.session["receiptlanguage"]
	if request.method=="POST":
		action=request.POST['btnsubmit']
		if action=="Cancel":
			did=request.POST["did"]
			if DevoteeDetails.objects.filter(id=did).exists():
				devoteedata=DevoteeDetails.objects.filter(id=did)
				devoteedata.update(softdelete=1)
				msg="Devotee Seva Disabled"
				return render(request,"operator/optsevasearch.html",{"dl":dl,"devoteedata":devoteedata,"msg":msg})
		else:
			fromdate=request.POST["fromdate"]
			todate=request.POST["todate"]
			if DevoteeDetails.objects.filter(softdelete=0,devoteesevadate__range=[fromdate,todate],createdby_id=request.session["userid"]).exists():
				devoteedata=DevoteeDetails.objects.filter(devoteesevadate__range=[fromdate,todate],createdby_id=request.session["userid"],softdelete=0)
			else:
				msg="No Seva On These Days"
			if DevoteeDetails.objects.filter(devoteesevadate__range=[fromdate,todate],softdelete=0).exists():
				collectionsum = DevoteeDetails.objects.filter(devoteesevadate__range=[fromdate,todate],softdelete=0).aggregate(collections=Sum("devoteetotalamount"))
				if not all(collectionsum.values()):
					collectionsum=0
				else:
					collectionsum=collectionsum["collections"]
	return render(request,"operator/optsevasearch.html",{"collectionsum":collectionsum,"dl":dl,"sevadetails":sevadetails,"msg":msg,"devoteedata":devoteedata})


def optsevaentry(request):
	msg=""
	gotradata=""
	nakshtradata=""
	rashidata=""
	dl=request.session["receiptlanguage"]
	if MstRashi.objects.filter(softdelete=0).exists():
		rashidata=MstRashi.objects.filter(softdelete=0)
		print(rashidata)
	if MstNakshatra.objects.filter(softdelete=0).exists():
		nakshtradata=MstNakshatra.objects.filter(softdelete=0)
	if MstGotra.objects.filter(softdelete=0).exists():
		gotradata=MstGotra.objects.filter(softdelete=0)
	if request.method == 'POST':
		if DevoteeDetails.objects.filter(devoteename_en=request.POST['fullname'],
			devoteemobilenumber=request.POST['Mobile'],devoteesevadate=request.POST['sevadate'],softdelete=0).exists():
			msg = 'Already Exists'
		else:
			dd=DevoteeDetails()
	        # Perform translation
			dd.devoteename_en=request.POST['fullname']
			text_to_translate=request.POST.get('fullname', '')
			translator = Translator()
			result = translator.translate(text_to_translate, src='en', dest='kn')
			dd.devoteename_kn = result.text
			dd.devoteemobilenumber=request.POST['Mobile']
			dd.devoteenakshatra=request.POST['nakshatra']
			dd.devoteegotra=request.POST['gotra']
			dd.devoteerashi=request.POST['rashi']
			dd.devoteesevadate=request.POST['sevadate']
			sevadate=request.POST["sevadate"].split("-")
			dd.devoteedevadateindian=sevadate[2]+"-"+sevadate[1]+"-"+sevadate[0]
			dd.devoteetotalamount=request.POST['dtotalamount']
			dd.dpaymentmode=request.POST['pmode']
			dd.dtransactionno=request.POST['tdetails']
			dd.createdon=(datetime.now().date())
			dd.createdonindiandate=datetime.now().strftime("%d-%m-%Y")
			dd.createdby_id=request.session['userid']
			dd.save()
			newdevoteeid=DevoteeDetails.objects.filter(devoteemobilenumber=request.POST["Mobile"],createdby_id=request.session['userid']).last().id
			sm=SevaMaster.objects.filter(softdelete=0)
			request.session['devoteemobilenumber']=request.POST['Mobile']
			devottemobile=request.session['devoteemobilenumber']
			i=1
			for s in sm:
				tagname="sevaname"+str(s.id);
				sevainfo=request.POST.get(tagname,"0")
				if sevainfo!="0":
					sd=DevoteeSevaDetails()
					sd.sevaid_id=s.id
					sd.slno=i
					sd.devoteetotalamountdetails=s.amount
					sd.devoteeid_id=newdevoteeid
					sd.createdon=(datetime.now().date())
					sd.createdby_id=request.session['userid']
					sd.save()
					i=i+1
					msg="Devotee Seva Details Added"
				request.session["devoteeid"]=newdevoteeid
			date=""
			devoteedata=""
			sevaname=""
			sevaamt=""
			totalamount=""
			sevadetails=""
			if DevoteeDetails.objects.filter(softdelete=0,createdby_id=request.session['userid'],id=request.session["devoteeid"]).exists():
				devoteedata=DevoteeDetails.objects.filter(softdelete=0,createdby_id=request.session['userid'],id=request.session["devoteeid"])
			if DevoteeSevaDetails.objects.filter(softdelete=0,createdby_id=request.session['userid'],devoteeid_id=request.session["devoteeid"]).exists():
				sevadetails=DevoteeSevaDetails.objects.filter(softdelete=0,createdby_id=request.session['userid'],devoteeid_id=request.session["devoteeid"])
			scount=sevadetails.count()
			dispcount=12-scount;
			dispcount=range(1,dispcount)
			slno=1;
			print(dispcount)
			i=1;
			return render(request,"operator/optprintreceipt.html",{"gotradata":gotradata,"nakshtradata":nakshtradata,"rashidata":rashidata,"dl":dl,"sevadetails":sevadetails,"devoteedata":devoteedata,"slno":slno,"dispcount":dispcount})

	sevadata=SevaMaster.objects.filter(softdelete=0)
	return render(request,"operator/optsevaentry.html",{"gotradata":gotradata,"nakshtradata":nakshtradata,"rashidata":rashidata,"dl":dl,"msg":msg,"sevadata":sevadata})





def optchangepassword(request):
    msg=""
    dl=request.session["receiptlanguage"]
    if request.method=="POST":
        usernumber=request.session["optmobilenumber"]
        currentpassword=request.POST["txtcurrentpassword"]
        newpassword=request.POST["txtnewpassword"]
        confirmpassword=request.POST["txtconfirmpassword"]
        if newpassword != confirmpassword:
            msg=" new password & confirm new password  must be same"
        else:
            if UserRegister.objects.filter(mobilenumber=usernumber,password=currentpassword,createdby=request.session['userid'],softdelete=0).exists():
                data=UserRegister.objects.filter(mobilenumber=usernumber,password=currentpassword,createdby=request.session['userid'],softdelete=0)
                data.update(password=newpassword)
                msg="change password successfully"
            else:
                msg="current password  does not match"
    return render(request,"operator/optchangepassword.html",{"msg":msg,"dl":dl})
