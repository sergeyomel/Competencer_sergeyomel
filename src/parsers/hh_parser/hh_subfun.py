import requests, json,  time, datetime, re
from bs4 import BeautifulSoup
import fake_useragent

def get_links():
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=f'https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&hhtmFromLabel=rainbow_profession&hhtmFrom=main&page=1&specialization=1.221',
        headers={"user-agent": ua.random}

    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    try:
         page_number = int(soup.find("div", attrs={"class":"pager"}).find_all("span",recursive = False)[-1].find("a").find("span").text)
    except:
        return
    nump = 1
    for page in range(page_number):
        print(f"page number {nump}")
        nump+=1
        try:
            data = requests.get(
                url=f'https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&hhtmFromLabel=rainbow_profession&hhtmFrom=main&page={page}&specialization=1.221',
                headers={"user-agent": ua.random}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, 'lxml')
            for a in soup.find_all("a", attrs = {"class":"serp-item__title"}):
                yield f"{a.attrs['href'].split('?')[0]}"
        except Exception as e:
            print(f"{e}")
        time.sleep(1)


def text_division(list_of_text):
    if len(list_of_text) > 1:
        min = list_of_text[0]
        max = list_of_text[1]
    elif len(list_of_text) == 1:
        min = '0'
        max = list_of_text[0]

    return min, max


def text_to_date():
    pass

def get_vacancies(link):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=link,
        headers={"user-agent": ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")

    date_of_parsing = str(datetime.date.today())
    vacancy_id = str(link).split('/')[-1]

    try:
        name = soup.find(attrs={"class":"bloko-header-section-1"}).text
    except:
        name = ""

    try:
        salary = soup.find(attrs={"class":"bloko-header-section-2 bloko-header-section-2_lite"}).text.replace("\xa0", "")
        list_of_salary = re.findall(r"\S\d{3,}", salary)
        min_salary, max_salary = text_division(list_of_salary)

    except:
        min_salary = '0'
        max_salary = '0'

    try:
        experience = soup.find(attrs={"class":"vacancy-description-list-item"}).text
        list_of_exp = re.findall(r'\d', experience)
        min_exp,max_exp = text_division(list_of_exp)
    except:
        min_exp = '0'
        max_exp = '0'

    try:
        responsibText = soup.find(attrs={'class':'g-user-content'}).text
        responsibilities = re.findall(r'(\Задачи|\Обязанности|\Что предстоит делать|\Что нужно делать\Чем предстоит заниматься)(.*?)(?=\.\s\s)',responsibText)
        list_of_responsibilities = str(responsibilities)

    except:
        list_of_responsibilities = []

    try:
        tags = [tag.text for tag in soup.find(attrs={"class":"bloko-tag-list"}).find_all(attrs={"class":"bloko-tag__section_text"})]
    except:
        tags = []

    try:
        requirementsText = soup.find(attrs={'class':'g-user-content'}).text
        requirements = re.findall(r'(\Требования|\Что необходимо|\Мы ждем от вас|\Наши ожидания|Мы ждем, что вы)(.*?)(?=\.\s\s)',requirementsText)
        list_of_requirements = str(requirements[0][1]).split(';')

    except:
        list_of_requirements = []

    try:
        recommended_skillsText  = soup.find("div", attrs={"class":"g-user-content"}).text
        recommended_skills = re.findall(r'(\Будет плюсом|\Дополнительные навыки|\Плюсом может быть\Плюсом будет, если вы)(.*?)(?=\.\s\s)', recommended_skillsText)
        list_of_recommended_skills = str(recommended_skills[0][1]).split(';')

    except:
        list_of_recommended_skills = []

    try:
        employer = soup.find(attrs={"class":"vacancy-company-name"}).text.replace("\xa0"," ")
    except:
        employer = ""

    try:
        address = soup.find(attrs={"class":"bloko-link bloko-link_kind-tertiary bloko-link_disable-visited"}).text
    except:
        address = ""

    months = {'декабря':'12','января':'01','февраля':'02','марта':'03','апреля':'04','мая':'05','июня':'06','июля':'07','августа':'08','сентября':'09','октября':'10','ноября':'11'}
    try:
        published = soup.find(attrs={"class":"vacancy-creation-time-redesigned"}).text.replace("\xa0"," ")
        date = re.findall(r'\b\d{1,2}\b',published)[0]
        month = re.findall(r'(?<=\d\s).+?(?=\s\d)', published)[0]
        for i in months:
            if month == i:
                month = months.get(month)
        year = re.findall(r'\d{4}',published)[0]
        published_date = year + "-" + month + "-" + date
    except:
        published_date =''


    item = {
        "parsing":{
            "date": date_of_parsing,
            "resource": "hh"
        },
        "company": {
           "name": employer,
           "location": {
               "country": "russia",
               "city": address,
               "street": ""
           }
        },
       "vacancy": {
        "id": vacancy_id,
        "title": name,
        "publicDate": published_date,
        "description": " ",
        "workExp": {
            "min": min_exp,
            "max": max_exp
        },
        "salary": {
            "min": min_salary,
            "max": max_salary
        },
        "skills": {
            "necessary": list_of_requirements,
            "extra": list_of_recommended_skills,
            "key": tags
        },
        "responsibilities": list_of_responsibilities
        }
    }
    return item
