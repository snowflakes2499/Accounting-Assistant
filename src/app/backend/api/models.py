from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_quantity = models.IntegerField()
    product_tax = models.DecimalField(max_digits=10, decimal_places=2)

class Client(models.Model):
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=15)
    client_address = models.TextField()

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100)
    invoice_date = models.DateField()
    invoice_due_date = models.DateField()
    invoice_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    invoice_products = models.ManyToManyField(Product)
    invoice_total = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_status = models.CharField(max_length=20)

class Vendor(models.Model):
    vendor_name = models.CharField(max_length=100)
    vendor_email = models.EmailField()
    vendor_phone = models.CharField(max_length=15)
    vendor_address = models.TextField()