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


def scrape_page(letter):
    if letter == "A":
        letter = ""
    source = requests.get("https://web.archive.org/web/20141127175811/"
                          "http://dlmf.nist.gov/bib" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, "html.parser")

    dls = soup.find_all("dl")
    for a_dl in dls:
        should_process_tuple = process_dl(a_dl)
        if should_process_tuple[0]:

            dds = a_dl.find_all("dd")
            for a_dd in dds:
                a_tag_list = a_dd.find_all("a", {"class": "ltx_ref"})
                for a_tag_cited_class in a_tag_list:

                    if "dlmf.nist.gov" in a_tag_cited_class["href"]:
                        zbl_code.append(should_process_tuple[1])
                        dlmf_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1][1:])


upper_list = list(string.ascii_uppercase)
for each_letter in upper_list:
    scrape_page(each_letter)

together_list = []
together_list.append(zbl_code)
together_list.append(dlmf_id)
zipped_list = list(zip(*together_list))


def write_csv_2014():
    with open("csv_files/dlmf_dataset_2014.csv", "w", newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for each_line in zipped_list:
            wr.writerow(each_line)


write_csv_2014()