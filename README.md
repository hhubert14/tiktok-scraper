# Setup

1. **Clone the Repository**  
   Clone the repository to your local machine.

2. **Set Up Environment Variables**  
   - Create a `.env` file in the root directory of the project.
   - Add the following line to the `.env` file:
     ```
     TIKTOK_SESSION_ID = "<replace with your session id>"
     ```
   - You can find your TikTok session ID by logging into your TikTok account, inspecting the element, navigating to cookies, and retrieving the value associated with the name `sessionid`.

3. **Download Chrome WebDriver**  
   - Download the Chrome WebDriver compatible with your version of Chrome from [ChromeDriver Downloads](https://developer.chrome.com/docs/chromedriver/downloads).
   - Refer to this [Selenium Web Scraping Guide](https://builtin.com/articles/selenium-web-scraping) for additional details.

4. **Adjust Scraper Settings**  
   In `scraper.py`, adjust the following variables to suit your needs:
   ```python
   chrome_driver_path = "path/to/your/chromedriver"
   save_videos_locally = True
   save_videos_to_spreadsheet = True
   search_queries = [
       ...,
   ]
   search_query_formats = [
       ...,
   ]
   conditions = {
       "min_view_count": 1000,
   }
   ```

5. **Install Required Dependencies**  
   Run the following command in your terminal to install the necessary dependencies:
   ```
   pip install -r requirements.txt
   ```

6. **Run the Scraper**  
   Start the scraping process by executing the following command:
   ```
   python scraper.py
   ```
   - If `save_videos_locally` is set to `True`, the scraped videos will be saved in the `videos` folder.
