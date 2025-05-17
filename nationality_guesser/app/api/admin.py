from django.contrib import admin
from django.utils.html import format_html
from .models import Country, NameNationality

from django.contrib.admin import AdminSite


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "country_code",
        "name",
        "created_at",
    )
    list_filter = ("region", "is_independent")
    search_fields = ("name", "country_code", "capital")
    readonly_fields = (
        "created_at",
        "updated_at",
        "flag_preview",
        "coat_of_arms_preview",
    )
    fieldsets = (
        ("Basic Info", {"fields": ("country_code", "name", "full_name")}),
        (
            "Geography",
            {
                "fields": (
                    "region",
                    "subregion",
                    "is_independent",
                    "capital",
                    ("capital_latitude", "capital_longitude"),
                    "border",
                )
            },
        ),
        ("Maps", {"fields": ("google_maps_link", "openstreetmap_link")}),
        ("Flags", {"fields": ("flag_png", "flag_svg", "flag_alt", "flag_preview")}),
        (
            "Coat of Arms",
            {
                "fields": (
                    "coat_of_arms_png",
                    "coat_of_arms_org",
                    "coat_of_arms_preview",
                )
            },
        ),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def flag_preview(self, obj):
        if obj.flag_png:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>', obj.flag_png
            )
        return "-"

    flag_preview.short_description = "Flag Preview"

    def coat_of_arms_preview(self, obj):
        if obj.coat_of_arms_png:
            return format_html(
                '<img src="{}" style="max-height: 50px;"/>', obj.coat_of_arms_png
            )
        return "-"

    coat_of_arms_preview.short_description = "Coat of Arms Preview"


class NameNationalityAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "probability_bar", "count", "last_accessed")
    list_filter = ("country",)
    search_fields = ("name", "country__name")
    readonly_fields = ("created_at", "last_accessed")
    list_per_page = 50
    date_hierarchy = "last_accessed"

    fieldsets = (
        (None, {"fields": ("name", "country", "probability", "count")}),
        (
            "Metadata",
            {"fields": ("last_accessed", "created_at"), "classes": ("collapse",)},
        ),
    )

    def probability_bar(self, obj):
        percent = int(obj.probability * 100)
        color = "success" if percent > 70 else "warning" if percent > 40 else "danger"
        return format_html(
            '<div class="progress" style="width: 100px; height: 20px;">'
            '<div class="progress-bar bg-{}" role="progressbar" style="width: {}%" '
            'aria-valuenow="{}" aria-valuemin="0" aria-valuemax="100">{}</div></div>',
            color,
            percent,
            percent,
            f"{percent}%",
        )

    probability_bar.short_description = "Probability"
    probability_bar.admin_order_field = "probability"


# Регистрация моделей
admin.site.register(Country, CountryAdmin)
admin.site.register(NameNationality, NameNationalityAdmin)
