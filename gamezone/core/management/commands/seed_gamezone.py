from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import GalleryImage, Game, Genre, Platform

class Command(BaseCommand):
    help = "Seed DEMON ZONE with required games and consoles."

    def add_arguments(self, parser):
        parser.add_argument(
            "--if-empty",
            action="store_true",
            help="Only seed when no games exist yet.",
        )

    def handle(self, *args, **options):
        if options["if_empty"] and Game.objects.exists():
            self.stdout.write("Skipping seed because games already exist.")
            return

        genre_data = [
            ("PC Games", "#FF6B2C", "bolt"),
            ("PS5 Console", "#47D7AC", "gamepad"),
            ("PS4 Console", "#F04F78", "gamepad"),
            ("Car Simulator", "#6C8CFF", "track"),
            ("Bike Simulator", "#FDBB2D", "track"),
            ("Cafeteria", "#E8E1D9", "spark"),
        ]

        genres = {}
        platforms = {}
        for name, color, icon in genre_data:
            genres[name], _ = Genre.objects.get_or_create(
                slug=slugify(name),
                defaults={"name": name, "accent_color": color, "icon": icon},
            )
            platforms[name], _ = Platform.objects.get_or_create(
                slug=slugify(name),
                defaults={"name": name},
            )

        # Base default image for missing ones
        generic_cover = "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=900&q=80"
        generic_banner = "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1600&q=80"

        game_list_raw = [
            ("Valorant", "PC Games", True),
            ("CS GO 2", "PC Games", False),
            ("Rainbow Seige 6", "PC Games", False),
            ("Fortnite", "PC Games", True),
            ("League of Legends", "PC Games", False),

            ("GTA V", "PS5 Console", True),
            ("Last Of Us 2 Remastered", "PS5 Console", True),
            ("Ghost Of Tsuhima", "PS5 Console", False),
            ("Ghost Of Yotei", "PS5 Console", False),
            ("Black Myth Wukong", "PS5 Console", True),
            ("The Witcher", "PS5 Console", False),
            ("God Of War Ragnarok", "PS5 Console", True),

            ("GTA SA", "PS4 Console", False),
            ("GTA VC", "PS4 Console", False),
            ("Counter Strike", "PS4 Console", False),
            ("Hitman", "PS4 Console", False),
            ("WWE", "PS4 Console", False),

            ("F1 26", "Car Simulator", True),
            ("Gran Tourismo", "Car Simulator", False),
            ("Dirt Rally", "Car Simulator", False),

            ("Moto GP 25", "Bike Simulator", True),

            ("Veg Items", "Cafeteria", False),
            ("Colddrinks", "Cafeteria", False),
        ]

        # For variety on the homepage, let's mix the boolean flags
        for i, (title, cat, is_feat) in enumerate(game_list_raw):
            game, _ = Game.objects.update_or_create(
                slug=slugify(title),
                defaults={
                    "title": title,
                    "tagline": f"Experience {title} at DEMON ZONE",
                    "short_description": "Top tier gaming and simulation experience.",
                    "description": f"Enjoy {title} in our premium lounges.",
                    "studio": "DEMON ZONE",
                    "release_year": 2026,
                    "playtime": "Any",
                    "age_rating": "All",
                    "price": 50.00,
                    "discount_price": 40.00,
                    "critic_score": 95,
                    "player_rating": 4.8,
                    "is_featured": is_feat,
                    "is_trending": (i % 2 == 0),
                    "is_new_release": (i % 3 == 0),
                    "is_editors_pick": (i % 4 == 0),
                    "hero_badge": "Available Now",
                    "cover_url": generic_cover,
                    "banner_url": generic_banner,
                },
            )
            game.genres.set([genres[cat]])
            game.platforms.set([platforms[cat]])
            if not game.gallery.exists():
                GalleryImage.objects.create(
                    game=game,
                    image_url=game.banner_url,
                    caption="Signature key art",
                    sort_order=1,
                )
                GalleryImage.objects.create(
                    game=game,
                    image_url=game.cover_url,
                    caption="Cover frame",
                    sort_order=2,
                )

        self.stdout.write(self.style.SUCCESS("DEMON ZONE content is ready."))
