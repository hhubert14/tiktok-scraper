import time
from typing import List, Optional
import os

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

from video_metadata import VideoMetadata

def scroll_to_bottom(driver: webdriver.Chrome) -> None:
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            time.sleep(5)
            latest_height = driver.execute_script("return document.body.scrollHeight")
            if latest_height == new_height:
                break
        last_height = new_height

def check_conditions(view_count: Optional[str]="0", **kwargs) -> bool:
    if "min_view_count" in kwargs:
        if any(x in view_count for x in ['K', 'M', 'B']):
            return True
        return int(view_count) >= kwargs["min_view_count"]
    
    return False

def get_contact_info(creator_url: str, driver: webdriver.Chrome) -> List[str]:
    contact_info = []
    driver.get(creator_url)
    user_stats_container = driver.find_element(By.XPATH, "//div[@class='css-1a6c9yg-CreatorPageHeaderTextContainer e1457k4r16']")
    user_bio = user_stats_container.find_element(By.XPATH, ".//h2[@data-e2e='user-bio']").text
    link = user_stats_container.find_elements(By.XPATH, "./div/a")

    if (link):
        contact_info.append(link[0].get_attribute("href"))
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'

    if re.search(email_pattern, user_bio):
        contact_info.append(re.findall(email_pattern, user_bio)[0])
    if re.search(phone_pattern, user_bio):
        contact_info.append(re.findall(phone_pattern, user_bio)[0])

    return contact_info

def get_downloadable_url(video_url: str) -> str:
    try:
        api_url = f"https://tiktok-dl.akalankanime11.workers.dev/?url={video_url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            video_data = response.json()
            return video_data["non_watermarked_url"]
        else:
            for i in range(10):
                print(f"Retry #{i + 1}")
                response = requests.get(api_url)
                if response.status_code == 200:
                    video_data = response.json()
                    return video_data["non_watermarked_url"]
            raise Exception(f"Failed to download: {response.status_code}")
    except Exception as e:
        print(f"Error downloading video: {e}")
        return ""
    
def sanitize(name: str) -> str:
    sanitized = re.sub(r'[<>:"/\\|?*]', '', name)
    return sanitized[:100].strip()
    
def save_video(video_metadata: VideoMetadata) -> None:
    creator_name = video_metadata.creator_url.split('@')[-1]
    safe_title = sanitize(video_metadata.video_title)
    safe_job = sanitize(video_metadata.job_title)

    folder_name = f"{creator_name}-{safe_title}"
    folder_path = os.path.join("videos", safe_job, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        return
    
    try:
        metadata_path = os.path.join(folder_path, "metadata.txt")
        with open(metadata_path, 'wb') as f:
            f.write(str(video_metadata).encode('utf-8'))

        if not video_metadata.downloadable_video_url:
            print(f"No downloadable video URL available for {video_metadata.video_url}")
            return

        response = requests.get(video_metadata.downloadable_video_url)
        if response.status_code == 200:
            video_path = os.path.join(folder_path, "video.mp4")
            with open(video_path, 'wb') as f:
                f.write(response.content)
        else:
            print(f"Error downloading video: {response.status_code}")
    except Exception as e:
        print(f"Error saving files: {e}")
    return

def add_to_spreadsheet(video_metadata_object: VideoMetadata) -> None:
    try:
        data = {
            'job_title': video_metadata_object.job_title,
            'video_url': video_metadata_object.video_url,
            'video_title': video_metadata_object.video_title,
            'creator_url': video_metadata_object.creator_url,
            'creator_contact_info': ', '.join(video_metadata_object.creator_contact_info),
            'downloadable_video_url': video_metadata_object.downloadable_video_url,
        }
        
        response = requests.post(
            'https://script.google.com/macros/s/AKfycbzTK3IxdKWux0CTIFrlZ1NlqSiMyOgMwTXGe76qYxz-uadZ8d5h0nlX7vztT91J4fE/exec',
            data=data
        )
        
        if response.status_code != 200:
            print(f"Error posting to spreadsheet: {response.status_code}")
            
    except Exception as e:
        print(f"Error adding to spreadsheet: {e}")