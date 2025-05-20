from terminaltables import AsciiTable

def create_table(programming_languages, language_statistic):
    vacansies_table = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    ]
    for language_name in programming_languages:
        vacansies_table.append([language_name, language_statistic[language_name]['vacancies_found'], language_statistic[language_name]['vacancies_processed'], language_statistic[language_name]['average_salary']])
    table = AsciiTable(vacansies_table)
    return table.table