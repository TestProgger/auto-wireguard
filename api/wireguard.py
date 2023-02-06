import subprocess
import util
from config import Config
from model import Client

def generate_keypair_and_psk():
    privkey = util.exec_command(["wg", "genkey"])
    pubkey = util.exec_command(["echo", privkey, '|', 'wg', 'pubkey'])
    psk = util.exec_command(['wg', 'genpsk'])

    return pubkey, privkey, psk


def generate_peer_record(id: int, pubkey: str, psk: str):
    peer_record = f"## BEGIN PEER-{id}\n"
    peer_record += "[Peer]\n"
    peer_record += f"PublicKey = {pubkey}\n"
    peer_record += f"PresharedKey = {psk}\n"
    peer_record += f"AllowedIPs = 0.0.0.0/0, ::/0\n"
    peer_record += f"## END PEER-{id}\n\n\n"

    return peer_record


def write_peer_record(id: int, pubkey: str, psk: str):
    with open('/etc/wireguard/wg0.conf', "rw", encoding="utf-8") as wg_file:
        wg_file.write(generate_peer_record(id, pubkey, psk))


def generate_client_config(*,
                           dns: str = "1.1.1.1",
                           privkey: str,
                           server_pubkey: str,
                           host_id: str,
                           psk: str,
                           persistent_keepalive=0,
                           wg_host: str,
                           wg_port: int
                           ):
    client_config = "[Interface]\n"
    client_config += f"PrivateKey = {privkey}"
    client_config += f"Address = 10.8.0.{host_id}/24"
    client_config += f"DNS = {dns}"
    client_config += "\n"
    client_config += "\n"
    client_config += "[Peer]\n"
    client_config += f"PublicKey = {server_pubkey}"
    client_config += f"PresharedKey = {psk}"
    client_config += "AllowedIPs = 0.0.0.0/0, ::/0"
    client_config += f"PersistentKeepalive = {persistent_keepalive}"
    client_config += f"Endpoint = {wg_host}:{wg_port}"

    return client_config


def create_client(*, 
        client_id: int, 
        wg_name: str, 
        host_id: int, 
        privkey: str, 
        pubkey: str, 
        psk: str,
        server_public_key : str,
    ):

    client = Client.create(  
                            client_id=client_id , 
                            name=wg_name ,  
                            host_id=host_id ,  
                            public_key = pubkey,
                            private_key = privkey,
                            pre_shared_key = psk
                        )
    write_peer_record( id=client.id  , pubkey=pubkey , psk=psk )

    client_config = generate_client_config(
                dns = Config.wg_default_dns,
                privkey=privkey,
                server_pubkey=server_public_key,
                host_id=host_id,
                psk=psk,
                persistent_keepalive=Config.wg_persistent_keepalive,
                wg_host=Config.wg_host,
                wg_port=Config.wg_port
            )
    return client_config

