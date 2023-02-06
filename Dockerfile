FROM python:3.11-alpine

# PREPARING FOR INSTALLATION
RUN apk update && apk upgrade

# INSTALLING WIREGUARD
RUN apk add wireguard-tools
RUN apk add dumb-init

ENV WG_DEST_PORT 30000

# Creation wg config
RUN wg genkey > /etc/wireguard/privatekey
RUN cat /etc/wireguard/privatekey | wg pubkey > /etc/wireguard/publickey
RUN echo '[Interface]' >> /etc/wireguard/wg0.conf 
RUN echo "PrivateKey = $(cat /etc/wireguard/privatekey)" >> /etc/wireguard/wg0.conf 
RUN echo "ListenPort = $WG_DEST_PORT"  >> /etc/wireguard/wg0.conf 
RUN echo "Address = 10.0.8.1"  >> /etc/wireguard/wg0.conf 
RUN echo "PostUp = iptables -t nat -A POSTROUTING -s 10.0.8.0/24 -o eth0 -j MASQUERADE; iptables -A INPUT -p udp -m udp --dport $WG_DEST_PORT -j ACCEPT; iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT;" >> /etc/wireguard/wg0.conf 
RUN echo "" >> /etc/wireguard/wg0.conf

WORKDIR /app
COPY ./api .
COPY .env .

RUN pip install -r requirements.txt

ENTRYPOINT [ "/usr/bin/dumb-init" , "python" , "main.py" ]
# ENTRYPOINT [ "tail" , "-f" , "/dev/null" ]


