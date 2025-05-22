from dotenv import load_dotenv
from super_job import get_super_job_statistics
from hh_ru import get_hh_statistics
from terminaltables import AsciiTable
import os


def create_table(language_statistic):
    vacansies_table = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language_name, statistic in language_statistic.items():
        vacansies_table.append([language_name, statistic['vacancies_found'], statistic['vacancies_processed'], statistic['average_salary']])
    table = AsciiTable(vacansies_table)
    return table.table

def main():
    load_dotenv()
    super_job_key = os.environ["SUPER_JOB_KEY"]
    programming_languages = ["java", "javascript", "python", "C++", "C#", "C"]
    super_job_statistics = get_super_job_statistics(programming_languages, super_job_key)
    print(create_table(super_job_statistics))
    hh_ru_statistics = get_hh_statistics(programming_languages)
    print(create_table(hh_ru_statistics))


if __name__=="__main__":
    main()