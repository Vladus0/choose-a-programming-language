import requests
from itertools import count
from predict_rub_salary import predict_rub_salary


def get_hh_statistics(programming_languages):
    hh_statistics = {}
    for language_name in programming_languages:       
        area = 1
        url = "https://api.hh.ru/vacancies"
        for page in count(0, 1):
            payload = {
                "area": area,
                "text": language_name,
                "page": page,
                "per_page": 100
            }
            page_response = requests.get(url, params=payload)
            page_response.raise_for_status()
            hh_response = page_response.json()
            vacancies = hh_response["items"]


            average_salaries = []
            for vacancy_num, vacancy in enumerate(vacancies):
                salary = vacancy["salary"]
                if salary:
                    payment_from = salary['from']
                    payment_to = salary['to']
                    average_salaries.append(predict_rub_salary(payment_from, payment_to))
        
            if page >= hh_response['pages']-1:
                break


        if len(average_salaries):                
            average_salary = int((sum(average_salaries)/len(average_salaries)))
        else:
            average_salary = 0
             
        vacancies_statistics = {
            "vacancies_found": hh_response["found"],
            "vacancies_processed": len(average_salaries),
            "average_salary": average_salary
        }

        hh_statistics[language_name] = vacancies_statistics
    return hh_statistics 


