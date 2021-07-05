import re
import logging
import time
from configparser import ConfigParser
import numpy as np
from datetime import datetime
import aiohttp
import asyncio
import nest_asyncio

nest_asyncio.apply()


# Config file contains info on the API (Citation Matcher): url+user+pwd
def read_config(filename):
    config = ConfigParser()
    config.read(filename)
    return config


# Logging used to detect unmatched references and parsing problems
logging.getLogger("").handlers = []
logging.basicConfig(filename="info_scraping.log",
                    format="%(asctime)s - %(message)s",
                    level=logging.INFO,
                    filemode="w")


# Remove html tags
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


# Extract all references of given sequence from OEIS
async def extract(number_seq, session, sem):
    num_attempts = 0
    cutoff = 5
    url = f"https://oeis.org/search?fmt=json&q=id:A{number_seq}"
    while num_attempts < cutoff:
        async with sem:
            async with session.get(url) as resp:
                if resp.status == 200:
                    doc = await resp.json()
                    # results is a dictionary
                    # Relevant keys are "name", "reference", "link"
                    results = doc["results"][0]
                    seq_id = number_seq
                    seq_name = results["name"]
                    seq_created = results["created"]
                    # list_tot is the list of all references to be matched
                    list_tot = []
                    if "reference" in results and "link" in results:
                        list_refs = results["reference"]
                        links = results["link"]
                        list_links = list(map(lambda x: cleanhtml(x), links))
                        list_tot = list_refs + list_links
                    elif "reference" not in results and "link" in results:
                        links = results["link"]
                        list_links = list(map(lambda x: cleanhtml(x), links))
                        list_tot = list_links
                        logging.info(f"Sequence {seq_id} has no references")
                    elif "link" not in results and "reference" in results:
                        list_refs = results["reference"]
                        list_tot = list_refs
                        logging.info(f"Sequence {seq_id} has no links")
                    else:
                        logging.info(
                            f"Sequence {seq_id} has no references and no links"
                        )
                    return list_tot, seq_id, seq_name, seq_created
                else:
                    time.sleep(5)
                    num_attempts += 1
                    logging.info(
                        f"New attempt for sequence {number_seq} "
                        f"(status code OEIS  was not 200)"
                    )
    if num_attempts == cutoff:
        logging.info(
            f"5 attempts for sequence {number_seq} "
            f"(status code OEIS  was not 200)"
        )


# Match all references of a given sequence
async def match(extract_data, session, sem):
    # Provide the list of all references for a given sequence
    list_tot, seq_id, seq_name, seq_created = extract_data
    # Citation Matcher
    citation_matcher = config["zbmatch"]["url"]
    data = {"queries": [{"q": ref} for ref in list_tot]}
    num_attempts = 0
    cutoff = 5
    user = config["auth"]["username"]
    password = config["auth"]["password"]
    authentication = aiohttp.BasicAuth(
        login=user,
        password=password,
        encoding="utf-8"
    )
    while num_attempts < cutoff:
        async with sem:
            r = await session.request(method="POST", url=citation_matcher,
                                      json=data, auth=authentication)
            if r.status == 200:
                response = await r.json()
                refs = response["results"]
                # refs_matched is a list of matched references (list of dicts)
                # with filter score >=5
                # Each dictionary contains all data for all matched references
                # Relevant key is "de"
                refs_matched = []
                for item in refs:
                    if item and item[0]:
                        min_score = 7
                        item_score = item[0]["score"]
                        if item_score >= min_score:
                            refs_matched.append(item)
                        elif item_score < min_score:
                            zbl_de = item[0]["de"]
                            logging.info(
                                f"For sequence {seq_id}, DE {zbl_de} matched "
                                f"with score < {min_score}"
                            )
                    else:
                        logging.info(
                            f"For sequence {seq_id}, "
                            f"empty reference {item} detected"
                        )
                return seq_id, seq_name, seq_created, refs_matched
            else:
                time.sleep(3)
                num_attempts += 1
                logging.info(
                    f"New attempt for sequence {seq_id} "
                    f"(status code Citation Matcher was not 200)"
                )
    if num_attempts == cutoff:
        logging.info(
            f"5 attempts for sequence {seq_id} "
            f"(status code Citation Matcher was not 200)"
        )


async def async_extraction(block_start, block_end):
    sem = asyncio.Semaphore(5)
    async with aiohttp.ClientSession() as session:
        extract_tasks = []
        for sequence in range(block_start, block_end):
            extract_task = asyncio.ensure_future(
                extract(sequence, session, sem)
            )
            extract_tasks.append(extract_task)
        extract_results = await asyncio.gather(*extract_tasks)
    return extract_results


async def async_match(extract_results):
    sem = asyncio.Semaphore(5)
    async with aiohttp.ClientSession() as session:
        match_tasks = []
        for result in extract_results:
            match_task = asyncio.ensure_future(
                match(result, session, sem)
            )
            match_tasks.append(match_task)
        match_results = await asyncio.gather(*match_tasks)
    return match_results


# Write the csv file in blocks of length step
async def write_csv(initial_sequence, final_sequence, step):
    for block in range(initial_sequence, final_sequence, step):
        start_time = datetime.now()
        block_start = block
        block_end = block_start + step
        block_data = []
        extract_results = await async_extraction(block_start, block_end)
        # For each result get match
        match_results = await async_match(extract_results)
        for a_match in match_results:
            seq_id, seq_name, seq_created, refs_matched = a_match
            for ref in refs_matched:
                line = [
                    seq_id,
                    seq_name,
                    seq_created,
                    ref[0]["de"]
                ]
                if line[3]:
                    block_data.append(line)
        data_array = np.array(block_data, dtype="object")
        csv_file = f"./csv_datasets" \
                   f"/data_{block_start}_{block_end - 1}.csv"
        np.savetxt(csv_file, data_array, delimiter="|", fmt="%s")
        print(
            f"Time for block {block_start}-{block_end - 1} = "
            f"{datetime.now() - start_time}\n"
            f"Number of references in block {block_start}-{block_end - 1} = "
            f"{len(block_data)}\n"
        )


if __name__ == "__main__":
    config = read_config("config.ini")
    initial_seq = int(config["setsequences"]["initial_seq"])
    final_seq = int(config["setsequences"]["final_seq"])
    jump = int(config["setsequences"]["jump"])
    asyncio.run(write_csv(initial_seq, final_seq, jump))
