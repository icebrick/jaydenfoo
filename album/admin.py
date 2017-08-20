#-*- coding: utf-8 -*-
from django.contrib import admin
from .models import Album, Photo

# Register your models here.
class PhotoInline(admin.StackedInline):
    model = Photo
    fieldsets = [
            ('Name Description', {'fields': ['name', 'desc', 'as_cover'], 'classes':['collapse']}),
            (None,               {'fields': ['image']}),
            ]

#在admin页面使photo内联在Album中
class AlbumAdmin(admin.ModelAdmin):
    fieldsets = [
            (None,          {'fields': ['name', 'e_name']}),
            ('Description', {'fields': ['desc'], 'classes':['collapse']}),
            ]

    inlines = [
            PhotoInline,
            ]
admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo)
