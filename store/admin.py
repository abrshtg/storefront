from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from store.models import Customer, Product, Order, Collection, OrderItem


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    lt_ten = "<10"

    def lookups(self, request, model_admin):
        return [(self.lt_ten, "Low")]

    def queryset(self, request, queryset):
        if self.value() == self.lt_ten:
            return queryset.filter(inventory__lt=10)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "order_count"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    list_per_page = 10
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    @admin.display(ordering="order_count")
    def order_count(self, customer):
        url = reverse("admin:store_order_changelist")
        query = f"?{urlencode({'customer__id': customer.id})}"
        return format_html(f"<a href={url + query}>{customer.order_count}</a>")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_count=Count("order"))


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ["clear_inventory"]
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_filter = ["collection", "last_update", InventoryFilter]
    list_per_page = 10
    list_select_related = [
        "collection"
    ]  # here we should load 'collection' to prevent extra query for related field.
    prepopulated_fields = {"slug": ["title"]}
    search_fields = ["title", "collection_title"]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory > 10:
            return "HIGH"
        return "LOW"

    @admin.action(description="clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, f"{updated_count} products were successfully updated."
        )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ["product"]
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]
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
    list_display = ["title", "product_count"]

    @admin.display(ordering="product_count")
    def product_count(self, collection):
        url = reverse("admin:store_product_changelist")
        query = f"?{urlencode({'collection__id': str(collection.id)})}"
        return format_html(f"<a href={url + query}>{collection.product_count}</a>")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count("product"))
