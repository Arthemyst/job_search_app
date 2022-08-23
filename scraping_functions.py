import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import streamlit as st

@st.cache
def bulldog_page_job_offers() -> list:

    bulldog_list = list()

    url = "https://bulldogjob.pl/companies/jobs/s/city,Warszawa,Wrocław,Remote/skills,Python/experienceLevel,junior"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="__next")
    job_elements = results.find_all("div", class_="py-6 md:py-8 px-8 flex flex-wrap relative bg-white mb-2 rounded-lg shadow")
    
    for job_element in job_elements:
        bulldog_dict = dict()
        job_title_element = job_element.find("h3", class_="text-c28 font-medium mb-3 w-full md:hidden")
        if "Fullstack" not in job_title_element.text and "DevOps" not in job_title_element.text and "Test" not in job_title_element.text:
            position_element = job_element.find("p", class_="tracking-05 uppercase md:my-4")
            
            company_element = job_element.find("p", class_="text-sm md:text-xxs md:text-center my-2 font-medium text-gray-300")
            
            links = job_element.find("h3", class_="text-c28 font-medium mb-3 w-full md:hidden")
            
            for link in links:
                link_url = link["href"]
            page_job_element = requests.get(link_url)
            soup_page = BeautifulSoup(page_job_element.content, "html.parser")
            publication_date_element = soup_page.find("p", class_="text-gray-300 text-xs xl:text-sm mb-0.5")
            days_after_publication = int(re.findall(r'\b\d+\b', publication_date_element.text.strip())[0])
            publication_date = (datetime.today() - (timedelta(days=days_after_publication))).strftime("%Y-%m-%d")

            bulldog_dict["publication_date"] = publication_date
            bulldog_dict["company"] = company_element.text.strip()
            bulldog_dict["title"] = job_title_element.text.strip()
            bulldog_dict["position"] = position_element.text.strip().capitalize()
            bulldog_dict["link_url"] = link_url
            bulldog_list.append(bulldog_dict)
    return bulldog_list

@st.cache
def nofluffjobs_page_job_offers() -> list:

    nofluffjobs_list = list()
    

    url = "https://nofluffjobs.com/pl/praca-zdalna/python?criteria=city%3Dwarszawa%20seniority%3Dtrainee,junior%20%20salary<pln12000m&page=1"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    
    for job_element in soup.select('a[class*="posting-list-item posting-list-item--"]'):
        
        
        nofluffjobs_dict = dict()
        company_element = job_element.find("span", class_="d-block posting-title__company text-truncate")
        job_title_element = job_element.find("h3", class_="posting-title__position text-truncate color-main ng-star-inserted")
        if "Fullstack" not in job_title_element.text and "DevOps" not in job_title_element.text and "Golang" not in job_title_element.text:
            link_url = "http://nofluffjobs.com" + job_element["href"]
            page_job_element = requests.get(link_url)
            soup_page = BeautifulSoup(page_job_element.content, "html.parser")
            position = soup_page.find("span", class_="mr-10 font-weight-medium")
            publication_date_element = soup_page.find("div", class_="posting-time-row")
            
            days_after_publication = re.findall(r'\b\d+\b', publication_date_element.text.strip())
            if len(days_after_publication) == 0:
                 publication_date = datetime.today().strftime("%Y-%m-%d")
            
            else:
                publication_date = (datetime.today() - (timedelta(days=int(days_after_publication[0])))).strftime("%Y-%m-%d")
                       
            nofluffjobs_dict["publication_date"] = publication_date
            nofluffjobs_dict["company"] = company_element.text.strip()
            nofluffjobs_dict["title"] = job_title_element.text.strip()
            nofluffjobs_dict["position"] = position.text.strip()
            nofluffjobs_dict["link_url"] = link_url

            nofluffjobs_list.append(nofluffjobs_dict)
    return nofluffjobs_list

