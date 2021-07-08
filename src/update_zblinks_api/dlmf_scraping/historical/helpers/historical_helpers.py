
import pandas as pd
from bs4 import BeautifulSoup
from typing import List
import requests

# ------------------------------------------------------------------------------
# Functions to select paragraphs
# ------------------------------------------------------------------------------

def process_li_2008_2010(a_li):
    div_list = a_li.find_all("div", {"class": "bibblock"})
    for a_div in div_list:
        a_list = a_div.find_all("a", {"class": "zbl"})
        for a_hit in a_list:
            if a_hit:
                return True, a_hit["href"].split("an:")[1]
    return False, ""


def process_dl_2011_2019(a_dl):
    dds = a_dl.find_all("dd")
    for a_dd in dds:
        a_tag_list = a_dd.find_all("a", {"class": "zbl"})
        for a_tag in a_tag_list:
            if a_tag:
                return True, a_tag["href"].split("an:")[1]
    return False, ""


def process_dl_2020(a_dl):
    dds = a_dl.find_all("dd")
    for a_dd in dds:
        a_tag_list = a_dd.find_all("a", {"class": "zbl"})
        for a_tag in a_tag_list:
            if a_tag:
                return True, a_tag["href"].split("zbmath.org/")[1]
    return False, ""

# ------------------------------------------------------------------------------
# Functions to scrape
# ------------------------------------------------------------------------------

def scrape_page_2008(letter, external_id: List, zbl_code: List):
    if letter == "A":
        letter = ""
    source = requests.get(
        "https://web.archive.org/web/20080812084157/http:"
        "//dlmf.nist.gov/bib/" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, features="html.parser")

    lis = soup.find_all("li", {"class": "bibitem"})

    for a_li in lis:
        should_process_tuple = process_li_2008_2010(a_li)

        if should_process_tuple[0]:
            div_list = a_li.find_all("div", {"class": "bibblock"})

            for a_div_hit in div_list:
                a_tag_list = a_div_hit.find_all("a", {"class": "ref"})

                for a_tag_cited_class in a_tag_list:
                    if (len(a_tag_cited_class["class"]) == 1
                            and "dlmf.nist.gov" in a_tag_cited_class["href"]):
                        zbl_code.append(should_process_tuple[1])
                        external_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])


def scrape_page_2009(letter, external_id: List, zbl_code: List):
    if letter == "A":
        letter = ""
    source = requests.get(
        "https://web.archive.org/web/20091207124848/http:"
        "//dlmf.nist.gov/bib/" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, features="html.parser")

    lis = soup.find_all("li", {"class": "bibitem"})

    for a_li in lis:
        should_process_tuple = process_li_2008_2010(a_li)

        if should_process_tuple[0]:
            div_list = a_li.find_all("div", {"class": "bibblock"})

            for a_div_hit in div_list:
                a_tag_list = a_div_hit.find_all("a", {"class": "ref"})

                for a_tag_cited_class in a_tag_list:
                    if (len(a_tag_cited_class["class"]) == 1
                            and "dlmf.nist.gov" in a_tag_cited_class["href"]):
                        zbl_code.append(should_process_tuple[1])
                        external_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])


def scrape_page_2010(letter, external_id: List, zbl_code: List):
    if letter == "A":
        letter = ""
    source = requests.get(
        "https://web.archive.org/web/20101119144452/http:"
        "//dlmf.nist.gov/bib/" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, features="html.parser")

    lis = soup.find_all("li", {"class": "bibitem"})

    for a_li in lis:
        should_process_tuple = process_li_2008_2010(a_li)

        if should_process_tuple[0]:
            div_list = a_li.find_all("div", {"class": "bibblock"})

            for a_div_hit in div_list:
                a_tag_list = a_div_hit.find_all("a", {"class": "ref"})

                for a_tag_cited_class in a_tag_list:
                    if (len(a_tag_cited_class['class']) == 1
                            and "dlmf.nist.gov" in a_tag_cited_class["href"]):
                        zbl_code.append(should_process_tuple[1])
                        external_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])


def scrape_page_2011(letter, external_id: List, zbl_code: List):
    if letter == "A":
        letter = ""
    source = requests.get(
        "https://web.archive.org/web/20111021085410/http:"
        "//dlmf.nist.gov/bib/" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, features="html.parser")

    dls = soup.find_all("dl")

    for a_dl in dls:
        should_process_tuple = process_dl_2011_2019(a_dl)

        if should_process_tuple[0]:

            dds = a_dl.find_all("dd")

            for a_dd in dds:
                a_tag_list = a_dd.find_all("a", {"class": "ref citedby"})

                for a_tag_cited_class in a_tag_list:

                    if "dlmf.nist.gov" in a_tag_cited_class["href"]:
                        zbl_code.append(should_process_tuple[1])
                        external_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])


def scrape_page_2012(letter, external_id: List, zbl_code: List):
    if letter == "A":
        letter = ""
    source = requests.get(
        "https://web.archive.org/web/20121116035729/http:"
        "//dlmf.nist.gov/bib/" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, features="html.parser")

    dls = soup.find_all("dl")

    for a_dl in dls:
        should_process_tuple = process_dl_2011_2019(a_dl)

        if should_process_tuple[0]:

            dds = a_dl.find_all("dd")

            for a_dd in dds:
                a_tag_list = a_dd.find_all("a", {"class": "ref citedby"})

                for a_tag_cited_class in a_tag_list:

                    if "dlmf.nist.gov" in a_tag_cited_class["href"]:
                        zbl_code.append(should_process_tuple[1])
                        external_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])


def scrape_page_2013(letter, external_id: List, zbl_code: List):
    if letter == "A":
        letter = ""
    source = requests.get("https://web.archive.org/web/20131127014548/"
                          "http://dlmf.nist.gov/bib" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, "html.parser")

    dls = soup.find_all("dl")
    for a_dl in dls:
        should_process_tuple = process_dl_2011_2019(a_dl)
        if should_process_tuple[0]:

            dds = a_dl.find_all("dd")
            for a_dd in dds:
                a_tag_list = a_dd.find_all("a", {"class": "ltx_ref"})
                for a_tag_cited_class in a_tag_list:

                    if "dlmf.nist.gov" in a_tag_cited_class["href"]:
                        zbl_code.append(should_process_tuple[1])
                        external_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])


def scrape_page_2014(letter, external_id: List, zbl_code: List):
    if letter == "A":
        letter = ""
    source = requests.get("https://web.archive.org/web/20141127175811/"
                          "http://dlmf.nist.gov/bib" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, "html.parser")

    dls = soup.find_all("dl")
    for a_dl in dls:
        should_process_tuple = process_dl_2011_2019(a_dl)
        if should_process_tuple[0]:

            dds = a_dl.find_all("dd")
            for a_dd in dds:
                a_tag_list = a_dd.find_all("a", {"class": "ltx_ref"})
                for a_tag_cited_class in a_tag_list:

                    if "dlmf.nist.gov" in a_tag_cited_class["href"]:
                        zbl_code.append(should_process_tuple[1])
                        external_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])


def scrape_page_2015(letter, external_id: List, zbl_code: List):
    if letter == "A":
        letter = ""
    source = requests.get("https://web.archive.org/web/20151218103036/"
                          "http://dlmf.nist.gov/bib" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, "html.parser")

    dls = soup.find_all("dl")
    for a_dl in dls:
        should_process_tuple = process_dl_2011_2019(a_dl)
        if should_process_tuple[0]:

            dds = a_dl.find_all("dd")
            for a_dd in dds:
                a_tag_list = a_dd.find_all("a", {"class": "ltx_ref"})
                for a_tag_cited_class in a_tag_list:

                    if "dlmf.nist.gov" in a_tag_cited_class["href"]:
                        zbl_code.append(should_process_tuple[1])
                        external_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])


def scrape_page_2016(letter, external_id: List, zbl_code: List):
    if letter == "A":
        letter = ""
    source = requests.get("https://web.archive.org/web/20161230225724/"
                          "http://dlmf.nist.gov/bib" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, "html.parser")

    dls = soup.find_all("dl")
    for a_dl in dls:
        should_process_tuple = process_dl_2011_2019(a_dl)
        if should_process_tuple[0]:

            dds = a_dl.find_all("dd")
            for a_dd in dds:
                a_tag_list = a_dd.find_all("a", {"class": "ltx_ref"})
                for a_tag_cited_class in a_tag_list:

                    if "dlmf.nist.gov" in a_tag_cited_class["href"]:
                        zbl_code.append(should_process_tuple[1])
                        external_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])


def scrape_page_2017(letter, external_id: List, zbl_code: List):
    if letter == "A":
        letter = ""
    source = requests.get("https://web.archive.org/web/20171111221944/"
                          "http://dlmf.nist.gov/bib" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, "html.parser")

    dls = soup.find_all("dl")
    for a_dl in dls:
        should_process_tuple = process_dl_2011_2019(a_dl)
        if should_process_tuple[0]:

            dds = a_dl.find_all("dd")
            for a_dd in dds:
                a_tag_list = a_dd.find_all("a", {"class": "ltx_ref"})
                for a_tag_cited_class in a_tag_list:

                    if "dlmf.nist.gov" in a_tag_cited_class["href"]:
                        zbl_code.append(should_process_tuple[1])
                        external_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])


def scrape_page_2018(letter, external_id: List, zbl_code: List):
    if letter == "A":
        letter = ""
    source = requests.get("https://web.archive.org/web/20181010051553/"
                          "http://dlmf.nist.gov/bib" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, "html.parser")

    dls = soup.find_all("dl")
    for a_dl in dls:
        should_process_tuple = process_dl_2011_2019(a_dl)
        if should_process_tuple[0]:

            dds = a_dl.find_all("dd")
            for a_dd in dds:
                a_tag_list = a_dd.find_all("a", {"class": "ltx_ref"})
                for a_tag_cited_class in a_tag_list:

                    if "dlmf.nist.gov" in a_tag_cited_class["href"]:
                        zbl_code.append(should_process_tuple[1])
                        external_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])


def scrape_page_2019(letter, external_id: List, zbl_code: List):
    if letter == "A":
        letter = ""
    source = requests.get("https://web.archive.org/web/20191218070644/"
                          "http://dlmf.nist.gov/bib" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, "html.parser")

    dls = soup.find_all("dl")
    for a_dl in dls:
        should_process_tuple = process_dl_2011_2019(a_dl)
        if should_process_tuple[0]:

            dds = a_dl.find_all("dd")
            for a_dd in dds:
                a_tag_list = a_dd.find_all("a", {"class": "ltx_ref"})
                for a_tag_cited_class in a_tag_list:

                    if "dlmf.nist.gov" in a_tag_cited_class["href"]:
                        zbl_code.append(should_process_tuple[1])
                        external_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])


def scrape_page_2020(letter, external_id: List, zbl_code: List):
    if letter == "A":
        letter = ""
    source = requests.get("https://web.archive.org/web/20201230110228/https:"
                          "//dlmf.nist.gov/bib" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, "html.parser")

    dls = soup.find_all("dl")
    for a_dl in dls:
        should_process_tuple = process_dl_2020(a_dl)
        if should_process_tuple[0]:

            dds = a_dl.find_all("dd")
            for a_dd in dds:
                a_tag_list = a_dd.find_all("a", {"class": "ltx_ref"})
                for a_tag_cited_class in a_tag_list:

                    if "dlmf.nist.gov" in a_tag_cited_class["href"]:
                        zbl_code.append(should_process_tuple[1])
                        external_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])

# ------------------------------------------------------------------------------
# Create the dataframe
# ------------------------------------------------------------------------------

def get_dataframe(zipped_list: List):
    df = pd.DataFrame.from_records(
        data=zipped_list,
        columns=["zbl_code", "external_id"]
    )
    return df
