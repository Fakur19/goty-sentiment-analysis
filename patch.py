import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import shutil  # Used as a fallback for checking the PATH
import os  # Used to check for files and expand user paths


def setup_driver():
    """
    Sets up a local Selenium Chrome WebDriver for a Windows environment.
    It checks common installation paths to be more reliable.
    """
    # --- Check for Chrome in common Windows locations ---
    chrome_path = None
    # List of common installation paths for Chrome on Windows
    possible_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
    ]

    print("Searching for Google Chrome installation...")
    for path in possible_paths:
        if os.path.exists(path):
            chrome_path = path
            print(f"Found Chrome at: {path}")
            break

    # Fallback to shutil.which if not found in common locations
    if not chrome_path:
        print("Chrome not found in common locations, checking system PATH...")
        chrome_path = shutil.which("chrome")

    if not chrome_path:
        print("---")
        print("ERROR: Google Chrome browser not found.")
        print("Please install Google Chrome on your system to run this scraper.")
        print("You can download it from: https://www.google.com/chrome/")
        print("---")
        return None  # Return None to indicate that setup failed

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Run in headless mode (no browser window)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    print("Setting up WebDriver...")
    # Automatically download and manage the correct ChromeDriver for your installed Chrome version
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        print("WebDriver setup complete.")
        return driver
    except Exception as e:
        print(f"ERROR: Failed to setup WebDriver. {e}")
        print("This might be a permission issue or a problem with webdriver-manager.")
        return None


def scrape_steam_announcements(app_ids):
    """
    Scrapes Steam announcements for a list of app_ids by scrolling the page,
    and saves the data to a CSV file.

    Args:
        app_ids: A list of Steam application IDs (as strings).

    Returns:
        A pandas DataFrame containing the scraped data.
    """
    base_url = "https://steamcommunity.com/app/{}}/allnews/"
    all_announcements_data = []
    driver = setup_driver()

    # --- Check if driver setup was successful ---
    if not driver:
        print("WebDriver setup failed. Aborting the scraping process.")
        return pd.DataFrame()  # Return an empty DataFrame

    for app_id in app_ids:
        print(f"Scraping announcements for app_id: {app_id}")
        url = base_url.format(app_id)

        try:
            driver.get(url)

            # --- Handle Age Verification Gate ---
            try:
                # Wait for the page to load and potentially show the age gate
                time.sleep(2)
                # Updated locator using the CSS classes you provided.
                # This looks for an element with both 'btn_blue_steamui' and 'btn_medium' classes.
                age_gate_button = driver.find_element(
                    By.CSS_SELECTOR, ".btn_blue_steamui.btn_medium"
                )
                print(
                    f"Age verification page found for app_id {app_id}. Clicking button."
                )
                age_gate_button.click()
                # Wait for the actual content page to load
                time.sleep(3)
            except NoSuchElementException:
                # If the button isn't found, it means there was no age gate.
                print(
                    f"No age verification page for app_id {app_id}, proceeding directly."
                )
                pass

            # --- Scrolling Logic ---
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scroll_attempts = 5  # Prevents infinite loops on static pages

            while scroll_attempts < max_scroll_attempts:
                # Scroll down to the bottom of the page
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait for new content to load
                time.sleep(3)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    # If height hasn't changed, we've likely reached the bottom
                    print("Reached the end of the page.")
                    break
                last_height = new_height
                scroll_attempts += 1

            # --- Parsing Logic ---
            # Get the full page source after scrolling
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Find all announcement cards
            announcement_cards = soup.find_all("div", class_="apphub_Card")
            print(
                f"Found {len(announcement_cards)} announcement cards for app_id: {app_id} after scrolling."
            )

            for card in announcement_cards:
                date_elem = card.find("div", class_="apphub_CardContentNewsDate")
                title_elem = card.find("div", class_="apphub_CardHeaderContent")
                desc_elem = card.find("div", class_="apphub_CardContentNewsDesc")

                date = date_elem.get_text(strip=True) if date_elem else "N/A"
                title = (
                    title_elem.a.get_text(strip=True)
                    if title_elem and title_elem.a
                    else "N/A"
                )
                description = desc_elem.get_text(strip=True) if desc_elem else "N/A"

                all_announcements_data.append(
                    {
                        "game_id": app_id,
                        "date": date,
                        "title": title,
                        "desc": description,
                    }
                )

        except Exception as e:
            print(f"An error occurred while processing app_id {app_id}: {e}")

    # Close the browser once all app_ids are processed
    print("Closing WebDriver.")
    driver.quit()

    df = pd.DataFrame(all_announcements_data)
    return df


if __name__ == "__main__":
    # Instructions for Windows:
    # 1. Make sure you have Python and Google Chrome installed.
    # 2. Open a Command Prompt or PowerShell.
    # 3. Install the required libraries: pip install pandas beautifulsoup4 selenium webdriver-manager
    # 4. Run this script: python your_script_name.py
    game_ids = [
        "1222690",  # Dragon Age Inquisition
        "292030",  # The Witcher 3
        "1593500",  # God of War
        "814380",  # Sekiro : Shadow Die Twice
        "2531310",  # The Last of Us Part II
        "1426210",  # It Takes Two
        "1245620",  # ELDEN RING
        "1086940",  # Baldur's Gate 3
    ]

    announcement_df = scrape_steam_announcements(game_ids)

    if not announcement_df.empty:
        csv_filename = "steam_announcements.csv"
        announcement_df.to_csv(csv_filename, index=False, encoding="utf-8")

        print(f"\n--- Scraping Complete ---")
        print(f"Successfully scraped {len(announcement_df)} announcements.")
        print(f"Data exported to '{csv_filename}'")
        print("\n--- First 5 rows of the data ---")
        print(announcement_df.head())
    else:
        print("\nNo data was scraped. The CSV file was not created.")
