from django.contrib import admin
from petapp.models import Pet, Cart

# Register your models here.
class PetAdmin(admin.ModelAdmin):
   list_display = ['id','name','type','breed','gender','age','price','description','petimage']
   list_filter = ['type','breed','price']
   
class CartAdmin(admin.ModelAdmin):
   list_display = ['id','uid','pid','quantity']
   list_filter = ['uid']
   
admin.site.register(Pet,PetAdmin)
admin.site.register(Cart, CartAdmin)