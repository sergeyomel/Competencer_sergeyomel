import re

class DataHandler:

    @staticmethod
    def del_tags(data):
        str_symbols = ['\\r', '\\n','</li>']

        for i in str_symbols:
            if i == '</li>':
                data = data.replace(i,';')
            elif i == '\\n':
                data = data.replace(i, ' ')
            elif i == '\\r':
                data = data.replace(i,'')

        data = re.sub(r'(?<=<).+?(?=>)', '', data).replace('<>', '')
        return data

    @staticmethod
    def del_comma_in_list(data):
        new_list = []
        for i in data:
            str = i.replace(re.search(r'.*?(?=[A-Za-zА-Яа-я])', i)[0], '')
            new_list.append(str)

        return new_list