from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import OperationalError, ProgrammingError
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ReviewForm
from .models import Game, Genre, Platform, Review, Wishlist


def home(request):
    context = {
        "featured_game": None,
        "trending_games": [],
        "new_releases": [],
        "editors_picks": [],
        "genres": [],
        "total_games": 0,
        "total_reviews": 0,
        "total_platforms": 0,
        "database_ready": True,
    }

    try:
        games = (
            Game.objects.prefetch_related("genres", "platforms")
            .annotate(review_average=Avg("reviews__score"), review_count=Count("reviews"))
        )
        context.update(
            {
                "featured_game": games.filter(is_featured=True).first() or games.first(),
                "trending_games": games.filter(is_trending=True)[:4],
                "new_releases": games.filter(is_new_release=True)[:4],
                "editors_picks": games.filter(is_editors_pick=True)[:3],
                "genres": Genre.objects.annotate(game_count=Count("games"))[:6],
                "total_games": Game.objects.count(),
                "total_reviews": Review.objects.count(),
                "total_platforms": Platform.objects.count(),
            }
        )
    except (OperationalError, ProgrammingError):
        context["database_ready"] = False

    return render(request, "core/home.html", context)


def health_check(request):
    return JsonResponse({"status": "ok"})


def browse_games(request):
    games = Game.objects.prefetch_related("genres", "platforms").all()
    genres = Genre.objects.all()
    platforms = Platform.objects.all()

    query = request.GET.get("q", "").strip()
    selected_genre = request.GET.get("genre", "").strip()
    selected_platform = request.GET.get("platform", "").strip()
    sort = request.GET.get("sort", "featured").strip()

    if query:
        games = games.filter(
            Q(title__icontains=query)
            | Q(tagline__icontains=query)
            | Q(studio__icontains=query)
            | Q(genres__name__icontains=query)
        )

    if selected_genre:
        games = games.filter(genres__slug=selected_genre)

    if selected_platform:
        games = games.filter(platforms__slug=selected_platform)

    sort_map = {
        "featured": ["-is_featured", "-critic_score", "title"],
        "rating": ["-critic_score", "-player_rating"],
        "latest": ["-release_year", "title"],
        "price-low": ["active_price", "title"],
        "price-high": ["-price", "title"],
    }

    if sort == "price-low":
        games = sorted(games, key=lambda game: game.active_price)
    else:
        games = games.order_by(*sort_map.get(sort, sort_map["featured"])).distinct()

    context = {
        "games": games,
        "genres": genres,
        "platforms": platforms,
        "filters": {
            "q": query,
            "genre": selected_genre,
            "platform": selected_platform,
            "sort": sort,
        },
    }
    return render(request, "core/browse.html", context)


def game_detail(request, slug):
    game = get_object_or_404(
        Game.objects.prefetch_related("genres", "platforms", "gallery", "reviews__user"),
        slug=slug,
    )
    review_form = ReviewForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"{'/login/'}?next={request.path}")
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            Review.objects.update_or_create(
                game=game,
                user=request.user,
                defaults=review_form.cleaned_data,
            )
            messages.success(request, "Your review has been published.")
            return redirect(game.get_absolute_url())

    related_games = (
        Game.objects.filter(genres__in=game.genres.all())
        .exclude(pk=game.pk)
        .distinct()[:3]
    )
    in_wishlist = (
        request.user.is_authenticated
        and Wishlist.objects.filter(user=request.user, game=game).exists()
    )

    return render(
        request,
        "core/game_detail.html",
        {
            "game": game,
            "related_games": related_games,
            "review_form": review_form,
            "in_wishlist": in_wishlist,
        },
    )


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related("game")
    return render(request, "core/wishlist.html", {"items": items})


@login_required
def dashboard(request):
    items = Wishlist.objects.filter(user=request.user).select_related("game")[:4]
    reviews = Review.objects.filter(user=request.user).select_related("game")[:4]
    return render(
        request,
        "core/dashboard.html",
        {
            "items": items,
            "reviews": reviews,
        },
    )


def signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome to GameZone.")
        return redirect("dashboard")
    return render(request, "registration/signup.html", {"form": form})


@require_POST
@login_required
def toggle_wishlist(request, slug):
    game = get_object_or_404(Game, slug=slug)
    item, created = Wishlist.objects.get_or_create(user=request.user, game=game)
    if created:
        messages.success(request, f"{game.title} added to your wishlist.")
    else:
        item.delete()
        messages.info(request, f"{game.title} removed from your wishlist.")
    return redirect(request.POST.get("next") or game.get_absolute_url())
