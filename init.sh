#!/usr/bin/bash

export WG_PRIV_KEY=$(wg genkey)
export WG_PUB_KEY=$(echo "$WG_PRIV_KEY" | wg pubkey)
export WG_DEST_PORT=30000

echo '[Interface]' >> /etc/wireguard/wg0.conf 
echo "PrivateKey = $WG_PRIV_KEY" >> /etc/wireguard/wg0.conf 
echo "ListenPort = $WG_DEST_PORT"  >> /etc/wireguard/wg0.conf 
echo "Address = 10.0.8.1"  >> /etc/wireguard/wg0.conf 
echo "PostUp = iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE; iptables -A INPUT -p udp -m udp --dport $WG_DEST_PORT -j ACCEPT; iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT;" >> /etc/wireguard/wg0.conf 

# echo '[Interface]' 
# echo "PrivateKey = $WG_PRIV_KEY" 
# echo "ListenPort = $WG_DEST_PORT"  
# echo "Address = 10.0.8.1"  
# echo "PostUp = iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE; iptables -A INPUT -p udp -m udp --dport $WG_DEST_PORT -j ACCEPT; iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT;"  


wg-quick up wg0
