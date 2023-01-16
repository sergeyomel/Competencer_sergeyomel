from Indeed_parser import Indeed_parser


if __name__ == '__main__':
    params = {
        'path': "jsons/",
        'pages': 100,
        'json_size': 1000
    }

    parser = Indeed_parser()
    parser.get_vacancy()