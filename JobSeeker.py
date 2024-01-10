# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ #
# █                                                   █ #
# █             ██╗  ██╗          ██╗                 █ #
# █             ██║ ██╔╝          ██║                 █ #
# █             █████╔╝           ██║                 █ #
# █             ██╔═██╗           ██║                 █ #
# █             ██║  ██╗ ██╗      ██║ ██╗             █ #
# █             ╚═╝  ╚═╝ ╚═╝      ╚═╝ ╚═╝             █ #
# █                                                   █ #
# █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ █ #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from bs4 import BeautifulSoup
import requests
from dotenv import dotenv_values
import re
import json
import time
import os


def get_data(url, domen):
    headers = {
        'Accept': 'text / html, application / xhtml + xml, application / xml; q = 0.9, * / *;q = 0.8',
        'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15(KHTML, like Gecko) Version/16.6 Safari/605.1.15'
    }

    req = requests.get(url, headers=headers)

    with open('data/jobs_1.html', 'w') as file:
        file.write(req.text)

    with open('data/jobs_1.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    pagination = int(soup.find('ul', 'pagination pagination_with_numbers').find_all('a', 'page-link')[-2].text)
    vacancy_urls = []

    for page in range(1, pagination + 1):
        if page != 1:
            req = requests.get(f'{url}&page={page}')

            with open(f'data/jobs_{page}.html', 'w') as file:
                file.write(req.text)

            with open(f'data/jobs_{page}.html') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')

        vacancies = soup.find_all('li', class_='list-jobs__item')

        for vacancy in vacancies:
            vacancy_url = domen + vacancy.find('a', class_='job-list-item__link').get('href')
            vacancy_urls.append(vacancy_url)

    vacancy_data_list = []
    print(f'Number of iterations - {len(vacancy_urls)}')
    iteration = 0
    num_file = 1
    for vacancy_url in vacancy_urls:
        req = requests.get(vacancy_url, headers=headers)

        vacancy_name = ' '.join(vacancy_url.split('/')[-2].split('-')[1:]).title().strip()

        file_path = os.path.join('data', f'{vacancy_name}.html')

        if os.path.exists(file_path):
            file_path = os.path.join('data', f'{vacancy_name}_{num_file}.html')
            num_file += 1

        with open(file_path, 'w') as file:
            file.write(req.text)

        with open(file_path) as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        vacancy_data = soup.find('div', class_='job-post-page')

        try:
            owner = vacancy_data.find('header').find('div', class_='job-details--main-info')
            vacancy_owner = owner.find('a', class_='job-details--title').text.strip() + '\n' + owner.find('a',
                                                                                                          class_='job-details--recruiter-name').text.strip()
        except Exception:
            vacancy_owner = 'No vacancy owner'

        try:
            salary = vacancy_data.find('div', class_='col').find('span', class_='public-salary-item').text.strip()
        except Exception:
            salary = 'No information about salary'

        try:
            vacancy_description = vacancy_data.find('div', class_='mb-4').text.strip()
        except Exception:
            vacancy_description = 'No vacancy description'

        try:
            company_info = vacancy_data.find('div', class_='mb-4').find_next('div', class_='mb-4')
            company_info = company_info.text.strip().replace('\n', ' ')
        except Exception:
            company_info = 'No company info'

        try:
            # leave only one space using re.sub
            publication_date = re.sub(r'\s+', ' ', vacancy_data.find('p', class_='text-muted').contents[2])
        except Exception:
            publication_date = 'No company info'

        try:
            info_list = vacancy_data.find_all('ul', 'job-additional-info--body')

            additional_info = ''
            for info in info_list:
                add_info_list = info.find_all('div', 'job-additional-info--item-text')
                for extra_info in add_info_list:
                    additional_info += ' '.join(extra_info.text.split()) + '\n'
        except Exception:
            additional_info = 'No additional info'

        vacancy_data_list.append({
            'Name:': vacancy_name,
            'URL:': vacancy_url,
            'Owner:': vacancy_owner,
            'Salary:': salary,
            'Description': vacancy_description,
            'Company info': company_info,
            'Date:': publication_date,
            'Extra information:': additional_info
        })

        iteration += 1
        print(f'Iteration #{iteration}, iteration left {len(vacancy_urls)-iteration}')
        time.sleep(1.5)

    with open('data/jobs_data.json', 'w', encoding='utf-8') as file:
        json.dump(vacancy_data_list, file, indent=4, ensure_ascii=False)


config = dotenv_values('.env')
URL = config.get('URL')
DOMEN = config.get('DOMEN')

get_data(URL, DOMEN)
