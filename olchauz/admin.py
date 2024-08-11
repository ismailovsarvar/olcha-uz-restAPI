from django.contrib import admin

from olchauz.models import (
    Product,
    Category,
    Group,
    Comment,
    Image,
    Key,
    Value,
    Attribute
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug')
    search_fields = ('title', 'slug')
    list_filter = ('title', 'created_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'price', 'discount', 'created_at')
    search_fields = ('name', 'slug',)
    list_filter = ('price', 'created_at')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'slug')
    list_filter = ('title', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('message', 'rating', 'created_at')
    search_fields = ('message',)
    list_filter = ('rating', 'created_at')


admin.site.register(Image)

admin.site.register(Key)
admin.site.register(Value)
admin.site.register(Attribute)