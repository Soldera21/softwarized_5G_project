$TTL    604800
@       IN      SOA     ns1.oai-ueransim.com. root.oai-ueransim.com. (
                  3       ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL
;
; name servers - NS records
     IN      NS      ns1.oai-ueransim.com.

; name servers - A records
ns1.oai-ueransim.com.          IN      A      192.168.70.160

; hosts - A records
mysql.oai-ueransim.com.       IN        A         192.168.70.131
nrf.oai-ueransim.com.       IN        A         192.168.70.130
udr.oai-ueransim.com.       IN        A         192.168.70.136
udm.oai-ueransim.com.       IN        A         192.168.70.137
ausf.oai-ueransim.com.       IN        A         192.168.70.138
amf.oai-ueransim.com.       IN        A         192.168.70.132
smf.oai-ueransim.com.       IN        A         192.168.70.133
vpp-upf.oai-ueransim.com.        IN        A         192.168.70.134
