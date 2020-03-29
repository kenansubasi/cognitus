from django.contrib import admin
from data.models import Data


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ("label", "text", "creator", "created_at", "updated_at")

    readonly_fields = ("creator", "created_at", "updated_at")
    search_fields = (
        "label", "text", "creator__username", "creator__email", "creator__first_name", "creator__last_name"
    )

    def get_fields(self, request, obj=None):
        fields = ("text", "label")
        if obj is not None:
            fields += ("creator", "created_at", "updated_at")
        return fields

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)
