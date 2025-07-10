from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Topic, Newspaper, Redactor


admin.site.register(Topic)


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("title", "short_content", "published_date",)
    search_fields = ("topic__name",)
    list_filter = ("publishers__username",)

    def short_content(self, obj):
        content = obj.content
        return (
            content[:50] + "..."
            if len(content) > 50
            else content
        )
    short_content.short_description = "Content"


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("years_of_experience",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "years_of_experience",
                    )
                },
            ),
        )
    )
