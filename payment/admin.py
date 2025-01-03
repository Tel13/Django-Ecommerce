from django.contrib import admin
from .models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User

# Register the model on the admin section 
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an orderitme inline 
class OredrItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

# Extend our order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    # show the read nly fileds
    readonly_fields = ['date_order']
    fields = ['user', 'full_name', 'email', "shipping_address", 'amount_paid', 'shipped', 'date_shipped']
    inlines = [OredrItemInline]

# Unregister order model
admin.site.unregister(Order)

# re register our order and order items
admin.site.register(Order, OrderAdmin)