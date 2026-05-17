from django.contrib import admin

from .models import GalleryImage, Game, Genre, Platform, Review, Wishlist


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "accent_color")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "studio",
        "release_year",
        "critic_score",
        "is_featured",
        "is_trending",
    )
    list_filter = ("is_featured", "is_trending", "is_new_release", "genres", "platforms")
    search_fields = ("title", "studio", "tagline")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("genres", "platforms")
    inlines = [GalleryImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("game", "user", "score", "created_at")
    list_filter = ("score", "created_at")
    search_fields = ("game__title", "user__username", "title")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "game__title")
