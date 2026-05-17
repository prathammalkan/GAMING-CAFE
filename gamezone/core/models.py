from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    accent_color = models.CharField(max_length=7, default="#FF5A36")
    icon = models.CharField(max_length=40, default="spark")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Platform(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=40, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Game(TimeStampedModel):
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=180)
    short_description = models.TextField()
    description = models.TextField()
    studio = models.CharField(max_length=120)
    release_year = models.PositiveIntegerField()
    playtime = models.CharField(max_length=60, default="20+ hrs")
    age_rating = models.CharField(max_length=20, default="16+")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    critic_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    player_rating = models.DecimalField(max_digits=3, decimal_places=1)
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_new_release = models.BooleanField(default=False)
    is_editors_pick = models.BooleanField(default=False)
    hero_badge = models.CharField(max_length=60, default="Featured Drop")
    cover_url = models.URLField()
    banner_url = models.URLField()
    trailer_url = models.URLField(blank=True)
    genres = models.ManyToManyField(Genre, related_name="games")
    platforms = models.ManyToManyField(Platform, related_name="games")

    class Meta:
        ordering = ["-is_featured", "-critic_score", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("game-detail", kwargs={"slug": self.slug})

    @property
    def active_price(self):
        return self.discount_price or self.price


class GalleryImage(TimeStampedModel):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="gallery")
    image_url = models.URLField()
    caption = models.CharField(max_length=120, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.game.title} gallery"


class Review(TimeStampedModel):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    body = models.TextField()
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("game", "user")

    def __str__(self):
        return f"{self.game.title} review by {self.user}"


class Wishlist(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items",
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="wishlisted_by")

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("user", "game")

    def __str__(self):
        return f"{self.user} -> {self.game}"
