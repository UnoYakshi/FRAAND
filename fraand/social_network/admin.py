from django.contrib import admin

from social_network.models import Item, Tag, Image


class InlineImage(admin.TabularInline):
    model = Image


class ItemAdmin(admin.ModelAdmin):
    inlines = [InlineImage]


admin.site.register(Item, ItemAdmin)
admin.site.register(Tag)
