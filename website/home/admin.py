from django.contrib import admin
from .models import *
import admin_thumbnails



class ProductVariantInlines(admin.TabularInline):
    model = Variants
    extra = 2

@admin_thumbnails.thumbnail('image')
class ImageInlines(admin.TabularInline):
    model = Images
    extra = 2


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create', 'update', 'sub_category')
    list_filter = ('create',)
    prepopulated_fields = {
        'slug': ('name',)
    }


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'create', 'update', 'amount', 'available', 'unit_price', 'discount', 'total_price']
    list_filter = ('available',)
    list_editable = ('amount',)
    raw_id_fields = ('category',)
    inlines = [ProductVariantInlines, ImageInlines]


class VariantAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'create', 'rate']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variants, VariantAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Images, )
