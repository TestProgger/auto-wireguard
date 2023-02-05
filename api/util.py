import subprocess


def exec_command(args : list[str]) -> str :
    return subprocess.run(args , stdout=subprocess.PIPE).stdout.decode("utf-8").strip()

def get_server_keypair():
    privkey = exec_command(["cat" , "/etc/wireguard/privatekey"])
    pubkey = exec_command(["cat" , "/etc/wireguard/publickey"])
    return pubkey , privkey