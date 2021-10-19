import configparser


# tuple of all partners for zblinks API
partners = ("DLMF",)
partners = tuple(p.lower() for p in partners)


config = configparser.ConfigParser()
config.read("config.ini")
username = config["DB"]["username"]
password = config["DB"]["password"]
host = config["DB"]["host"]
db = config["DB"]["database"]

api_key = config["keys"]["API-KEY"]

params_dict = {
    "host"      : host,
    "database"  : db,
    "user"      : username,
    "password"  : password
}

# url for link requests
link_url = config["zblinks"]["link_url"]

arg_names = {
    "document": "DE number",
    "link_ext_id": "external id",
    "link_partner": "partner",
    "edit_link_ext_id": "new_external_id",
    "date": "link_publication_date"
}
