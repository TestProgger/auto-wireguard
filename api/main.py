from flask import Flask ,request , jsonify
from model import Client , db
import util
from peewee import fn
import wireguard
app = Flask(__name__)

SERVER_PUBLIC_KEY = None

def before_startup():
    global SERVER_PUBLIC_KEY
    print("# ------------> START UP")
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
            Client.create(  
                            client_id=client_id , 
                            name=wg_name ,  
                            host_id=1 ,  
                            public_key = pubkey,
                            private_key = privkey,
                            pre_shared_key = psk
                        )

        elif prev_host_id == 253:
            return jsonify({ "error" : "Max client slots is reached" })
        else:
            Client.create( client_id=client_id , host_id=prev_host_id+1 )
         
    except:
        Client.get_or_create(client_id = 1 , host_id = 1)
    return jsonify(data)


if __name__ == "__main__":
    db.create_tables([Client , ])
    app.before_first_request(before_startup)
    app.run(host="127.0.0.1" , port=8000)