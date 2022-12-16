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

def get_vacancies(link):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=link,
        headers={"user-agent": ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, "lxml")
    v = soup.text
    vacancy_id = str(link).split('/')[-1]
    f = open('hh.txt', 'w')
    f.write('v')
    f.close()

    try:
        name = soup.find(attrs={"class":"bloko-header-section-1"}).text
    except:
        name = ""
    try:
        salary = soup.find(attrs={"class":"bloko-header-section-2 bloko-header-section-2_lite"}).text.replace("\xa0", "")
    except:
        salary = ""
    value = re.findall(r"\S\d{3,}", salary)
    min = ""
    max = ""
    if len(value) > 1:
        min = value[0]
        max = value[1]
    elif len(value) == 1:
        max = value[0]
    #Вставь код с 69-83 строчек
    try:
        responsibText = soup.find(attrs={'class':'g-user-content'}).text
        responsibilities = re.findall(r'(\Задачи|\Обязанности|\Что предстоит делать|\Что нужно делать\Чем предстоит заниматься)([\s\w*():;,-]+)[^\S]',responsibText)
    except:
        responsibilities = ''
    try:
        tags = [tag.text for tag in soup.find(attrs={"class":"bloko-tag-list"}).find_all(attrs={"class":"bloko-tag__section_text"})]
    except:
        tags = []
    try:
        requirementsText = soup.find(attrs={'class':'g-user-content'}).text
        requirements = re.findall(r'(\Требования|\Что необходимо|\Мы ждем от вас|\Наши ожидания|Мы ждем, что вы)([\s\w*():;""/!.,-]+)[^\S]',requirementsText)
    except:
        requirements = ""
    try:
        recommended_skills = [recommended_skill.text for recommended_skill in soup.find("div", attrs={"class":"g-user-content"}).find_all("ul")[2].find_all("li")]
    except:
        recommended_skills = ""
    try:
        employer = soup.find(attrs={"class":"vacancy-company-name"}).text.replace("\xa0"," ")
    except:
        employer = ""
    try:
        address = soup.find(attrs={"class":"bloko-link bloko-link_kind-tertiary bloko-link_disable-visited"}).text
    except:
        address = ""
    try:
        published = soup.find(attrs={"class":"vacancy-creation-time-redesigned"}).text.replace("\xa0"," ")
    except:
        published =''
    try:
        experience = soup.find(attrs={"class":"vacancy-description-list-item"}).text
    except:
        experience = ''

    date_of_parsing = str(datetime.date.today())

    item = {
        "parcing":{
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
        "vacancy_id": vacancy_id,
        "publicDate": published,
        "description": " ",
        "workExp": experience,
        "salary": {
            "min": min,
            "max": max
        },
        "skills": {
            "necessary": requirements,
            "extra": recommended_skills,
            "key": tags
        },
        "responsibilities": responsibilities
        }
    }
    return item