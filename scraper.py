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
    "Computer Engineer",
    "Accountant",
    "Financial Analyst",
    "Financial Controller",
    "Business Analyst",
    "Investment Banker",
    "Private Equity",
    "Venture Capitalist",
    "Financial Planner",
    "Market Researcher",
    "General Manager",
    "Financial Trader",
    "Quantitative Trader",
    "Digital Marketer",
    "Content Marketing Specialist",
    "Marketing Assistant",
    "SEO Specialist",
    "Strategy Consultant",
    "Management Consultant",
    "Technology Consultant",
    "Project Manager",
    "Human Resources Specialist",
    "Account Manager",
    "Account Executive",
    "Customer Service Representative",
    "Bookkeeper",
    "Entrepreneur",
    "Insurance Agent",
    "Economist",
    "Sales Development Representative",
    "Sales Representative",
    "Actuary",
    "Real Estate Agent",
    "Real Estate Developer",
    "Talent Manager",
    "Product Manager",
    "Engineer (general)",
    "Mechanical Engineer",
    "Aerospace Engineer",
    "Civil Engineer",
    "Industrial Engineer",
    "Electrical Engineer",
    "Environmental Engineer",
    "Chemical Engineer",
    "Biomedical Engineer",
    "Materials Engineer",
    "Mining Engineer",
    "Nuclear Engineer",
    "Petroleum Engineer",
    "Design Engineer",
    "Software Engineer",
    "DevOps Engineer",
    "Mechatronics Engineer",
    "Robotics Engineer",
    "Dentist",
    "Nurse",
    "Epidemiologist",
    "Audiologist",
    "Phlebotomist",
    "Medical Laboratory Technician",
    "Medical Laboratory Scientist",
    "Psychologist",
    "Nurse Practitioner",
    "Physician Assistant",
    "Healthcare Administrator",
    "Pharmacist",
    "Doctor (general)",
    "Radiologist",
    "Hematologist",
    "Hospitalist",
    "Immunologist",
    "Pulmonologist",
    "Rheumatologist",
    "Urologist",
    "Anesthesiologist",
    "Cardiologist",
    "Cardiothoracic surgeon",
    "Dermatologist",
    "Endocrinologist",
    "Gastroenterologist",
    "Neurologist",
    "Neurosurgeon",
    "Obstetrician/Gynecologist",
    "Oncologist",
    "Ophthalmologist",
    "Optometrist",
    "Orthopedic Surgeon",
    "Orthodontist",
    "Otolaryngologist",
    "Pediatrician",
    "Plastic Surgeon",
    "Psychiatrist",
    "Veterinarian",
    "Teacher",
    "Education Administrator",
    "Principal",
    "School Counselor",
    "Professor",
    "Librarian",
    "Judge",
    "Paralegal",
    "Lawyer (general)",
    "Personal Injury Lawyer",
    "Estate Lawyer",
    "Bankruptcy Lawyer",
    "Entertainment Lawyer",
    "Intellectual Property Lawyer",
    "Medical Malpractice Lawyer",
    "Prosecutor",
    "Criminal Defense Lawyer",
    "Contract Lawyer",
    "Employment Lawyer",
    "Corporate Lawyer",
    "Immigration Lawyer",
    "Tax Lawyer",
    "Family Lawyer",
    "Civil Litigation Lawyer",
    "Environmental Lawyer",
    "Legal Consultant",
    "Physical Therapist",
    "Sports Agent",
    "Sports Psychologist",
    "Fitness Instructor",
    "Coach",
    "Professional Athlete",
    "Referee",
    "Adminstrative Social Worker",
    "Therapist",
    "Police officer",
    "Firefighter",
    "Criminal Investigator",
    "Diplomat",
    "Politician",
    "Social Worker",
    "Federal Agent",
    "Military Personnel",
    "Scientist (general)",
    "Biologist",
    "Chemist",
    "Physicist",
    "Environmental Scientist",
    "Research Scientist",
    "Geologist",
    "Astronomer",
    "Paleontologist",
    "Anthropologist",
    "Electrician",
    "Carpenter",
    "Plumber",
    "Mechanic",
    "Farmer",
    "Chef",
    "HVAC Technician",
    "Graphic Designer",
    "UX/UI Designer",
    "Artist",
    "VFX Artist",
    "Musician",
    "Journalist",
    "Architect",
    "Interior Designer",
    "Filmmaker",
    "Film Producer",
    "Sound Engineer",
    "Hairstylist",
    "Writer",
    "Copywriter",
    "Publisher",
    "Photographer",
    "Actor",
    "Editor",
    "Video Editor",
    "Fashion Designer",
    "Illustrator",
    "Music Producer",
    "Screenwriter",
    "Set Designer",
    "Data Scientist",
    "Data Analyst",
    "Data Engineer",
    "AI Engineer",
    "AR/VR Developer",
    "Cloud Architect",
    "Cloud Engineer",
    "Database Administrator",
    "Cybersecurity",
    "Systems Analyst",
    "Systems Engineer",
    "Systems Administrator",
    "Game Developer",
    "Quality Assurance Engineer",
    "Blockchain Developer",
    "Network Administrator",
    "Network Engineer",
    "Flight Attendant",
    "Pilot",
    "Interpreter",
    "Travel Agent",
    "Air Traffic Controller",
    "Forensic Psychologist",
    "School Psychologist",
    "Health Psychologist",
    "Consumer Psychologist",
    "Social Psychologist",
    "Industrial Organization Psychologist",
    "Clinical Psychologist",
    "Neuropsychologist",
    "Cognitive Psychologist",
    "Developmental Psychologist",
    "Special Education Teacher",
    "Occupational Therapist",
    "Speech Language Pathologist",
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

def main():
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
            videos = videos_list.find_elements(By.XPATH, "./div[contains(@class, 'DivItemContainerForSearch')]")

            for video in videos:
                video_url = video.find_element(By.XPATH, ".//a").get_attribute("href")
                view_count = video.find_element(By.XPATH, ".//strong[contains(@class, 'StrongVideoCount')]").text
                video_title = video.find_element(By.XPATH, ".//h1[contains(@class, 'H1Container')]").text
                if "\\" in video_title or "\n" in video_title:
                    continue
                creator_url = "https://www.tiktok.com/@" + video.find_element(By.XPATH, ".//a[@data-e2e='search-card-user-link']").text
                creator_contact_info = get_contact_info(creator_url, user_driver)

                if check_conditions(view_count, **conditions):
                    # non_watermarked_url = get_downloadable_url(video_url)
                    non_watermarked_url = ""
                    video_metadata_object = VideoMetadata(search_query, video_url, video_title, creator_url, creator_contact_info, non_watermarked_url)
                    print(video_metadata_object)
                    if save_videos_locally:
                        save_video(video_metadata_object)
                    
                    if save_videos_to_spreadsheet:
                        add_to_spreadsheet(video_metadata_object)

    input("Press Enter to close the browser...")
    driver.quit()
    user_driver.quit()

# load_dotenv()
# DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')
# import dropbox

if __name__ == "__main__":
    main()
    # dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    # dbx.users_get_current_account()

