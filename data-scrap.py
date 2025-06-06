import requests
from bs4 import BeautifulSoup
from tqdm import tqdm  # Import tqdm for progress bar
import pandas as pd


# Function to get reviews for a given appid
def get_reviews(appid, params={"json": 1}):
    url = "https://store.steampowered.com/appreviews/"
    response = requests.get(
        url=url + appid, params=params, headers={"User-Agent": "Mozilla/5.0"}
    )
    return response.json()


# Function to get a specified number of reviews for a given appid
def get_n_reviews(appid, n=300, language="english"):
    reviews = []
    cursor = "*"
    params = {
        "json": 1,
        "filter": "all",
        "language": language,  # Use the provided language parameter
        "day_range": 9223372036854775807,
        "review_type": "all",
        "purchase_type": "all",
    }

    while n > 0:
        params["cursor"] = cursor.encode()
        params["num_per_page"] = min(100, n)
        n -= 100

        response = get_reviews(appid, params)
        cursor = response["cursor"]
        reviews += response["reviews"]

        if len(response["reviews"]) < 100:
            break

    return reviews


# Function to get the app ID for each game from Steam search results
def get_app_id(game_names):
    app_id = []
    for title in game_names:
        response = requests.get(
            url=f"https://store.steampowered.com/search/?term={title}&category1=998",
            headers={"User-Agent": "Mozilla/5.0"},
        )
        soup = BeautifulSoup(response.text, "html.parser")

        # Try to find the search result row
        game = soup.find(class_="search_result_row")

        if game:
            # If a game is found, get the appid
            app_id_value = game.get("data-ds-appid")
            if app_id_value:
                app_id.append(app_id_value)
            else:
                print(f"App ID not found for {title}")
        else:
            print(f"No search result found for {title}")

    return app_id


# List of games to scrape
games = [
    "Dragon Age: Inquisition",
    "The Witcher 3: Wild Hunt",
    "God of War",
    "Sekiro: Shadows Die Twice",
    "The Last of Us Part II",
    "It Takes Two",
    "Elden Ring",
    "Baldur's Gate 3",
]

# List of languages you want to scrape
languages = ["english"]

# Iterate through each language and scrape reviews
for language in languages:
    print(f"Scraping reviews for language: {language}")
    reviews = []
    game_list = get_app_id(games)

    # Initialize progress bar for iterating over the games
    for game, app_id in tqdm(
        zip(games, game_list), total=len(games), desc="Scraping reviews"
    ):
        # Get reviews for the app ID and add the 'game' column
        game_reviews = get_n_reviews(
            app_id, 1000, language=language
        )  # Use language parameter

        # Add the 'game' column to each review
        for review in game_reviews:
            review["game"] = game  # Add the game name to each review

        # Add the reviews to the main list
        reviews += game_reviews

    # Convert to DataFrame
    df = pd.DataFrame(reviews)[
        [
            "timestamp_created",
            "game",
            "review",
            "voted_up",
            "weighted_vote_score",
            "language",
            "author",
        ]
    ]

    # Save the reviews for the current language to a CSV file
    df.to_csv(f"data/GOTY_Steam_reviews_{language}_sample.csv", index=False)
    print(f"Reviews for language {language} saved to GOTY_Steam_reviews_{language}.csv")
    print(df["game"].value_counts())
    print(df.shape)
