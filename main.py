from dotenv import load_dotenv
from super_job import get_super_job_statistics
from hh_ru import get_hh_statistics
from create_table import create_table


def main():
    load_dotenv()
    programming_languages = ["java", "javascript", "python", "C++", "C#", "C"]
    super_job_statistics = get_super_job_statistics(programming_languages)
    print(create_table(programming_languages, super_job_statistics))
    hh_ru_statistics = get_hh_statistics(programming_languages)
    print(create_table(programming_languages, hh_ru_statistics))


if __name__=="__main__":
    main()