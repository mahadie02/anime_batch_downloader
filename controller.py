import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry # type: ignore
from playwright.sync_api import sync_playwright
from file_downloader import download_file

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}


# Function to create the folder structure for downloads
def create_folder_structure(base_folder, anime_name, season_number):
    season_folder = os.path.join(base_folder, anime_name, f'Season {season_number:02d}')
    os.makedirs(season_folder, exist_ok=True)
    return season_folder


# Function to check if an episode exists


def check_episode_exists(url):
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.head(url, timeout=20)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False



# Download Page Link
def get_download_page_link(episode_url):
    response = requests.get(episode_url, headers=HEADERS)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the download button under the class <pc-item pc-download>
    download_button = soup.find('a', class_='btn btn-sm pc-download')
    if download_button and 'href' in download_button.attrs:
        return download_button['href']  # Return the download page link
    else:
        print(f"Download link not found on {episode_url}.")
        return None



# Function to get direct download link
def get_direct_download_link(download_page_url):
    # Start Playwright in a headless browser mode
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch Chromium browser in headless mode
        page = browser.new_page()  # Create a new page

        page.goto(download_page_url)  # Open the download page

        # Wait for the download button to load (may need adjusting if it's dynamic)
        page.wait_for_selector("div.dowload a:has-text('Download (1080P - mp4)')")

        # Extract the download link
        download_button = page.query_selector("div.dowload a:has-text('Download (1080P - mp4)')")
        if download_button:
            download_url = download_button.get_attribute('href')
            browser.close()
            #print(download_url)
            return download_url

        browser.close()
        return None   



# Function to download an episode
def download_episode(url, folder, anime_name, season_number, episode_number):  
    file_name = f'{anime_name} S{season_number:02d}E{episode_number:03d}.mp4'
    download_file(url, folder, file_name)



# Main script
def main_control(base_url, download_folder, anime_name, season_number, start_episode, max_episodes):
    # Create folder structure for the anime and season
    season_folder = create_folder_structure(download_folder, anime_name, season_number)

    # Iterate through episode URLs and download them
    episode_number = start_episode
    while episode_number <= max_episodes:
        episode_url = base_url.rsplit('-', 1)[0] + f'-{episode_number}'
        print(f'Checking Episode {episode_number}...')

        if check_episode_exists(episode_url):
            download_page_url = get_download_page_link(episode_url)
            download_url = get_direct_download_link(download_page_url)
            #print(download_url)
            print(f'Episode {episode_number} found, downloading...')
            download_episode(download_url, season_folder, anime_name, season_number, episode_number)
            episode_number += 1
        else:
            print(f'Episode {episode_number} does not exist. Stopping.')
            break

    print('All available episodes downloaded successfully!')
