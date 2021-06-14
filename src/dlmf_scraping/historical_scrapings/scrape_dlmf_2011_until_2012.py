from bs4 import BeautifulSoup
import requests
import string
import csv

dlmf_id = []
zbl_code = []


def process_dl(a_dl):
    dds = a_dl.find_all("dd")
    for a_dd in dds:
        a_tag_list = a_dd.find_all("a", {"class": "zbl"})
        for a_tag in a_tag_list:
            if a_tag:
                return True, a_tag["href"].split("an:")[1]
    return False, ""


def scrape_page(letter, dlmf_html_year):
    if letter == "A":
        letter = ""
    source = requests.get(dlmf_html_year + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, features="html.parser")

    dls = soup.find_all("dl")

    for a_dl in dls:
        should_process_tuple = process_dl(a_dl)

        if should_process_tuple[0]:

            dds = a_dl.find_all("dd")

            for a_dd in dds:
                a_tag_list = a_dd.find_all("a", {"class": "ref citedby"})

                for a_tag_cited_class in a_tag_list:

                    if "dlmf.nist.gov" in a_tag_cited_class["href"]:
                        zbl_code.append(should_process_tuple[1])
                        dlmf_id.append(
                            a_tag_cited_class["href"].split(
                                "dlmf.nist.gov")[1]
                        )


def write_csv(dlmf_html_year):
    upper_list = list(string.ascii_uppercase)
    together_list = []
    for each_letter in upper_list:
        scrape_page(each_letter, dlmf_html_year)
    together_list.append(zbl_code)
    together_list.append(dlmf_id)
    zipped_list = list(zip(*together_list))
    with open(
            f"dlmf_dataset_{dlmf_html_year[28:32]}.csv", "w", newline=""
    ) as csv_file:
        wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        for each_line in zipped_list:
            wr.writerow(each_line)
    csv_file.close()


dlmf_html_2011 = "https://web.archive.org/web/20111021085410/" \
              "http://dlmf.nist.gov/bib/"
dlmf_html_2012 = "https://web.archive.org/web/20121116035729/" \
              "http://dlmf.nist.gov/bib/"

write_csv(dlmf_html_2012)
write_csv(dlmf_html_2011)
