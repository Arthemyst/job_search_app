import re
from datetime import datetime, timedelta

import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

from constants import months


def bulldog_page_job_offers() -> list:

    bulldog_list = list()

    url = "https://bulldogjob.pl/companies/jobs/s/city,Warszawa,Remote/skills,Python/experienceLevel,junior"
    flag = True
    try:
        page = requests.get(url)
    except requests.exceptions.ConnectionError as err:
        flag = False
    if flag:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="__next")
        job_elements = results.find_all(
            "div",
            class_="py-6 md:py-8 px-8 flex flex-wrap relative bg-white mb-2 rounded-lg shadow",
        )

        for job_element in job_elements:
            bulldog_dict = dict()
            job_title_element = job_element.find(
                "h3", class_="text-c28 font-medium mb-3 w-full md:hidden"
            )
            if (
                "Fullstack" not in job_title_element.text
                and "DevOps" not in job_title_element.text
                and "Test" not in job_title_element.text
            ):
                position_element = job_element.find(
                    "p", class_="tracking-05 uppercase md:my-4"
                )

                company_element = job_element.find(
                    "p",
                    class_="text-sm md:text-xxs md:text-center my-2 font-medium text-gray-300",
                )

                links = job_element.find(
                    "h3", class_="text-c28 font-medium mb-3 w-full md:hidden"
                )

                for link in links:
                    link_url = link["href"]
                pattern = re.compile(r"https?://([\w.\.\-]+)")
                website_name = pattern.match(link_url)
                page_job_element = requests.get(link_url)
                soup_page = BeautifulSoup(page_job_element.content, "html.parser")
                publication_date_element = soup_page.find(
                    "p", class_="text-gray-300 text-xs xl:text-sm mb-0.5"
                )
                days_after_publication = int(
                    re.findall(r"\b\d+\b", publication_date_element.text.strip())[0]
                )
                publication_date = (
                    datetime.today() - (timedelta(days=days_after_publication))
                ).strftime("%Y-%m-%d")

                bulldog_dict["publication_date"] = publication_date
                bulldog_dict["company"] = company_element.text.strip()
                bulldog_dict["title"] = job_title_element.text.strip()
                bulldog_dict["position"] = position_element.text.strip().capitalize()
                bulldog_dict["website"] = website_name[0]
                bulldog_dict["link_url"] = link_url

                bulldog_list.append(bulldog_dict)
    return bulldog_list


def nofluffjobs_page_job_offers() -> list:

    nofluffjobs_list = list()

    url = "https://nofluffjobs.com/pl/praca-zdalna/python?criteria=city%3Dwarszawa%20seniority%3Dtrainee,junior%20%20salary<pln12000m&page=1"

    flag = True
    try:
        page = requests.get(url)
    except requests.exceptions.ConnectionError as err:
        flag = False
    if flag:
        soup = BeautifulSoup(page.content, "html.parser")

        for job_element in soup.select(
            'a[class*="posting-list-item posting-list-item--"]'
        ):

            nofluffjobs_dict = dict()
            company_element = job_element.find(
                "span", class_="d-block posting-title__company text-truncate"
            )
            job_title_element = job_element.find(
                "h3",
                class_="posting-title__position text-truncate color-main ng-star-inserted",
            )
            if (
                "Fullstack" not in job_title_element.text
                and "DevOps" not in job_title_element.text
                and "Golang" not in job_title_element.text
                and "Test" not in job_title_element.text
            ):
                link_url = "https://nofluffjobs.com" + job_element["href"]
                pattern = re.compile(r"https?://([\w.\.\-]+)")
                website_name = pattern.match(link_url)
                page_job_element = requests.get(link_url)
                soup_page = BeautifulSoup(page_job_element.content, "html.parser")
                position = soup_page.find("span", class_="mr-10 font-weight-medium")
                publication_date_element = soup_page.find(
                    "div", class_="posting-time-row"
                )

                days_after_publication = re.findall(
                    r"\b\d+\b", publication_date_element.text.strip()
                )
                if len(days_after_publication) == 0:
                    publication_date = datetime.today().strftime("%Y-%m-%d")

                else:
                    publication_date = (
                        datetime.today()
                        - (timedelta(days=int(days_after_publication[0])))
                    ).strftime("%Y-%m-%d")

                nofluffjobs_dict["publication_date"] = publication_date
                nofluffjobs_dict["company"] = company_element.text.strip()
                nofluffjobs_dict["title"] = job_title_element.text.strip()
                nofluffjobs_dict["position"] = position.text.strip()
                nofluffjobs_dict["website"] = website_name[0]
                nofluffjobs_dict["link_url"] = link_url

                nofluffjobs_list.append(nofluffjobs_dict)
    return nofluffjobs_list


def pracuj_page_job_offers() -> list:
    pracuj_list = list()

    url = "https://www.pracuj.pl/praca/python;kw/warszawa;wp?rd=30&et=1%2c17&tc=0%2c3%2c2&ws=0&wm=full-office%2chybrid%2chome-office"
    flag = True
    try:
        page = requests.get(url)
    except requests.exceptions.ConnectionError as err:
        flag = False
    if flag:
        soup = BeautifulSoup(page.content, "html.parser")

        for job_element in soup.find_all(
            lambda tag: tag.name == "li"
            and tag.get("class") == ["results__list-container-item"]
        ):

            pracuj_dict = dict()

            link_element = job_element.select('div[class*="offer__info"]')
            if len(link_element) != 0:
                job_title_element = job_element.find(
                    "a", class_="offer-details__title-link"
                )
                if (
                    "Fullstack" not in job_title_element.text
                    and "DevOps" not in job_title_element.text
                    and "Golang" not in job_title_element.text
                    and "Test" not in job_title_element.text
                ):
                    company_element = job_element.find("p", class_="offer-company")
                    publication_date_element = job_element.find(
                        "span", class_="offer-actions__date"
                    )
                    publication_date_text = publication_date_element.text.strip().split(
                        " "
                    )[1:]
                    month_name = months[publication_date_text[1]]
                    # change polish name of month to number ex. sierpnia to 8
                    publication_date_text[1] = str(month_name)
                    publication_date = "-".join(publication_date_text)
                    publication_date = datetime.strptime(
                        publication_date, "%d-%m-%Y"
                    ).strftime("%Y-%m-%d")

                    link_url = job_title_element["href"]
                    link_pattern = re.compile(r"https?://([\w.\.\-]+)")
                    website_name = link_pattern.match(link_url)
                    page_job_element = requests.get(link_url)
                    soup_page = BeautifulSoup(page_job_element.content, "html.parser")
                    position = soup_page.select('li[class*="offer-view"]')
                    if "unior" in str(position):
                        position_pattern = "Junior"
                    elif "rainee" in str(position) or "staż" in str(position):
                        position_pattern = "Trainee"
                    else:
                        position_pattern = "no info"

                    pracuj_dict["publication_date"] = publication_date
                    pracuj_dict["company"] = company_element.text.strip()
                    pracuj_dict["title"] = job_title_element.text.strip()
                    pracuj_dict["position"] = position_pattern
                    pracuj_dict["link_url"] = link_url
                    pracuj_dict["website"] = website_name[0]
                    pracuj_list.append(pracuj_dict)
    return pracuj_list


@st.cache
def merge_dataframes():

    nofluffjobs_list = nofluffjobs_page_job_offers()
    df_raw_1 = pd.DataFrame.from_records(nofluffjobs_list)
    df_1 = df_raw_1.copy()

    bulldogjob_list = bulldog_page_job_offers()
    df_raw_2 = pd.DataFrame.from_records(bulldogjob_list)
    df_2 = df_raw_2.copy()

    pracuj_list = pracuj_page_job_offers()
    df_raw_3 = pd.DataFrame.from_records(pracuj_list)
    df_3 = df_raw_3.copy()

    df_merged = pd.concat([df_1, df_2, df_3], axis=0, ignore_index=True)
    if len(df_merged) != 0:

        df_merged["publication_date"] = pd.to_datetime(
            df_merged["publication_date"], infer_datetime_format=True
        )
        df_merged.drop_duplicates(
            subset=["publication_date", "company", "title"],
            inplace=True,
            ignore_index=True,
        )
        df_merged["publication_date"] = df_merged["publication_date"].dt.strftime(
            "%Y-%m-%d"
        )
        df_merged.sort_values(["publication_date"], inplace=True, ascending=False)

    return df_merged
