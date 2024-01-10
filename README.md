## JobSeeker 🚀


### Overview 🌟

JobSeeker is a Python application for scraping job vacancies from Djinni.co. It harnesses the power of BeautifulSoup, Requests, and other libraries for seamless web scraping. The collected data includes job names, URLs, owners, salaries, descriptions, company information, publication dates, and additional insights.

### Features ✨

- **Dynamic Scraping:** The application dynamically scrapes job vacancies from Djinni.co, intelligently adapting to changes in pagination.

- **Data Integrity:** Handles duplicate job names by appending a unique identifier to the filename, ensuring pristine data integrity.

- **Structured Data:** Collects meticulously structured data, including comprehensive job details, to create a rich and informative JSON file.

### Installation 🛠️

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/job-scraper.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration ⚙️

- Set your Djinni.co job search URL and domain in the `.env` file:

   ```env
   URL=https://djinni.co/jobs/?primary_keyword=Python
   DOMAIN=https://djinni.co
   ```

### Usage 🚀

Run the main script:

```bash
python main.py
```

### Acknowledgments 🙌

Special thanks to the creators of BeautifulSoup, Requests, and other libraries used in this project.

Happy coding! 🚀
