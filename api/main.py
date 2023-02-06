from flask import Flask ,request , jsonify
from model import Client , db
import util
from peewee import fn
import wireguard
from config import Config


app = Flask(__name__)

SERVER_PUBLIC_KEY = None

def before_startup():
    global SERVER_PUBLIC_KEY
    print("# ------------> START UP")
    print(Config)
    pubkey , privkey = util.get_server_keypair()
    
    SERVER_PUBLIC_KEY = pubkey

@app.post('/add-client')
def addUser():
    data = request.get_json()
    client_id = data["client_id"]
    wg_name = data["wg_name"]

    try:
        prev_host_id = Client.select(fn.MAX(Client.host_id)).scalar()
        if prev_host_id is None:
            pubkey , privkey , psk = wireguard.generate_keypair_and_psk()
            return wireguard.create_client( client_id=client_id , wg_name=wg_name , host_id=1 , privkey=privkey , pubkey=pubkey, psk=psk, server_public_key=SERVER_PUBLIC_KEY  )

        elif prev_host_id == 253:
            return jsonify({ "error" : "Max client slots is reached" })
        else:
            pubkey , privkey , psk = wireguard.generate_keypair_and_psk()
            return wireguard.create_client( client_id=client_id , wg_name=wg_name , host_id=prev_host_id+1 , privkey=privkey , pubkey=pubkey, psk=psk, server_public_key=SERVER_PUBLIC_KEY  )
         
    except Exception as ex:
        print(ex)
        Client.get_or_create(client_id = 1 , host_id = 1)
    return jsonify(data)


if __name__ == "__main__":
    db.create_tables([Client , ])
    app.before_first_request(before_startup)
    app.run(host="127.0.0.1" , port=8000)