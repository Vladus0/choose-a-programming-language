import requests
from itertools import count
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable

def get_super_job_statistics(programming_languages):
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

            
            average_salaries = []
            for profession_num, professions in enumerate(page_payload):
                job = page_payload[profession_num]
                payment_from = (job["payment_from"])
                payment_to = (job["payment_to"])
                salary = predict_rub_salary(payment_from, payment_to)
                if salary != None:
                    average_salaries.append(salary)

                average_salary = int((sum(average_salaries)/len(average_salaries)))

            if not page_response.json()["more"]:
                break
            
        info_about_vacancies = {
            "vacancies_found": page_response.json()["total"],
            "vacancies_processed": len(average_salaries),
            "average_salary": average_salary
        }
        info_about_language[language_name] = info_about_vacancies
    return info_about_language
        

def predict_rub_salary(payment_from, payment_to):
    if payment_from == None:
        return int(payment_to*1.2)
    elif payment_to == None:
        return int(payment_from*0.8)
    else:
        return int((payment_from+payment_to)/2)
    

def create_table(programming_languages, info_about_language):
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language_name in programming_languages:
        table_data.append([language_name, info_about_language[language_name]['vacancies_found'], info_about_language[language_name]['vacancies_processed'], info_about_language[language_name]['average_salary']])
    table = AsciiTable(table_data)
    return table.table
    

def get_hh_ru_statistic(programming_languages):
    info_about_language = {}
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
            average_salaries = []
            for name_num, name in enumerate(works):
                work = works[name_num]
                salary = work["salary"]
                if salary != None:
                    payment_from = salary['from']
                    payment_to = salary['to']
                    average_salaries.append(predict_rub_salary(payment_from, payment_to))

                    average_salary = int((sum(average_salaries)/len(average_salaries)))
            
            if page >= page_payload['pages']-1:
                break
             
        info_about_vacancies = {
            "vacancies_found": page_response.json()["found"],
            "vacancies_processed": len(average_salaries),
            "average_salary": average_salary
        }

        info_about_language[language_name] = info_about_vacancies
    return info_about_language


def main():
    programming_languages = ["java", "javascript", "python", "C++", "C#", "C"]
    super_job_statistics = get_super_job_statistics(programming_languages)
    print(create_table(programming_languages, super_job_statistics))
    hh_ru_statistics = get_hh_ru_statistic(programming_languages)
    print(create_table(programming_languages, hh_ru_statistics))

if __name__=="__main__":
    main()