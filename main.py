import requests
from itertools import count
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_super_job_statistics(programming_languages):
    load_dotenv()
    super_job_key = os.environ["SUPER_JOB_KEY"]
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
                payment_from = (vacancy["payment_from"])
                payment_to = (vacancy["payment_to"])
                salary = predict_rub_salary(payment_from, payment_to)
                if salary != None:
                    average_salaries.append(salary)

            average_salary = int((sum(average_salaries)/len(average_salaries)))

            if not page_response.json()["more"]:
                break
            
        vacancies_statistics = {
            "vacancies_found": page_response.json()["total"],
            "vacancies_processed": len(average_salaries),
            "average_salary": average_salary
        }
        sj_statistic[language_name] = vacancies_statistics
    return sj_statistic
        

def predict_rub_salary(payment_from, payment_to):
    if payment_from == None:
        return int(payment_to*1.2)
    elif payment_to == None:
        return int(payment_from*0.8)
    else:
        return int((payment_from+payment_to)/2)
    

def create_table(programming_languages, language_statistic):
    vacansies_table = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language_name in programming_languages:
        vacansies_table.append([language_name, language_statistic[language_name]['vacancies_found'], language_statistic[language_name]['vacancies_processed'], language_statistic[language_name]['average_salary']])
    table = AsciiTable(vacansies_table)
    return table.table
    

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

            vacancies = page_response.json()["items"]
            average_salaries = []
            for vacancy_num, vacancy in enumerate(vacancies):
                salary = vacancy["salary"]
                if salary != None:
                    payment_from = salary['from']
                    payment_to = salary['to']
                    average_salaries.append(predict_rub_salary(payment_from, payment_to))

                    average_salary = int((sum(average_salaries)/len(average_salaries)))
            
            if page >= page_response.json()['pages']-1:
                break
             
        vacancies_statistics = {
            "vacancies_found": page_response.json()["found"],
            "vacancies_processed": len(average_salaries),
            "average_salary": average_salary
        }

        hh_statistics[language_name] = vacancies_statistics
    return hh_statistics 


def main():
    programming_languages = ["java", "javascript", "python", "C++", "C#", "C"]
    super_job_statistics = get_super_job_statistics(programming_languages)
    print(create_table(programming_languages, super_job_statistics))
    hh_ru_statistics = get_hh_statistics(programming_languages)
    print(create_table(programming_languages, hh_ru_statistics))

if __name__=="__main__":
    main()