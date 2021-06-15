from bs4 import BeautifulSoup
import requests
import string
import csv

dlmf_id = []
zbl_code = []


def process_li(a_li):
    div_list = a_li.find_all("div", {"class": "bibblock"})
    for a_div in div_list:
        a_list = a_div.find_all("a", {"class": "zbl"})
        for a_hit in a_list:
            if a_hit:
                return True, a_hit["href"].split("an:")[1]
    return False, ""


def scrape_page(letter):
    if letter == "A":
        letter = ""
    source = requests.get(
        "https://web.archive.org/web/20101119144452/http:"
        "//dlmf.nist.gov/bib/" + "/" + letter)
    html_text = source.text
    soup = BeautifulSoup(html_text, features="html.parser")

    lis = soup.find_all("li", {"class": "bibitem"})

    for a_li in lis:
        should_process_tuple = process_li(a_li)

        if should_process_tuple[0]:
            div_list = a_li.find_all("div", {"class": "bibblock"})

            for a_div_hit in div_list:
                a_tag_list = a_div_hit.find_all("a", {"class": "ref"})

                for a_tag_cited_class in a_tag_list:
                    if (len(a_tag_cited_class['class']) == 1
                            and "dlmf.nist.gov" in a_tag_cited_class["href"]):
                        zbl_code.append(should_process_tuple[1])
                        dlmf_id.append(a_tag_cited_class["href"].split(
                            "dlmf.nist.gov")[1])


upper_list = list(string.ascii_uppercase)
for each_letter in upper_list:
    scrape_page(each_letter)

together_list = []
together_list.append(zbl_code)
together_list.append(dlmf_id)
zipped_list = list(zip(*together_list))


def write_csv_2010():
    with open("dlmf_dataset_2010.csv", "w", newline="") as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        for each_line in zipped_list:
            wr.writerow(each_line)


write_csv_2010()
