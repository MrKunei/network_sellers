from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.core import serializers
from django.urls import reverse
from django.utils.html import format_html
from sellers.models import Seller, Product
from sellers.tasks import update_seller_debt

@admin.action(description='Clear debt')
def clear_debt(modeladmin, request, queryset):
    if len(queryset) < 20:
        queryset.update(debt=0)
    else:
        data = serializers.serialize('json', queryset)
        update_seller_debt.delay(data)


class SellerAdmin(ModelAdmin):
    list_display = ('name', 'email', 'copy_btn', 'employees', 'parent_link', 'level', 'debt',)
    list_display_links = ('name',)
    list_filter = ('city',)
    search_fields = ('name',)
    actions = (clear_debt,)

    def parent_link(self, obj):
        if obj.parent_id != None:
            link = reverse("admin:sellers_seller_change", args=(obj.parent_id,))
            return format_html('<a href="{}">{}</a>', link, obj.parent)
        else:
            return None
    parent_link.short_description = 'supplier'

    def copy_btn(self, obj):
         return format_html('<input type="button" class="btn" value="copy email"></button>')
    copy_btn.short_description = 'copy email'


admin.site.register(Seller, SellerAdmin)
admin.site.register(Product)