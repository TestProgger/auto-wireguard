import subprocess


def generate_keypair_and_psk():
    privkey = subprocess.call(["wg" , "genkey"] , stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    pubkey = subprocess.call(["echo" , privkey , '|' , 'wg' , 'pubkey']).stdout.decode("utf-8").strip()
    psk = subprocess.call(['wg' , 'genpsk']).stdout.decode("utf-8").strip()

    return {
        "pub" : pubkey,
        "priv" : privkey,
        'psk' : psk
    }

def generate_peer_record(client_id : int , pubkey : str , psk : str , host_id : str , host:str , port:int):
    peer_record =  f"## BEGIN PEER-{client_id}\n"
    peer_record += "[Peer]\n"
    peer_record += f"PublicKey = {pubkey}\n"
    peer_record += f"PresharedKey = {psk}\n"
    peer_record += f"AllowedIPs = 0.0.0.0/0, ::/0\n"
    peer_record += f"PersistentKeepalive = 0\n"
    peer_record += f"Endpoint = ${host}:${port}\n"
    peer_record += f"## END PEER-{client_id}\n\n"
