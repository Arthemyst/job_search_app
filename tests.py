import pytest
import pandas as pd
from scraping_functions import (
    bulldog_page_job_offers,
    merge_dataframes,
    nofluffjobs_page_job_offers,
    pracuj_page_job_offers,
)


def test_nofluffjobs_wrong_url():
    url = "www.wrongpage.pl"
    nofluffjobs_empty_list = nofluffjobs_page_job_offers(url)
    assert len(nofluffjobs_empty_list) == 0


def test_nofluffjobs_good_url():
    url = "https://nofluffjobs.com/pl/praca-zdalna/python?criteria=city%3Dwarszawa%20seniority%3Dtrainee,junior%20%20salary>pln15000m&page=1"
    nofluffjobs_list = nofluffjobs_page_job_offers(url)
    assert len(nofluffjobs_list) != 0


def test_bulldogjob_wrong_url():
    url = "www.wrongpage.pl"
    bulldogjob_empty_list = bulldog_page_job_offers(url)
    assert len(bulldogjob_empty_list) == 0


def test_bulldogjob_good_url():
    bulldogjob_list = bulldog_page_job_offers()
    assert len(bulldogjob_list) != 0


def test_pracuj_wrong_url():
    url = "www.wrongpage.pl"
    pracuj_empty_list = pracuj_page_job_offers(url)
    assert len(pracuj_empty_list) == 0


def test_pracuj_good_url():
    pracuj_list = pracuj_page_job_offers()
    assert len(pracuj_list) != 0


def test_pracuj_dict_result_keys():
    pracuj_list = pracuj_page_job_offers()
    assert list(pracuj_list[0].keys()) == [
        "publication_date",
        "company",
        "title",
        "position",
        "website",
        "link_url",
    ]


def test_nofluffjobs_dict_result_keys():
    nofluffjobs_list = nofluffjobs_page_job_offers()
    assert list(nofluffjobs_list[0].keys()) == [
        "publication_date",
        "company",
        "title",
        "position",
        "website",
        "link_url",
    ]


def test_bulldogjob_dict_result_keys():
    bulldogjob_list = bulldog_page_job_offers()
    assert list(bulldogjob_list[0].keys()) == [
        "publication_date",
        "company",
        "title",
        "position",
        "website",
        "link_url",
    ]


def test_merge_dataframes_rows_not_equal_zero():
    df_merged = merge_dataframes()
    assert len(df_merged) != 0


def test_merge_dataframes_good_columns_names():
    df_merged = merge_dataframes()
    assert list(df_merged.columns) == [
        "publication date",
        "company",
        "title",
        "position",
        "website",
        "url link",
    ]
