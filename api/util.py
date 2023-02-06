import subprocess


def exec_command(args : list[str] , _input : str = None) -> str :
    if _input is None:
        return subprocess.run(args , stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
    else:
        return subprocess.run(args , stdout=subprocess.PIPE , input=_input).stdout.decode("utf-8").strip()

def get_server_keypair():
    privkey = exec_command(["cat" , "/etc/wireguard/privatekey"])
    pubkey = exec_command(["cat" , "/etc/wireguard/publickey"])
    return pubkey , privkey