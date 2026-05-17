from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from django.db import OperationalError

from .models import Game, Genre, Platform


class CoreViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        genre = Genre.objects.create(name="Action", slug="action")
        platform = Platform.objects.create(name="PC", slug="pc")
        game = Game.objects.create(
            title="Neon Rift",
            slug="neon-rift",
            tagline="A pulse-racing cyber arena.",
            short_description="Fast tactical combat in a luminous city.",
            description="Detailed description for testing page rendering.",
            studio="Pulse Forge",
            release_year=2026,
            playtime="18 hrs",
            age_rating="16+",
            price=49.99,
            critic_score=92,
            player_rating=4.8,
            is_featured=True,
            is_trending=True,
            cover_url="https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=900&q=80",
            banner_url="https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1400&q=80",
        )
        game.genres.add(genre)
        game.platforms.add(platform)

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GameZone")

    def test_browse_page_loads(self):
        response = self.client.get(reverse("browse"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Neon Rift")

    def test_detail_page_loads(self):
        response = self.client.get(reverse("game-detail", kwargs={"slug": "neon-rift"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pulse Forge")

    @patch("core.views.Game.objects.count", side_effect=OperationalError("db not ready"))
    def test_home_page_handles_database_startup_error(self, _mock_count):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Database setup is not complete yet")
