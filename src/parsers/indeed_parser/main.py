from Indeed_parser import Indeed_parser


if __name__ == '__main__':
    params = {
        'path': "jsons/",  # куда будут сохраняться json'ы
        'pages': 10,  # количество страниц для каждого поискогого запроса, 1 страница = 15 ваканский
        'json_size': 100  # количество ваканский в одном json файле
    }

    parser = Indeed_parser()
    parser.get_vacancy()