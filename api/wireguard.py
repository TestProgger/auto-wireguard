import subprocess
import util

def generate_keypair_and_psk():
    privkey = util.exec_command(["wg" , "genkey"])
    pubkey = util.exec_command(["echo" , privkey , '|' , 'wg' , 'pubkey'])
    psk = util.exec_command(['wg' , 'genpsk'])

    return pubkey , privkey, psk

def generate_peer_record(client_id : int , pubkey : str , psk : str ):
    peer_record =  f"## BEGIN PEER-{client_id}\n"
    peer_record += "[Peer]\n"
    peer_record += f"PublicKey = {pubkey}\n"
    peer_record += f"PresharedKey = {psk}\n"
    peer_record += f"AllowedIPs = 0.0.0.0/0, ::/0\n"
    peer_record += f"## END PEER-{client_id}\n\n\n"

    return peer_record

def write_peer_record( client_id : int , pubkey : str , psk : str ):
    with open('/etc/wireguard/wg0.conf' , "rw" , encoding="utf-8") as wg_file:
        wg_file.write(generate_peer_record(client_id , pubkey , psk))
    

def generate_client_config( * , 
                            dns : str = "1.1.1.1" , 
                            privkey : str ,  
                            server_pubkey : str,
                            host_id : str,
                            psk : str,
                            persistent_keepalive = 0,
                            wg_host : str,
                            wg_port : int
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
    client_config +=  "AllowedIPs = 0.0.0.0/0, ::/0"
    client_config += f"PersistentKeepalive = {persistent_keepalive}"
    client_config += f"Endpoint = {wg_host}:{wg_port}"

    return client_config