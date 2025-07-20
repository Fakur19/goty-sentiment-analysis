import pandas as pd
import os
from datetime import datetime, timedelta
import re


def clean_date(date_str):
    """
    Converts a string from various Steam date formats to a standardized datetime object.
    - Handles 'DD Mon, YYYY' (e.g., '21 Nov, 2024').
    - Handles 'Month DD, YYYY' (e.g., 'May 29, 2024').
    - Handles 'Mon DD, YYYY' (e.g., 'Dec 3, 2022').
    - Handles 'DD Mon' (e.g., '16 Jan', assumes current year).
    - Handles 'Yesterday'.
    - Handles 'X days ago'.

    Args:
        date_str (str): The date string to convert.

    Returns:
        datetime or pd.NaT: A datetime object or NaT (Not a Time) if conversion fails.
    """
    if not isinstance(date_str, str):
        return pd.NaT

    date_str_lower = date_str.lower()
    now = datetime.now()

    # Case 1: Handle relative dates like "Yesterday" or "X days ago"
    if "yesterday" in date_str_lower:
        return (now - timedelta(days=1)).date()
    if "days ago" in date_str_lower:
        try:
            # Use regex to find the number of days
            days = int(re.search(r"\d+", date_str_lower).group())
            return (now - timedelta(days=days)).date()
        except (ValueError, AttributeError):
            return pd.NaT  # If number extraction fails

    # Case 2: Date includes a year (e.g., "21 Nov, 2024" or "May 29, 2024")
    if "," in date_str:
        # A list of possible date formats with a year
        formats_to_try = [
            "%d %b, %Y",  # e.g., '21 Nov, 2024'
            "%B %d, %Y",  # e.g., 'May 29, 2024'
            "%b %d, %Y",  # e.g., 'Dec 3, 2022'
        ]
        for fmt in formats_to_try:
            try:
                return pd.to_datetime(date_str, format=fmt).date()
            except ValueError:
                continue  # Try the next format if this one fails

    # Case 3: Date does not include a year (e.g., "16 Jan")
    try:
        # Append the current year and parse
        date_with_year = f"{date_str} {now.year}"
        dt = pd.to_datetime(date_with_year, format="%d %b %Y")
        # If the parsed date is in the future, it likely belongs to the previous year
        if dt > now:
            dt = dt.replace(year=now.year - 1)
        return dt.date()
    except ValueError:
        return pd.NaT  # Return NaT if all formats fail


def extract_topic(row):
    """
    Analyzes the title and description of an announcement to determine its topic.
    The function checks for keywords in a specific order.

    Args:
        row (pd.Series): A row of a DataFrame, must contain 'title' and 'desc' columns.

    Returns:
        str: The extracted topic (e.g., "Hotfix", "Patch", "DLC", "Update", "Other").
    """
    title = str(row["title"]).lower()
    desc = str(row["desc"]).lower()

    # Combine title and description for a more comprehensive search
    full_text = title + " " + desc

    # Check for keywords in a specific order of priority
    if "dlc" in full_text:
        return "DLC"
    if "hotfix" in title or "hot fix" in title:  # Prioritize title for hotfix
        return "Hotfix"
    if "patch" in full_text:
        return "Patch"
    if "update" in full_text:
        return "Update"
    if "fix" in full_text:
        return "Fix"

    return "Other"  # Default category if no keywords are found


def add_game_titles_and_topics(input_csv_path, output_csv_path):
    """
    Reads a CSV file of scraped Steam announcements, adds a 'game_title' and 'topic'
    column, cleans the date column, and saves the result to a new CSV file.

    Args:
        input_csv_path (str): The path to the input CSV file from the scraper.
        output_csv_path (str): The path where the new CSV file will be saved.
    """
    # --- Step 1: Define the mapping from game_id to game_title ---
    id_to_title_map = {
        "1222690": "Dragon Age: Inquisition",  # Note: This ID is actually for Ghost of Tsushima
        "292030": "The Witcher 3: Wild Hunt",
        "1593500": "God of War",
        "814380": "Sekiro: Shadows Die Twice",
        "2531310": "The Last of Us Part II",
        "1426210": "It Takes Two",
        "1245620": "ELDEN RING",
        "1086940": "Baldur's Gate 3",
    }

    # --- Step 2: Check if the input file exists ---
    if not os.path.exists(input_csv_path):
        print(f"ERROR: The input file '{input_csv_path}' was not found.")
        print("Please make sure you have run the scraping script first.")
        return

    print(f"Reading data from '{input_csv_path}'...")
    df = pd.read_csv(input_csv_path)

    # --- Step 3: Create new cleaned_date column, keeping the original ---
    print("Cleaning and standardizing dates...")
    # Rename original 'date' column to 'original_date' for comparison
    df.rename(columns={"date": "original_date"}, inplace=True)
    # Create the new 'cleaned_date' column by applying the function
    df["cleaned_date"] = df["original_date"].apply(clean_date)
    print("Created 'cleaned_date' column.")

    # --- Step 4: Add the 'game_title' column ---
    df["game_id"] = df["game_id"].astype(str)

    # --- Check for unknown game IDs and warn the user ---
    known_ids = set(id_to_title_map.keys())
    all_ids_in_csv = set(df["game_id"].unique())
    unknown_ids = all_ids_in_csv - known_ids

    if unknown_ids:
        print("\n--- WARNING: Unknown Game IDs Found ---")
        print("The following game IDs from your CSV were not found in the title map:")
        for uid in sorted(list(unknown_ids)):
            print(f"  - {uid}")
        print("These games will have 'Unknown Game' as their title.")
        print("-------------------------------------\n")

    df["game_title"] = df["game_id"].map(id_to_title_map)
    df["game_title"].fillna("Unknown Game", inplace=True)  # Fill missing titles
    print("Successfully added the 'game_title' column.")

    # --- Step 5: Add the 'topic' column ---
    df["topic"] = df.apply(extract_topic, axis=1)
    print("Successfully added the 'topic' column.")

    # --- Step 6: Reorder columns for better readability ---
    cols = [
        "game_id",
        "game_title",
        "original_date",
        "cleaned_date",
        "title",
        "topic",
        "desc",
    ]
    existing_cols = [col for col in cols if col in df.columns]
    other_cols = [col for col in df.columns if col not in existing_cols]
    df = df[existing_cols + other_cols]

    # --- Step 7: Report on missing values ---
    print("\n--- Missing Values Report ---")
    missing_values_summary = df.isnull().sum()
    print(missing_values_summary[missing_values_summary > 0])
    if missing_values_summary.sum() == 0:
        print("No missing values found in the final dataset.")
    print("-----------------------------\n")

    # --- Step 8: Save the new DataFrame to a new CSV file ---
    try:
        df.to_csv(output_csv_path, index=False, encoding="utf-8")
        print(f"Successfully saved the updated data to '{output_csv_path}'")
        print("\n--- First 5 rows of the new data ---")
        print(df.head())
    except Exception as e:
        print(f"An error occurred while saving the new CSV file: {e}")


if __name__ == "__main__":
    # The file generated by the scraper script
    input_file = "steam_announcements.csv"

    # The name for the new file with the added titles and topics
    output_file = "steam_announcements_with_titles.csv"

    # Run the function to process the data
    add_game_titles_and_topics(input_file, output_file)
