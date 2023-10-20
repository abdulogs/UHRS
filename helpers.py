from googletrans import Translator
import requests
from bs4 import BeautifulSoup as crawler


def translate(text):
    translator = Translator()
    data = translator.translate(text, dest='ur')
    return data.text


def childreninfo(section):
    description = ""
    for children in section:
        if children.name == 'p':
            description += str(children.text)

        if children.name == 'ul':
            for item in children.findAll('li'):
                description += str(item.text) + ". "

    return description.strip()


def Html(url):
    req = requests.get(url)
    soup = crawler(req.content, 'html5lib')
    return soup


def fetchDisease(name):
    name = name.replace(" ", "-").lower().strip()
    disease = {}

    website = Html(f"https://www.marham.pk/all-diseases/{name}")

    website = website.findAll('div', attrs={'class': 'container'})[1]

    # details
    disease_details = website.findAll(
        'div', attrs={'class': 'row mt-2 bg-white padding'})[1]
    disease["name"] = translate(name.replace("-", " "))
    description = childreninfo(disease_details.div)
    disease["description"] = translate(description)

    # Doctors
    disease_details = website.find(
        'div', attrs={'class': 'row mt-2 bg-white padding mt-2'})
    doctors_details = website.findAll(
        'div', attrs={'class': 'card ml-1 box-shadow-sm ga-event-listing-calldoctor-card'})

    # Doctors
    try:
        doctors = []
        for doctor in doctors_details:
            doctor_image = doctor.find('img')['data-src']
            doctor_name = doctor.find('p', attrs={"class": "font-size-md mb-0 h2"}).text
            doctor_href = doctor.find('a', attrs={"class": "btn"})['href']
            doctors.append({
                "link": doctor_href,
                "image": doctor_image,
                "name": doctor_name
            })
        disease["doctors"] = doctors
    except:
        disease["doctors"] = None
    # # Doctors

    # summary
    try:
        disease_details = website.findAll(
            'div', attrs={'class': 'row mt-2 bg-white padding'})[2]
        summary = childreninfo(disease_details.div)
        disease["summary"] = translate(summary)
    except:
        disease["summary"] = None
    # summary

    # Symptoms
    try:
        disease_details = website.findAll(
            'div', attrs={'class': 'row mt-2 bg-white padding'})[3]
        symptoms = childreninfo(disease_details.div)
        disease["symptoms"] = translate(symptoms)
    except:
        disease["symptoms"] = None
    # Symptoms

    # Treatment
    try:
        disease_details = website.findAll(
            'div', attrs={'class': 'row mt-2 bg-white padding'})[4]
        treatment = childreninfo(disease_details.div)
        disease["treatment"] = translate(treatment)
    except:
        disease["treatment"] = None
    # Treatment

    # Risk
    try:
        disease_details = website.findAll(
            'div', attrs={'class': 'row mt-2 bg-white padding'})[5]
        risk = childreninfo(disease_details.div)
        disease["risk"] = translate(risk)
    except:
        disease["risk"] = None
    # Risk

    # Prevention
    try:
        disease_details = website.findAll(
            'div', attrs={'class': 'row mt-2 bg-white padding'})[6]
        prevention = childreninfo(disease_details.div)
        disease["prevention"] = translate(prevention)
    except:
        disease["prevention"] = None
    # Prevention

    return disease
