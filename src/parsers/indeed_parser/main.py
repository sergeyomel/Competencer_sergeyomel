from Indeed_parser import IndeedParser


if __name__ == '__main__':
    params = {
        'path': "jsons/",  # куда будут сохраняться json'ы
        'log_path': 'logs/',  # куда сохранять логи
        'start_from': 0,  # с какой страницы начинать поиск
        'pages': 3,  # количество страниц для каждого поискогого запроса, 1 страница = 15 ваканский
        'json_size': 1000,  # количество ваканский в одном json файле
        'semaphore_count': 10,  # количество одновременных корутин
    }

    parser = IndeedParser(params=params)
    parser.get_vacancies()
