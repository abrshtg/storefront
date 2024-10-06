from django.contrib import admin

from store.models import Customer, Product, Order, Collection


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    list_per_page = 10


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_per_page = 10
    list_select_related = [
        "collection"
    ]  # here we should load 'collection' to prevent extra query for related field.

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory > 10:
            return "HIGH"
        return "LOW"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer_full_name", "placed_at", "payment_status"]
    list_editable = ["payment_status"]
    list_per_page = 10
    list_select_related = ["customer"]

    @admin.display(ordering="customer__first_name")
    def customer_full_name(self, order):
        first_name = order.customer.first_name
        last_name = order.customer.last_name

        return f"{first_name} {last_name}"


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title"]
