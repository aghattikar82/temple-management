from django.db import models

class MstRashi(models.Model):
	rashi_kn=models.CharField(max_length=100)
	rashi_en=models.CharField(max_length=100)
	createdby=models.IntegerField(default=1)
	softdelete=models.IntegerField(default=0)
	def __str__(self):
		return self.rashi_kn

class MstNakshatra(models.Model):
	nakshatra_kn=models.CharField(max_length=100)
	nakshatra_en=models.CharField(max_length=100)
	createdby=models.IntegerField(default=1)
	softdelete=models.IntegerField(default=0)
	def __str__(self):
		return self.nakshatra_kn

class MstGotra(models.Model):
	gotra_kn=models.CharField(max_length=100)
	gotra_en=models.CharField(max_length=100)
	createdby=models.IntegerField(default=1)
	softdelete=models.IntegerField(default=0)
	def __str__(self):
		return self.gotra_kn

class UserRegister(models.Model):
	fullname=models.CharField(max_length=200)
	mobilenumber=models.CharField(max_length=15,default="")
	designation=models.CharField(max_length=15,default="")
	password=models.CharField(max_length=50)
	address=models.CharField(max_length=500)
	receiptlanguage=models.CharField(max_length=500,default="kn")
	softdelete=models.IntegerField(default=0)
	createdon=models.CharField(max_length=50,default="  ")
	createdby=models.CharField(max_length=50,default="Admin")
	upadated=models.CharField(max_length=50,default="  ")
	updatedby=models.CharField(max_length=100,default="")
	deletedon=models.CharField(max_length=50,default="  ")
	deletedby=models.CharField(max_length=100,default="")
	def __str__(self):
		return self.fullname

class SevaMaster(models.Model):
	sevaname_kn=models.CharField(max_length=200)
	sevaname_en=models.CharField(max_length=200,default="")
	amount=models.CharField(max_length=15,default="")
	softdelete=models.IntegerField(default=0)
	createdon=models.CharField(max_length=50,default="  ")
	createdby=models.ForeignKey(UserRegister,on_delete=models.PROTECT)
	upadated=models.CharField(max_length=50,default="  ")
	updatedby=models.CharField(max_length=100,default="")
	deletedon=models.CharField(max_length=50,default="  ")
	deletedby=models.CharField(max_length=100,default="")
	def __str__(self):
		return self.sevaname_kn


class DevoteeDetails(models.Model):
	devoteename_en=models.CharField(max_length=200)
	devoteename_kn=models.CharField(max_length=200,default="")
	devoteemobilenumber=models.CharField(max_length=200)
	devoteenakshatra=models.CharField(max_length=200)
	devoteegotra=models.CharField(max_length=200)
	devoteegotra_en=models.CharField(max_length=200,default="")
	devoteerashi=models.CharField(max_length=200)
	devoteesevadate=models.CharField(max_length=200)
	devoteedevadateindian=models.CharField(max_length=200,default=0)
	createdonindiandate=models.CharField(max_length=200,default=0)
	devoteetotalamount=models.FloatField(max_length=200)
	dpaymentmode=models.CharField(max_length=200)
	dtransactionno=models.CharField(max_length=200)
	softdelete=models.IntegerField(default=0)
	createdon=models.CharField(max_length=50,default="  ")
	createdby=models.ForeignKey(UserRegister,on_delete=models.PROTECT)
	upadated=models.CharField(max_length=50,default="  ")
	updatedby=models.CharField(max_length=100,default="")
	deletedon=models.CharField(max_length=50,default="  ")
	deletedby=models.CharField(max_length=100,default="")
	def __str__(self):
		return self.devoteename_kn

class DevoteeSevaDetails(models.Model):
	slno=models.IntegerField(default=0)
	devoteeid=models.ForeignKey(DevoteeDetails,on_delete=models.PROTECT,default=0)
	devoteetotalamountdetails=models.FloatField(default=0)
	sevaid=models.ForeignKey(SevaMaster,on_delete=models.PROTECT)
	softdelete=models.IntegerField(default=0)
	createdon=models.CharField(max_length=50,default="")
	createdby=models.ForeignKey(UserRegister,on_delete=models.PROTECT)
	upadated=models.CharField(max_length=50,default="")
	updatedby=models.CharField(max_length=100,default="")
	deletedon=models.CharField(max_length=50,default="")
	deletedby=models.CharField(max_length=100,default="")


class DonationTypeMaster(models.Model):
	donamtiontype=models.CharField(max_length=200)
	donamtiontype_kn=models.CharField(max_length=200,default="kn")
	softdelete=models.IntegerField(default=0)
	createdon=models.CharField(max_length=50,default="  ")
	createdby=models.ForeignKey(UserRegister,on_delete=models.PROTECT)
	upadated=models.CharField(max_length=50,default="  ")
	updatedby=models.CharField(max_length=100,default="")
	deletedon=models.CharField(max_length=50,default="  ")
	deletedby=models.CharField(max_length=100,default="")


class ExpenseHead(models.Model):
	expensehead=models.CharField(max_length=200)
	expensehead_kn=models.CharField(max_length=200,default="kn")
	softdelete=models.IntegerField(default=0)
	createdon=models.CharField(max_length=50,default="  ")
	createdby=models.ForeignKey(UserRegister,on_delete=models.PROTECT)
	upadated=models.CharField(max_length=50,default="  ")
	updatedby=models.CharField(max_length=100,default="")
	deletedon=models.CharField(max_length=50,default="  ")
	deletedby=models.CharField(max_length=100,default="")

class ExpenseDetails(models.Model):
	expenseheadid=models.ForeignKey(ExpenseHead,on_delete=models.PROTECT,default="0")
	paidto=models.CharField(max_length=200)
	paidto_kn=models.CharField(max_length=200,default="operator")
	paymentdate=models.CharField(max_length=200)
	paymentdatedateindian=models.CharField(max_length=200,default=0)
	amountpaid=models.CharField(max_length=200)
	paymentmode=models.CharField(max_length=200)
	paymentdetails=models.CharField(max_length=200)
	softdelete=models.IntegerField(default=0)
	createdon=models.CharField(max_length=50,default="")
	createdby=models.ForeignKey(UserRegister,on_delete=models.PROTECT)
	upadated=models.CharField(max_length=50,default="  ")
	updatedby=models.CharField(max_length=100,default="")
	deletedon=models.CharField(max_length=50,default="  ")
	deletedby=models.CharField(max_length=100,default="")
	def __str__(self):
		return self.paidto

class DonationRegister(models.Model):
	donorname=models.CharField(max_length=50,default="  ")
	donorname_kn=models.CharField(max_length=50,default="kannada")
	memoryof=models.CharField(max_length=50,default="")
	memoryof_kn=models.CharField(max_length=50,default="kannadamemoryof")
	donormobilenumber=models.CharField(max_length=50,default="  ")
	donateditem=models.ForeignKey(DonationTypeMaster,on_delete=models.PROTECT)
	donatedon=models.CharField(max_length=50,default="  ")
	donationindiandate=models.CharField(max_length=50,default="  ")
	note=models.CharField(max_length=50,default="  ")
	softdelete=models.IntegerField(default=0)
	createdon=models.CharField(max_length=50,default="")
	createdonindiandate=models.CharField(max_length=50,default="")
	createdby=models.ForeignKey(UserRegister,on_delete=models.PROTECT)
	upadated=models.CharField(max_length=50,default="  ")
	updatedby=models.CharField(max_length=100,default="")
	deletedon=models.CharField(max_length=50,default="  ")
	deletedby=models.CharField(max_length=100,default="")
	def __str__(self):
		return self.donorname_kn

class Temptabletotalamount(models.Model):
	totalamount=models.FloatField(default=0)
	expenseamount=models.FloatField(default=0)
	balanceamount=models.FloatField(default=0)
	fromdate=models.CharField(max_length=1000,default="") 
	createdby=models.FloatField(default=0)
