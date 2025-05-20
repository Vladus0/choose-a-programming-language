import requests
from itertools import count
import os
from predict_rub_salary import predict_rub_salary


def get_super_job_statistics(programming_languages, super_job_key):
    sj_statistic = {}
    for language_name in programming_languages:
        for page in count(0, 1):
            url = "https://api.superjob.ru/2.0/vacancies/"
            headers = {
                "X-Api-App-Id": super_job_key,
            }
            payload = {
                "town": "Москва",
                "keyword": language_name,
                "page": page,
                "count": 100,
            }      
            page_response = requests.get(url, headers=headers, params=payload)
            page_response.raise_for_status()
            vacancies = page_response.json()["objects"]

            
            average_salaries = []
            for vacancy_num, vacancy in enumerate(vacancies):
                payment_from = vacancy["payment_from"]
                payment_to = vacancy["payment_to"]
                if payment_to or payment_from:
                    average_salaries.append(predict_rub_salary(payment_from, payment_to))

            if len(average_salaries):
                average_salary = int((sum(average_salaries)/len(average_salaries)))
            else:
                average_salary = 0

            if not page_response.json()["more"]:
                break
            
        vacancies_statistics = {
            "vacancies_found": page_response.json()["total"],
            "vacancies_processed": len(average_salaries),
            "average_salary": average_salary
        }
        
        sj_statistic[language_name] = vacancies_statistics
    return sj_statistic
    