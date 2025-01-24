import os
from typing import List
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from functions import sanitize, process_search_results, sort_by_fewest_videos, print_queries_with_no_videos
from chatgpt import get_keywords
from video_metadata import VideoMetadata

# Adjustable Variables
chrome_driver_path = "C:/Users/huang/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
save_videos_locally = True
save_videos_to_spreadsheet = True
search_keywords_with_gpt = True
gpt_model = "gpt-4o-mini"
search_queries = [
    'Neuropsychologist',
    'Military Personnel',
    'Principal',
    'Strategy Consultant',
    'Family Lawyer',
    'Cybersecurity',
    'Mechanic',
    'General Manager',
    'Dentist',
    'Content Marketing Specialist',
    'Content Creator',
    'Firefighter',
    'Screenwriter',
    'Developmental Psychologist',
    'Astronomer',
    'Entrepreneur',
    'VFX Artist',
    'Urologist',
    'Health Psychologist',
    'Database Administrator',
    'Geologist',
    'Game Developer',
    'Education Administrator',
    'Project Manager',
    'Farmer',
    'DevOps Engineer',
    'Network Engineer',
    'Artist',
    'Civil Litigation Lawyer',
    'Engineer (general)',
    'Politician',
    'Data Scientist',
    'Analytical Chemist',
    'Medical Physicist',
    'Publisher',
    'Filmmaker',
    'Veterinarian',
    'Real Estate Agent',
    'Bookkeeper',
    'Hematologist',
    'Cloud Engineer',
    'Musician',
    'Financial Planner',
    'Management Consultant',
    'Personal Injury Lawyer',
    'Financial Controller',
    'Estate Planning Lawyer',
    'Film Producer',
    'Pharmacist',
    'Professional Athlete',
    'Technology Consultant',
    'Customer Service Representative',
    'Tax Lawyer',
    'Radiologic Technician',
    'Software Engineer',
    'Corporate Strategist',
    'Dermatologist',
    'Special Education Teacher',
    'Digital Marketer',
    'Environmental Chemist',
    'School Superintendent',
    'Graphic Designer',
    'Flight Attendant',
    'Sales Representative',
    'Copywriter',
    'Healthcare Administrator',
    'Ecologist',
    'Therapist',
    'Writer',
    'Molecular Biologist',
    'Social Worker',
    'Nuclear Engineer',
    'Neurologist',
    'Research Physicist',
    'Environmental Lawyer',
    'Quality Assurance Engineer',
    'Medical Laboratory Scientist',
    'Anthropologist',
    'Occupational Therapist',
    'Medicinal Chemist',
    'Coach',
    'Electrical Engineer',
    'Prosecutor',
    'Quantitative Trader',
    'Audiologist',
    'Phlebotomist',
    'Personal Trainer',
    'Accountant',
    'Neuroscientist',
    'Criminal Defense Lawyer',
    'Zoologist',
    'Neurosurgeon',
    'Computer Engineer',
    'Product Manager',
    'Clinical Psychologist',
    'Anesthesiologist',
    'Transactional Lawyer',
    'Sales Development Representative',
    'Mining Engineer',
    'Chemical Engineer',
    'Librarian',
    'Veterinary Technician',
    'Epidemiologist',
    'Cognitive Psychologist',
    'Physical Therapist',
    'Wind Turbine Technician',
    'Paleontologist',
    'Actuary',
    'Air Traffic Controller',
    'Interior Designer',
    'Petroleum Engineer',
    'Mechanical Engineer',
    'Optometrist',
    'Ophthalmologist',
    'Judge',
    'Endocrinologist',
    'Psychiatrist',
    'Financial Analyst',
    'Climate Scientist',
    'Investment Banker',
    'Economist',
    'Paralegal',
    'Cosmetic Chemist',
    'Radiologist',
    'Forensic Psychologist',
    'Pediatrician',
    'Employment Lawyer',
    'School Psychologist',
    'Carpenter',
    'Nurse Practitioner',
    'Systems Administrator',
    'Music Producer',
    'Account Executive',
    'Data Engineer',
    'Travel Agent',
    'Welder',
    'Materials Engineer',
    'Immunologist',
    'Cardiologist',
    'Physicist',
    'Interpreter',
    'Editor',
    'Mechatronics Engineer',
    'Systems Analyst',
    'Physician Assistant',
    'Financial Trader',
    'Sports Psychologist',
    'Social Psychologist',
    'School Counselor',
    'Equity Research Analyst',
    'Fashion Designer',
    'Chef',
    'Medical Malpractice Lawyer',
    'HVAC Technician',
    'Human Resources Specialist',
    'AI Engineer',
    'Nurse',
    'Immigration Lawyer',
    'Cloud Architect',
    'Referee',
    'AR/VR Developer',
    'UX/UI Designer',
    'Blockchain Developer',
    'Video Editor',
    'Architect',
    'Pulmonologist',
    'Professor',
    'Intellectual Property Lawyer',
    'Teacher',
    'Pilot',
    'Environmental Engineer',
    'Astrophysicist',
    'Industrial Engineer',
    'Journalist',
    'Speech Language Pathologist',
    'Venture Capitalist',
    'Insurance Agent',
    'SEO Specialist',
    'Real Estate Developer',
    'Electrician',
    'Corporate Lawyer',
    'Bankruptcy Lawyer',
    'Wildlife Biologist',
    'Research Scientist',
    'Environmental Scientist',
    'Systems Engineer',
    'Federal Agent',
    'Private Equity',
    'Civil Engineer',
    'Quantum Computing Scientist',
    'Gastroenterologist',
    'Robotics Engineer',
    'Urban Planner',
    'Oncologist',
    'Public Defender',
    'Legal Consultant',
    'Event Planner',
    'Orthodontist',
    'Biomedical Engineer',
    'Design Engineer',
    'Otolaryngologist',
    'Diplomat',
    'Detective',
    'Actor',
    'Obstetrician/Gynecologist',
    'Set Designer',
    'Market Researcher',
    'Plastic Surgeon',
    'Rheumatologist',
    'Orthopedic Surgeon',
    'Environmental Consultant',
    'Compliance Officer',
    'Microbiologist',
    'Photographer',
    'Solar Panel Installer',
    'School Dean',
    'Plumber',
    'Policy Analyst',
    'Account Manager',
    'Consumer Psychologist',
    'Aerospace Engineer',
    'Medical Laboratory Technician',
    'Cardiothoracic Surgeon',
    'Prothetist',
    'Game Designer',
    'Sports Agent',
    'Network Administrator',
    'Psychologist',
    'Hospitalist',
    'Sound Engineer',
    'Illustrator',
    'Marketing Assistant',
    'Business Analyst',
    'Data Analyst',
    'Police officer',
    'Marine Biologist',
    'Hairstylist',
    'Industrial Organization Psychologist',
    'Talent Manager',
    'Bioinformatician',
    'Entertainment Lawyer',
]


search_query_formats = [
    "{query}",
    "{query}: day in the life",
    "What is a {query}?",
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
    print(TIKTOK_SESSION_ID)

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

    sorted_queries = sort_by_fewest_videos(search_queries)

    print(sorted_queries)

    for search_query in sorted_queries:
        search_query = sanitize(search_query)
        job_title_folder_path = os.path.join("videos", search_query)
        if not os.path.exists(job_title_folder_path):
            os.makedirs(job_title_folder_path)
        
        for search_query_format in search_query_formats:
            modified_search_query = search_query_format.replace("{query}", search_query)
            modified_search_query = modified_search_query.replace(" ", "%20")

            process_search_results(driver,
                                   user_driver,
                                   search_query,
                                   base_url + modified_search_query,
                                   "https://www.tiktok.com/@",
                                   conditions,
                                   True,
                                   True,
                                   )

        if search_keywords_with_gpt:
            keywords = get_keywords(search_query, gpt_model).split(",")
            for keyword in keywords:
                modified_search_query = f"{keyword} in {search_query}"
                modified_search_query = modified_search_query.replace(" ", "%20")

                process_search_results(driver,
                                       user_driver,
                                       search_query,
                                       base_url + modified_search_query,
                                       "https://www.tiktok.com/@",
                                       conditions,
                                       True,
                                       True,
                                       )


    input("Press Enter to close the browser...")
    driver.quit()
    user_driver.quit()

if __name__ == "__main__":
    main()
    # print_queries_with_no_videos(search_queries)