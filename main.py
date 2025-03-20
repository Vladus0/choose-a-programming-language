import requests
from itertools import count
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable


programming_languages = ["java", "javascript", "python", "C++", "C#", "C"]


def create_table(language_name, table_data):
    table_data.append([language_name, info_about_language[language_name]['vacancies_found'], info_about_language[language_name]['vacancies_processed'], info_about_language[language_name]['average_salary']])
    table = AsciiTable(table_data)

    return table.table

def predict_rub_salary_for_superJob(payment_from, payment_to):
    if payment_from == 0 and payment_to == 0:
        return None
    elif payment_from == 0:
        return int(payment_to *1.2)
    elif payment_to == 0:
        return int(payment_from *0.8)
    else:
        return int((payment_from+payment_to)/2)
    

def info_about_vacansies_in_superjob():
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ]
    load_dotenv()
    secret_key = os.environ["SECRET_KEY"]
    info_about_language = {}
    for language_name in programming_languages:
        for page in count(0, 1):
            url = "https://api.superjob.ru/2.0/vacancies/"
            headers = {
                "X-Api-App-Id": secret_key,
            }
            payload = {
                "town": "Москва",
                "keyword": language_name,
                "page": page,
                "count": 100,
            }      
            page_response = requests.get(url, headers=headers, params=payload)
            page_response.raise_for_status()
            page_payload = page_response.json()["objects"]
                
            list_of_average_salaries = []
            for profession_num, professions in enumerate(page_payload):
                job = page_payload[profession_num]
                payment_from = (job["payment_from"])
                payment_to = (job["payment_to"])
                salary = predict_rub_salary_for_superJob(payment_from, payment_to)
                if salary != None:
                    list_of_average_salaries.append(predict_rub_salary_for_superJob(payment_from, payment_to))

            if not page_response.json()["more"]:
                break

        average_salary = int((sum(list_of_average_salaries)/len(list_of_average_salaries)))

        info_about_vacancies = {
            "vacancies_found": page_response.json()["total"],
            "vacancies_processed": len(list_of_average_salaries),
            "average_salary": average_salary
            }
        info_about_language[language_name] = info_about_vacancies

        create_table(language_name, table_data)
    print(create_table(language_name, table_data))
        
def predict_rub_salary(salary):
    if salary["from"] == None:
        return int(salary["to"]*1.2)
    elif salary["to"] == None:
        return int(salary["from"]*0.8)
    else:
        return int((salary["from"]+salary["to"])/2)
    
info_about_language = {}

def info_about_vacansies_in_hh_ru():
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ]
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

            page_payload = page_response.json()

            works = page_response.json()["items"]
            list_of_average_salaries = []
            for name_num, name in enumerate(works):
                work = works[name_num]
                salary = work["salary"]
                if salary != None:
                    list_of_average_salaries.append(predict_rub_salary(salary))
            
            if page >= page_payload['pages']-1:
                break
        
        average_salary = int((sum(list_of_average_salaries)/len(list_of_average_salaries)))
    
        info_about_vacancies = {
            "vacancies_found": page_payload["found"],
            "vacancies_processed": len(list_of_average_salaries),
            "average_salary": average_salary
            }
        info_about_language[language_name] = info_about_vacancies

        create_table(language_name, table_data)
    print(create_table(language_name, table_data))   


info_about_vacansies_in_superjob()
info_about_vacansies_in_hh_ru()
