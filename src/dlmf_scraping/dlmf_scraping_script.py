# ------------------------------------------------------------------------------
# Code to scrape the DLMF bibliography and create a CSV dataset
# ------------------------------------------------------------------------------

from bs4 import BeautifulSoup
from datetime import date
import requests
import string
import csv

today = date.today()

# Columns to be created
external_id = []
title = []
zbl_code = []


# Procedure to select only those rows in the html source with zbmath.org/
def process_dl(a_dl):
    dds = a_dl.find_all("dd")
    for a_dd in dds:
        a_tag_list = a_dd.find_all("a", {"class": "zbl"})
        for a_tag in a_tag_list:
            if a_tag:
                return True, a_tag["href"].split("zbmath.org/")[1]
    return False, ""


# Scraping procedure to extract the 4 desired columns to appear in the CSV file
def scrape_page(letter):
    if letter == "A":
        letter = ""
    source = requests.get("https://dlmf.nist.gov/bib" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, features="html.parser")
    dls = soup.find_all("dl")
    for a_dl in dls:
        should_process_tuple = process_dl(a_dl)
        if should_process_tuple[0]:
            dds = a_dl.find_all("dd")
            for a_dd in dds:
                a_tag_list = a_dd.find_all("a", {"class": "ltx_ref"})
                for a_tag_ltx_ref_class in a_tag_list:
                    if a_tag_ltx_ref_class and \
                            len(a_tag_ltx_ref_class["class"]) == 1:
                        if a_tag_ltx_ref_class["href"][0] == ".":
                            a_reference = a_tag_ltx_ref_class["href"][5:]
                            if not "bib" in a_reference:
                                external_id.append(a_reference)
                                zbl_code.append(should_process_tuple[1])
                                title_tag = a_tag_ltx_ref_class["title"]
                                if "About" in title_tag:
                                    title.append(title_tag[:-20])
                                else:
                                    title.append(title_tag)


upper_list = list(string.ascii_uppercase)
for each_letter in upper_list:
    scrape_page(each_letter)

# Prepare lists to form columns of the CSV file
together_list = []
together_list.append(zbl_code)
together_list.append(external_id)
together_list.append(title)
zipped_list = list(zip(*together_list))


# Create the CSV file to be used as dataset (after storing it in the API)
def write_csv(scraping_data):
    with open(
            f"dlmf_dataset_{today}", "w", newline=""
    ) as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for each_line in scraping_data:
            wr.writerow(each_line)


def main():
    write_csv(zipped_list)


if __name__ == "__main__":
    main()
