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
    pubkey , privkey = util.get_server_keypair()
    SERVER_PUBLIC_KEY = pubkey

@app.post('/create-client')
def create_client():
    data = request.get_json()

    try:
        client_id = data["client_id"]
        wg_name = data["wg_name"]
        prev_host_id = Client.select(fn.MAX(Client.host_id)).scalar()
        if prev_host_id is None:
            pubkey , privkey , psk = wireguard.generate_keypair_and_psk()
            return wireguard.create_client( client_id=client_id , wg_name=wg_name , host_id=2 , privkey=privkey , pubkey=pubkey, psk=psk, server_public_key=SERVER_PUBLIC_KEY  )

        elif prev_host_id == 253:
            return jsonify({ "error" : "Max client slots is reached" })
        else:
            pubkey , privkey , psk = wireguard.generate_keypair_and_psk()
            return wireguard.create_client( client_id=client_id , wg_name=wg_name , host_id=prev_host_id+1 , privkey=privkey , pubkey=pubkey, psk=psk, server_public_key=SERVER_PUBLIC_KEY  )
         
    except Exception as ex:
        app.logger.error(str(ex))
        return jsonify({"error" : str(ex)})

@app.delete('/delete-client')
def delete_client():
    data = request.get_json()
    try:
        record_id = data["record_id"]
        client_id = data["client_id"]
        rows_affected = Client.delete().where( Client.id == record_id , Client.client_id == client_id ).execute()
        wireguard.delete_peer_record(record_id)
        return jsonify({ "record_id" : record_id , "rows_affected" : rows_affected})
    except Exception as ex:
        app.logger.error(str(ex))
        return jsonify({ "error" : str(ex) })

@app.get("/get-all-clients")
def get_all_clients():
    try:
        clients = Client.select(Client.id , Client.client_id , Client.host_id , Client.created_at).dicts()
        print(clients)
        return jsonify(list(clients))
    except Exception as ex:
        return jsonify({ "error" : str(ex) })

        
if __name__ == "__main__":
    db.create_tables([Client , ])
    util.exec_command(['wg-quick' , 'up' , 'wg0'])
    app.before_first_request(before_startup)
    app.run(host="0.0.0.0" , port=Config.api_port)