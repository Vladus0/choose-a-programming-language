from dotenv import load_dotenv
from super_job import get_super_job_statistics
from hh_ru import get_hh_statistics
from terminaltables import AsciiTable


def create_table(programming_languages, language_statistic):
    vacansies_table = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language_name in programming_languages:
        vacansies_table.append([language_name, language_statistic[language_name]['vacancies_found'], language_statistic[language_name]['vacancies_processed'], language_statistic[language_name]['average_salary']])
    table = AsciiTable(vacansies_table)
    return table.table

def main():
    load_dotenv()
    programming_languages = ["java", "javascript", "python", "C++", "C#", "C"]
    super_job_statistics = get_super_job_statistics(programming_languages)
    print(create_table(programming_languages, super_job_statistics))
    hh_ru_statistics = get_hh_statistics(programming_languages)
    print(create_table(programming_languages, hh_ru_statistics))


if __name__=="__main__":
    main()