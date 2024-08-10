from django.contrib import admin

from olchauz.models import Product, Category, Group, Comment, Image


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug')
    search_fields = ('title', 'slug')
    list_filter = ('title', 'created_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug', )
    list_display = ('name', 'price', 'discount', 'created_at')
    search_fields = ('name', 'slug',)
    list_filter = ('price', 'created_at')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title', 'slug')
    list_filter = ('title', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('message', 'rating', 'created_at')
    search_fields = ('message',)
    list_filter = ('rating', 'created_at')


admin.site.register(Image)
