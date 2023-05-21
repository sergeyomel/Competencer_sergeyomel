import re, json, os

import PyPDF2



print(os.listdir())
json_array = []
for filename in os.listdir('pdf'):
   with open(os.path.join('pdf', filename), 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    with open('PDFparse.txt', 'w', encoding='UTF-8') as PDFtext:
        PDFtext.write('')
    for page_num in range(len(pdf_reader.pages)):
        pdf_page = pdf_reader.pages[page_num]
        text = pdf_page.extract_text()
        text = text.replace('\n', ' ')
        with open('PDFparse.txt', 'a', encoding='UTF-8') as PDFtext:
            PDFtext.write(text)


    with open('PDFparse.txt', 'r', encoding='UTF-8') as PDFtext:
        text = PDFtext.read()
    try:
        purpose = re.split(r'\s\d+\..+?(?=[А-Яа-я])',re.search(r'ЦЕЛИ.+?(?=\d).+?(?=\s2)',text)[0])
        purpose.pop(0)
        print(purpose)

    except:
        purpose = []

    try:
        structure = re.search(r'\s2\.1\..+?(?=\s3)',text)[0]
    except:
        structure = []

    try:
        requirements = re.split(r'\s\d+\..+?(?=[А-Яа-я])',re.search(r'\s2\.1\..+?(?=\s2\.2)', structure)[0])
        requirements.pop(0)
        print(requirements)
    except:
        requirements = []

    try:
        disciplines = re.split(r'\s\d+\..+?(?=[А-Яа-я])',re.search(r'\s2\.2\..+', structure)[0])
        disciplines.pop(0)
        print(disciplines)
    except:
        disciplines = []

    try:
        skills = re.search(r'\s3\..+?(?=\s4)',text)[0]
    except:
        skills = []



    try:
        comp = re.search(r'\s3\..+?(?=\s3)',skills)[0]

        competency = re.sub(r'Знать:\s', 'УК-1 ', comp)
        competency = re.sub(r'Уметь:\s', 'УК-1.3 ', competency)
        competency = re.sub(r'Владеть:\s','УК-1.3 ', competency)

        competency = re.split(r'\s[А-Я]+-\d.+?(?=[А-Яа-я])',competency)
        competency.pop(0)
        print(competency)

    except:
        competency = re.split(r'\s[А-Я]+-\d.+?(?=[А-Яа-я])',re.search(r'\s3\..+?(?=\s3)',skills)[0])
        competency.pop(0)
        print(competency)

    try:
        knowledge = re.split(r'\s\d+\..+?(?=[А-Яа-я])',re.search(r'\s3\.1\..+?(?=3\.2)',text)[0])
        knowledge.pop(0)
        print(knowledge)

    except:
        knowledge = []


    try:
        can = re.split(r'\s\d+\..+?(?=[А-Яа-я])',re.search(r'\s3\.2\..+?(?=3\.3)',text)[0])
        can.pop(0)
        print(can)

    except:
        can = []


    try:
        use = re.split(r'\s\d+\..+?(?=[А-Яа-я])',re.search(r'\s3\.3\..+?(?=Наим)',text)[0])
        use.pop(0)
        print(use)

    except:
        use = []


    current_dict = {
        "Цели освоения дисциплины (модуля)": purpose,
        "Место дисциплины (модуля) в структуре образовательной программы": {
            "Требования к предварительной подготовке обучающегося": requirements,
            "Дисциплины (модули) и практики, для которых освоение данной дисциплины (модуля) необходимо как предшествующее": disciplines
        },
        "Компетенции обучающегося, формируемые в результате освоения дисциплины (модуля)": {
            "Знать": knowledge,
            "Уметь": can,
            "Владеть": use
        }
    }

    json_array.append(current_dict)
with open(f'ParsedData.json', 'w',encoding='UTF-8') as outfile:
    json.dump(json_array, outfile, ensure_ascii=False)