import requests, json, sys, time, random, os
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
    try:
        name = soup.find(attrs={"class":"bloko-header-section-1"}).text
    except:
        name = ""
    try:
        salary = soup.find(attrs={"class":"bloko-header-section-2 bloko-header-section-2_lite"}).text.replace("\xa0", "")
    except:
        salary = ""
    try:
        tags = [tag.text for tag in soup.find(attrs={"class":"bloko-tag-list"}).find_all(attrs={"class":"bloko-tag__section_text"})]
    except:
        tags = []
    try:
        requirements = [requirement.text for requirement in soup.find("div", attrs={"class":"g-user-content"}).find_all("ul")[1].find_all("li")]
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
        address = ''
    try:
        published = soup.find(attrs={"class":"vacancy-creation-time-redesigned"}).text.replace("\xa0"," ")
    except:
        published =''
    try:
        experience = soup.find(attrs={"class":"vacancy-description-list-item"}).text
    except:
        experience = ''
    vacancy = {
        "name":name,
        'experience':experience,
        "salary":  salary,
        "tags":tags,
        "requirements":requirements,
        "recommended_skills":recommended_skills,
        "employer":employer,
        'address': address,
        'published':published
    }
    return vacancy


if __name__=="__main__":
    vacancie = 1
    for a in get_links():
        print(a)
        data = json.dumps(get_vacancies(a))
        time.sleep(1)

