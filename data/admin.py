from django.contrib import admin
from data.models import Data, Train


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ("label", "text", "creator", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")

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


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ("task_id", "user", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")

    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
