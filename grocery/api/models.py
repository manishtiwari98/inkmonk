from django.db import models
import uuid,hashlib
class Item(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    priceperunit=models.IntegerField()
    oneUnitQuantity=models.IntegerField()
    measuredIn=models.CharField(max_length=10,default="gram")
    tax=models.DecimalField(max_digits=10,decimal_places=2)
    isMultipliable=models.BooleanField(default=True)
    tax=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    discount=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    unitsAvailable=models.IntegerField(default=0)
    
    def longid(self):
        return "SKU"+self.id
    longid=property(longid)

    def __str__(self):
        return self.name

class Item_History(models.Model):
    itemId=models.ForeignKey(Item,on_delete=models.CASCADE)
    datetime= models.DateTimeField(auto_now_add=True)
    unitsAdded=models.IntegerField()
    def save(self):
        self.itemId.unitsAvailable+=self.unitsAdded
        self.itemId.save()
        super().save()

    

class Invoice(models.Model):
    def longid(self):
        return "ODI"+"{0:06}".format(self.id)
    
    invoiceId=property(longid)
    datetime=models.DateTimeField(auto_now_add=True)
    customerName=models.CharField(max_length=100)
    mobNo=models.CharField(max_length=15,blank=True)
    totAmt=models.DecimalField(max_digits=12,decimal_places=2,default=0)
    totTax=models.DecimalField(max_digits=8,decimal_places=2,default=0)
    totDiscount=models.DecimalField(max_digits=8,decimal_places=2,default=0)

    def __str__(self):
        return self.invoiceId

class InvoiceDetail(models.Model):
    invoiceId=models.ForeignKey(Invoice,on_delete=models.CASCADE)
    itemId=models.ForeignKey(Item,on_delete=models.CASCADE)
    noOfUnits=models.IntegerField()
    
    def save(self):
        self.itemId.unitsAvailable-=self.noOfUnits
        if self.itemId.unitsAvailable < 0:
            raise Exception
        self.itemId.save()
        super().save()

class User(models.Model):
    email=models.EmailField(primary_key=True)
    password=models.CharField(max_length=200)
    authToken=models.CharField(max_length=50,default=uuid.uuid4().hex)
    def save(self):
        self.password=hashlib.md5((self.password).encode('utf-8')).hexdigest()
        super().save()  

