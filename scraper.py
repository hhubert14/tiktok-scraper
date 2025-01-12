import os
from typing import List

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

from functions import scroll_to_bottom, check_conditions, get_contact_info, get_downloadable_url, save_video, sanitize, add_to_spreadsheet
from video_metadata import VideoMetadata

# Adjustable Variables
chrome_driver_path = "C:/Users/huang/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
save_videos_locally = True
save_videos_to_spreadsheet = True
search_queries = [
   "electrical engineer",
]
search_query_formats = [
    "{query}",
    "{query}: day in the life",
    "{query} salary",
    "How to become a {query}?",
]
conditions = {
    "min_view_count": 1000,
}

load_dotenv()
TIKTOK_SESSION_ID = os.getenv('TIKTOK_SESSION_ID')

cookie = {
    'name': 'sessionid',      
    'value': TIKTOK_SESSION_ID,  
    'domain': '.tiktok.com',
    'path': '/',
}

cService = webdriver.ChromeService(executable_path=chrome_driver_path)

driver = webdriver.Chrome(service=cService)
driver.get("https://www.tiktok.com")
driver.add_cookie(cookie)
driver.refresh()

user_driver = webdriver.Chrome(service=cService)
user_driver.get("https://www.tiktok.com")
user_driver.add_cookie(cookie)
user_driver.refresh()

base_url = "https://www.tiktok.com/search?q="

for search_query in search_queries:
    search_query = sanitize(search_query)
    job_title_folder_path = os.path.join("videos", search_query)
    if not os.path.exists(job_title_folder_path):
        os.makedirs(job_title_folder_path)
    
    for search_query_format in search_query_formats:
        modified_search_query = search_query_format.replace("{query}", search_query)
        modified_search_query = modified_search_query.replace(" ", "%20")
        driver.get(base_url + modified_search_query)

        scroll_to_bottom(driver)

        videos_list = driver.find_element(By.XPATH, "//div[@data-e2e='search_top-item-list']")
        videos = videos_list.find_elements(By.XPATH, "./div")
        for video in videos:
            video_url = video.find_element(By.XPATH, ".//a").get_attribute("href")
            view_count = video.find_element(By.XPATH, ".//strong[@class='css-ws4x78-StrongVideoCount etrd4pu10']").text
            video_title = video.find_element(By.XPATH, ".//h1[@class='css-6opxuj-H1Container ejg0rhn1']").text
            creator_url = "https://www.tiktok.com/@" + video.find_element(By.XPATH, ".//a[@data-e2e='search-card-user-link']").text
            creator_contact_info = get_contact_info(creator_url, user_driver)

            if check_conditions(view_count, **conditions):
                non_watermarked_url = get_downloadable_url(video_url)
                video_metadata_object = VideoMetadata(search_query, video_url, video_title, creator_url, creator_contact_info, non_watermarked_url)
                print(video_metadata_object)
                if save_videos_locally:
                    save_video(video_metadata_object)
                
                if save_videos_to_spreadsheet:
                    add_to_spreadsheet(video_metadata_object)


input("Press Enter to close the browser...")
driver.quit()
user_driver.quit()