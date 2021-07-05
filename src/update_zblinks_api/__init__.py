import configparser


config = configparser.ConfigParser()
config.read('config.ini')
username = config['DB']['username']
password = config['DB']['password']
host = config['DB']['host']
db = config['DB']['database']

params_dict = {
    "host"      : host,
    "database"  : db,
    "user"      : username,
    "password"  : password
}

# tuple of all partners for zblinks API
partners = ("DLMF")

# url for link requests
link_url = config['zblinks']['link_url']