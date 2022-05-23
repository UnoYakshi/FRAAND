from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from social_network.models import Deal, Image, Item


class InlineImage(admin.TabularInline):
    model = Image


# @admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [
        InlineImage,
    ]

    def children_display(self, obj):
        display_text = ', '.join(
            [
                "<a href={}>{}</a>".format(
                    reverse(
                        'admin:{}_{}_change'.format(obj._meta.app_label, obj._meta.model_name),
                        args=(child.pk,),
                    ),
                    child.name,
                )
                for child in obj.children.all()
            ]
        )
        if display_text:
            return mark_safe(display_text)
        return "-"


admin.site.register(Item, ItemAdmin)
admin.site.register(Deal)
