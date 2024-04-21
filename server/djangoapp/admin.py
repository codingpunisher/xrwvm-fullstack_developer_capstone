from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Specifies the number of blank forms to display at the end of the inline.
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'year','car_make')  # Columns shown in the admin list view
    list_filter = ('type', 'year','car_make')  # Filters available on the sidebar
    search_fields = ('name', 'type', 'make__name')  # Searchable fields
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)