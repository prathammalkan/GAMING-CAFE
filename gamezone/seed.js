const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('db.sqlite3');

const run = (sql, params = []) => new Promise((resolve, reject) => {
    db.run(sql, params, function(err) {
        if (err) reject(err);
        else resolve(this);
    });
});

const get = (sql, params = []) => new Promise((resolve, reject) => {
    db.get(sql, params, (err, row) => {
        if (err) reject(err);
        else resolve(row);
    });
});

async function main() {
    await run("DELETE FROM core_game_genres");
    await run("DELETE FROM core_game_platforms");
    await run("DELETE FROM core_galleryimage");
    await run("DELETE FROM core_game");
    await run("DELETE FROM core_genre");
    await run("DELETE FROM core_platform");

    const generic_cover = "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=900&q=80";
    const generic_banner = "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1600&q=80";
    const categories = [
        {name: "PC Games", color: "#FF6B2C", icon: "bolt"},
        {name: "PS5 Console", color: "#47D7AC", icon: "gamepad"},
        {name: "PS4 Console", color: "#F04F78", icon: "gamepad"},
        {name: "Car Simulator", color: "#6C8CFF", icon: "track"},
        {name: "Bike Simulator", color: "#FDBB2D", icon: "track"},
        {name: "Cafeteria", color: "#E8E1D9", icon: "spark"}
    ];

    const slugify = (text) => text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');

    for (const c of categories) {
        await run("INSERT INTO core_genre (name, slug, accent_color, icon, description, created_at, updated_at) VALUES (?, ?, ?, ?, '', datetime('now'), datetime('now'))", [c.name, slugify(c.name), c.color, c.icon]);
        await run("INSERT INTO core_platform (name, slug, icon, created_at, updated_at) VALUES (?, ?, '', datetime('now'), datetime('now'))", [c.name, slugify(c.name)]);
    }

    const games = [
        {title: "Valorant", cat: "PC Games", feat: 1},
        {title: "CS GO 2", cat: "PC Games", feat: 0},
        {title: "Rainbow Seige 6", cat: "PC Games", feat: 0},
        {title: "Fortnite", cat: "PC Games", feat: 1},
        {title: "League of Legends", cat: "PC Games", feat: 0},
        {title: "GTA V", cat: "PS5 Console", feat: 1},
        {title: "Last Of Us 2 Remastered", cat: "PS5 Console", feat: 1},
        {title: "Ghost Of Tsuhima", cat: "PS5 Console", feat: 0},
        {title: "Ghost Of Yotei", cat: "PS5 Console", feat: 0},
        {title: "Black Myth Wukong", cat: "PS5 Console", feat: 1},
        {title: "The Witcher", cat: "PS5 Console", feat: 0},
        {title: "God Of War Ragnarok", cat: "PS5 Console", feat: 1},
        {title: "GTA SA", cat: "PS4 Console", feat: 0},
        {title: "GTA VC", cat: "PS4 Console", feat: 0},
        {title: "Counter Strike", cat: "PS4 Console", feat: 0},
        {title: "Hitman", cat: "PS4 Console", feat: 0},
        {title: "WWE", cat: "PS4 Console", feat: 0},
        {title: "F1 26", cat: "Car Simulator", feat: 1},
        {title: "Gran Tourismo", cat: "Car Simulator", feat: 0},
        {title: "Dirt Rally", cat: "Car Simulator", feat: 0},
        {title: "Moto GP 25", cat: "Bike Simulator", feat: 1},
        {title: "Veg Items", cat: "Cafeteria", feat: 0},
        {title: "Colddrinks", cat: "Cafeteria", feat: 0}
    ];

    for (let i = 0; i < games.length; i++) {
        const g = games[i];
        const res = await run(`INSERT INTO core_game 
            (title, slug, tagline, short_description, description, studio, release_year, playtime, age_rating, price, discount_price, critic_score, player_rating, is_featured, is_trending, is_new_release, is_editors_pick, hero_badge, cover_url, banner_url, trailer_url, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '', datetime('now'), datetime('now'))`, 
            [g.title, slugify(g.title), `Experience ${g.title} at DEMON ZONE`, "Top tier entertainment experience.", `Enjoy ${g.title} in our premium lounges.`, "DEMON ZONE", 2026, "Any", "All", 50.00, 40.00, 95, 4.8, g.feat, (i % 2 === 0 ? 1 : 0), (i % 3 === 0 ? 1 : 0), (i % 4 === 0 ? 1 : 0), "Available Now", generic_cover, generic_banner]);
        
        const gameId = res.lastID;
        
        const genre = await get("SELECT id FROM core_genre WHERE slug = ?", [slugify(g.cat)]);
        if (genre) await run("INSERT INTO core_game_genres (game_id, genre_id) VALUES (?, ?)", [gameId, genre.id]);
        
        const platform = await get("SELECT id FROM core_platform WHERE slug = ?", [slugify(g.cat)]);
        if (platform) await run("INSERT INTO core_game_platforms (game_id, platform_id) VALUES (?, ?)", [gameId, platform.id]);
    }

    db.close();
    console.log("Database seeded successfully with async!");
}

main().catch(console.error);
