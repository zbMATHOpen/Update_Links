import configparser
import os


# tuple of all partners for zblinks API
partners = ("DLMF",)
partners = tuple(p.lower() for p in partners)

arg_names = {
    "document": "DE number",
    "link_ext_id": "external id",
    "link_partner": "partner",
    "edit_link_ext_id": "new_external_id",
    "date": "link_publication_date"
}

config = configparser.ConfigParser()
config_path = os.getenv(
    "UPDATE_API_CONFIG", "/etc/update_zblinks_api/config.ini"
)
config.read(config_path)


def get_connection_params_dict():
    username = config["DB"]["username"]
    password = config.get("DB","password",raw=True)
    host = config["DB"]["host"]
    db = config["DB"]["database"]

    params_dict = {
        "host"      : host,
        "database"  : db,
        "user"      : username,
        "password"  : password
    }

    return params_dict

def get_key():
    api_key = config["keys"]["API-KEY"]
    return api_key


# url for link requests
def get_link_url():
    link_url = config.get("zblinks","link_url",raw=True)
    return link_url
