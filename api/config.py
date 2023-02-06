from dotenv import dotenv_values

try:
    __config = dotenv_values('../.env')
    print(__config["WG_HOST"])
except:
    __config = dotenv_values('.env')
    
print("__CONFIG: " , __config)

class ConfigClass:

    def __init__(self, __config) -> None:
        self.wg_host = __config["WG_HOST"]
        self.wg_port = int(__config["WG_PORT"])
        self.wg_default_dns = __config["WG_DEFAULT_DNS"]
        self.wg_allowed_ips = __config["WG_ALLOWED_IPS"]
        self.wg_mtu = int(__config["WG_MTU"])
        self.wg_persistent_keepalive = int(__config["WG_PERSISTENT_KEEPALIVE"])
        self.api_port = int(__config["API_PORT"])

Config = ConfigClass(__config)