import os
import docker
import time
import traceback

from comnetsemu.cli import CLI
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink, Intf
from mininet.log import info, setLogLevel
from mininet.node import Controller

AUTOTEST_MODE = os.environ.get("COMNETSEMU_AUTOTEST_MODE", 0)

setLogLevel("info")

client = docker.from_env()
containers = client.containers

prj_folder = os.getcwd()
wait_timeout = 150

net = Containernet(controller=Controller, link=TCLink)
mgr = VNFManager(net)


def stop_network():
    try: 
        mgr.removeContainer("dns_srv")
        mgr.removeContainer("mysql_srv")
        mgr.removeContainer("nssf_srv")
        mgr.removeContainer("udr_srv")
        mgr.removeContainer("udm_srv")
        mgr.removeContainer("ausf_srv")
        mgr.removeContainer("nrf_srv")
        mgr.removeContainer("amf_srv")
        mgr.removeContainer("smf_srv")
        mgr.removeContainer("upf_srv")
        mgr.removeContainer("ext_dn_srv")
        mgr.removeContainer("gnb_srv")
        mgr.removeContainer("ue_srv")
    except ValueError:
        pass

    net.stop()
    mgr.stop()


try:
    info("*** Adding controller\n")
    net.addController("c0")

    info("*** Adding switches\n")
    s1 = net.addSwitch("s1")

    info("*** Adding dev_tests\n")

    dns = net.addDockerHost(
        "dns",
        dimage="dev_test",
        docker_args={
            "hostname" : "dns",
        }
    )
    net.addLink(dns, s1, bw=1000, delay="1ms", intfName1="dns-s3", intfName2="s3-dns", params1={'ip': '192.168.70.160/24'})

    mysql = net.addDockerHost(
        "mysql",
        dimage="dev_test",
        docker_args={
            "hostname" : "mysql",
            "dns": ["192.168.70.160"],
        }
    )
    net.addLink(mysql, s1, bw=1000, delay="1ms", intfName1="mysql-s1", intfName2="s1-mysql", params1={'ip': '192.168.70.131/24'})

    nssf = net.addDockerHost(
        "nssf",
        dimage="dev_test",
        docker_args={
            "hostname" : "nssf",
            "dns": ["192.168.70.160"],
        },
        expose= {
            "80/tcp",
            "8080/tcp",
        }
    )
    net.addLink(nssf, s1, bw=1000, delay="1ms", intfName1="nssf-s1", intfName2="s1-nssf", params1={'ip': '192.168.70.134/24'})

    udr = net.addDockerHost(
        "udr",
        dimage="dev_test",
        docker_args={
            "hostname" : "udr",
            "dns": ["192.168.70.160"],
        },
        expose= {
            "80/tcp",
            "8080/tcp",
        }
    )
    net.addLink(udr, s1, bw=1000, delay="1ms", intfName1="udr-s1", intfName2="s1-udr", params1={'ip': '192.168.70.136/24'})

    udm = net.addDockerHost(
        "udm",
        dimage="dev_test",
        docker_args={
            "hostname" : "udm",
            "dns": ["192.168.70.160"],
        },
        expose= {
            "80/tcp",
            "8080/tcp",
        }
    )
    net.addLink(udm, s1, bw=1000, delay="1ms", intfName1="udm-s1", intfName2="s1-udm", params1={'ip': '192.168.70.137/24'})
    
    ausf = net.addDockerHost(
        "ausf",
        dimage="dev_test",
        docker_args={
            "hostname" : "ausf",
            "dns": ["192.168.70.160"],
        },
        expose= {
            "80/tcp",
            "8080/tcp",
        }
    )
    net.addLink(ausf, s1, bw=1000, delay="1ms", intfName1="ausf-s1", intfName2="s1-ausf", params1={'ip': '192.168.70.138/24'})

    nrf = net.addDockerHost(
        "nrf",
        dimage="dev_test",
        docker_args={
            "hostname" : "nrf",
            "dns": ["192.168.70.160"],
        },
        expose= {
            "80/tcp",
            "8080/tcp",
        }
    )
    net.addLink(nrf, s1, bw=1000, delay="1ms", intfName1="nrf-s1", intfName2="s1-nrf", params1={'ip': '192.168.70.130/24'})

    amf = net.addDockerHost(
        "amf",
        dimage="dev_test",
        docker_args={
            "hostname" : "amf",
            "dns": ["192.168.70.160"],
        },
        expose= {
            "80/tcp",
            "8080/tcp",
            "38412/sctp",
        }
    )
    net.addLink(amf, s1, bw=1000, delay="1ms", intfName1="amf-s1", intfName2="s1-amf", params1={'ip': '192.168.70.132/24'})

    smf = net.addDockerHost(
        "smf",
        dimage="dev_test",
        docker_args={
            "hostname" : "smf",
            "dns": ["192.168.70.160"],
        },
        expose= {
            "80/tcp",
            "8080/tcp",
            "8805/udp",
        }
    )
    net.addLink(smf, s1, bw=1000, delay="1ms", intfName1="smf-s1", intfName2="s1-smf", params1={'ip': '192.168.70.133/24'})

    upf = net.addDockerHost(
        "upf",
        dimage="dev_test",
        docker_args={
            "hostname" : "upf",
            "dns": ["192.168.70.160"],
        },
        expose= {
            "2152/udp",
            "8805/udp",
        }
    )
    net.addLink(upf, s1, bw=1000, delay="1ms", intfName1="upf-s1", intfName2="s1-upf", params1={'ip': '192.168.70.134/24'})

    ext_dn = net.addDockerHost(
        "ext_dn",
        dimage="dev_test",
        docker_args={
            "hostname" : "ext_dn",
            "dns": ["192.168.70.160"],
        }
    )
    net.addLink(ext_dn, s1, bw=1000, delay="50ms", intfName1="ext_dn-s1", intfName2="s1-ext_dn", params1={'ip': '192.168.70.150/24'})
    net.addLink(upf, ext_dn, bw=1000, delay="1ms", intfName1="upf-ext_dn", intfName2="ext_dn-upf", params1={'ip': '192.168.73.144/24'}, params2={'ip': '192.168.73.145/24'})

    gnb = net.addDockerHost(
        "gnb",
        dimage="dev_test",
        docker_args={
            "hostname" : "gnb",
            "dns": ["192.168.70.160"],
        }
    )
    net.addLink(gnb, s1, bw=1000, delay="1ms", intfName1="gnb-s1", intfName2="s1-gnb", params1={'ip': '192.168.70.156/24'})
    net.addLink(upf, gnb, bw=1000, delay="1ms", params1={'ip': '192.168.72.144/24'}, params2={'ip': '192.168.72.141/24'})

    ue = net.addDockerHost(
        "ue",
        dimage="dev_test",
        docker_args={
            "hostname" : "ue",
            "dns": ["192.168.70.160"],
        }
    )
    net.addLink(ue, s1, bw=1000, delay="1ms", intfName1="ue-s1", intfName2="s1-ue", params1={'ip': '192.168.70.157/24'})

    net.start()

    info("*** Adding DNS container\n")
    dns_srv = mgr.addContainer(
        name = "dns_srv",
        dhost = "dns",
        dimage = "ubuntu/bind9:latest",
        dcmd = "",
        docker_args={
            "environment": {
                "TZ": "Europe/Paris",
                "BIND9_USER": "root",
            },
            "volumes": {
                prj_folder + "/dns/": {
                    "bind": "/etc/bind/",
                    "mode": "rw",
                },
            },
            "privileged": True,
            "restart_policy": { "Name": "always", },
        }
    )

    info("*** Adding mysql container\n")
    mysql_srv = mgr.addContainer(
        name = "mysql_srv",
        dhost = "mysql",
        dimage = "mysql:8.0",
        dcmd = "",
        docker_args={
            "volumes": {
                prj_folder + "/database/oai_db.sql": {
                    "bind": "/docker-entrypoint-initdb.d/oai_db.sql",
                    "mode": "rw",
                },
                prj_folder + "/healthscripts/mysql-healthcheck.sh": {
                    "bind": "/tmp/mysql-healthcheck.sh",
                    "mode": "rw",
                },
            },
            "environment": {
                "TZ": "Europe/Paris",
                "MYSQL_DATABASE": "oai_db",
                "MYSQL_USER": "test",
                "MYSQL_PASSWORD": "test",
                "MYSQL_ROOT_PASSWORD": "linux",
            },
            "healthcheck": {
                "test": "/bin/bash -c \"/tmp/mysql-healthcheck.sh\"",
                "interval": 10000000000,
                "timeout": 5000000000,
                "retries": 30,
            },
        }
    )

    elapsed = 0
    info("Waiting for mysql to be up and healthy")
    while client.containers.get("mysql_srv").attrs["State"]["Health"]["Status"] != "healthy":
        time.sleep(0.5)
        info(".")
        elapsed += 1
        if elapsed >= wait_timeout:
            info("\n")
            mgr.removeContainer("dns_srv")
            mgr.removeContainer("mysql_srv")
            net.stop()
            mgr.stop()
            info("Error: timeout reached. Exiting\n")
            exit()
    info("\n")

    info("*** Adding NSSF container\n")
    nssf_srv = mgr.addContainer(
        name = "nssf_srv",
        dhost = "nssf",
        dimage = "oaisoftwarealliance/oai-nssf:v2.0.1",
        dcmd = "",
        docker_args={
            "volumes": {
                prj_folder + "/conf/oai_net_config.yaml": {
                    "bind": "/openair-nssf/etc/config.yaml",
                    "mode": "rw",
                },
                prj_folder + "/conf/nssf_slice_config.yaml": {
                    "bind": "/openair-nssf/etc/nssf_slice_config.yaml",
                    "mode": "rw",
                },
            },
            "environment": {
                "TZ": "Europe/Paris",
            },
            "cap_add": ["NET_ADMIN", "SYS_ADMIN"],
            "cap_drop": ["ALL"],
        }
    )

    info("*** Adding UDR container\n")
    udr_srv = mgr.addContainer(
        name = "udr_srv",
        dhost = "udr",
        dimage = "oaisoftwarealliance/oai-udr:v2.0.1",
        dcmd = "",
        docker_args={
            "volumes": {
                prj_folder + "/conf/oai_net_config.yaml": {
                    "bind": "/openair-udr/etc/config.yaml",
                    "mode": "rw",
                },
            },
            "environment": {
                "TZ": "Europe/Paris",
            },
        }
    )

    info("*** Adding UDM container\n")
    udm_srv = mgr.addContainer(
        name = "udm_srv",
        dhost = "udm",
        dimage = "oaisoftwarealliance/oai-udm:v2.0.1",
        dcmd = "",
        docker_args={
            "volumes": {
                prj_folder + "/conf/oai_net_config.yaml": {
                    "bind": "/openair-udm/etc/config.yaml",
                    "mode": "rw",
                },
            },
            "environment": {
                "TZ": "Europe/Paris",
            },
        }
    )

    info("*** Adding AUSF container\n")
    ausf_srv = mgr.addContainer(
        name = "ausf_srv",
        dhost = "ausf",
        dimage = "oaisoftwarealliance/oai-ausf:v2.0.1",
        dcmd = "",
        docker_args={
            "volumes": {
                prj_folder + "/conf/oai_net_config.yaml": {
                    "bind": "/openair-ausf/etc/config.yaml",
                    "mode": "rw",
                },
            },
            "environment": {
                "TZ": "Europe/Paris",
            },
        }
    )

    info("*** Adding NRF container\n")
    nrf_srv = mgr.addContainer(
        name = "nrf_srv",
        dhost = "nrf",
        dimage = "oaisoftwarealliance/oai-nrf:v2.0.1",
        dcmd = "",
        docker_args={
            "volumes": {
                prj_folder + "/conf/oai_net_config.yaml": {
                    "bind": "/openair-nrf/etc/config.yaml",
                    "mode": "rw",
                },
            },
            "environment": {
                "TZ": "Europe/Paris",
            },
        }
    )

    info("*** Adding AMF container\n")
    amf_srv = mgr.addContainer(
        name = "amf_srv",
        dhost = "amf",
        dimage = "oaisoftwarealliance/oai-amf:v2.0.1",
        dcmd = "",
        docker_args={
            "volumes": {
                prj_folder + "/conf/oai_net_config.yaml": {
                    "bind": "/openair-amf/etc/config.yaml",
                    "mode": "rw",
                },
            },
            "environment": {
                "TZ": "Europe/Paris",
            },
        }
    )

    info("*** Adding SMF container\n")
    smf_srv = mgr.addContainer(
        name = "smf_srv",
        dhost = "smf",
        dimage = "oaisoftwarealliance/oai-smf:v2.0.1",
        dcmd = "",
        docker_args={
            "volumes": {
                prj_folder + "/conf/oai_net_config.yaml": {
                    "bind": "/openair-smf/etc/config.yaml",
                    "mode": "rw",
                },
            },
            "environment": {
                "TZ": "Europe/Paris",
            },
        }
    )

    info("*** Adding UPF-VPP container\n")
    upf_srv = mgr.addContainer(
        name="upf_srv",
        dhost = "upf",
        dimage="oaisoftwarealliance/oai-upf-vpp:v2.0.1",
        dcmd = "",
        docker_args={
            "environment": {
                "IF_1_IP": "192.168.70.134",
                "IF_1_TYPE": "N4",
                "IF_1_IP_REMOTE": "192.168.70.133", # SMF IP Address
                "IF_2_IP": "192.168.72.144",
                "IF_2_TYPE": "N3",
                "IF_2_NWI": "access.oai.org",
                "IF_3_IP": "192.168.73.144",
                "IF_3_TYPE": "N6",
                "IF_3_IP_REMOTE": "192.168.73.145", # EXT-DN IP Address
                "IF_3_NWI": "internet.oai.org",
                "NAME": "upf_srv",
                "MNC": "95",
                "MCC": "208",
                # "REALM": "3gppnetwork.org",
                "REALM": "oai-ueransim.com",
                "VPP_MAIN_CORE": "0",
                "VPP_CORE_WORKER": "1",
                "VPP_PLUGIN_PATH": "/usr/lib/x86_64-linux-gnu/vpp_plugins/", # Ubntu18.04
                "SNSSAI_SD": "123",
                "SNSSAI_SST": "222",
                "DNN": "default",
                "REGISTER_NRF": "yes",
                "NRF_IP_ADDR": "192.168.70.130",
                "NRF_FQDN": "nrf.oai-ueransim.com",
                "USE_FQDN_DNS": "yes",
                # changes for HTTP2
                "NRF_PORT": "8080",
                "HTTP_VERSION": "2",
            },
            "healthcheck": {
                "test": "/bin/bash -c \"pgrep vpp\"",
                "interval": 10000000000,
                "timeout": 5000000000,
                "retries": 5,
            },
            "privileged": True,
            "cap_add": ["NET_ADMIN", "SYS_ADMIN"],
            "cap_drop": ["ALL"],
        }
    )

    info("*** Adding EXT-DN container\n")
    ext_dn_srv = mgr.addContainer(
        name = "ext_dn_srv",
        dhost = "ext_dn",
        dimage = "oaisoftwarealliance/trf-gen-cn5g:latest",
        dcmd = "",
        docker_args={
            "entrypoint": "/bin/bash -c \"iptables -t nat -A POSTROUTING -o ext_dn-upf -j MASQUERADE; ip route add 12.1.1.0/26 via 192.168.73.144 dev ext_dn-upf; ip route; sleep infinity\"",
            "command": ["/bin/bash", "-c", "trap : SIGTERM SIGINT; sleep infinity & wait"],
            "healthcheck": {
                "test": "/bin/bash -c \"iptables -L -t nat | grep MASQUERADE\"",
                "interval": 10000000000,
                "timeout": 5000000000,
                "retries": 10,
            },
            "privileged": True,
        }
    )

    time.sleep(5)

    info("*** Adding ueransim-gNb container\n")
    gnb_srv = mgr.addContainer(
        name = "gnb_srv",
        dhost = "gnb",
        dimage = "rfed/ueransim:v3.2.6",
        dcmd = "bash /mnt/ueransim/open5gs_gnb_init.sh",
        docker_args={
            "privileged" : True,
            "volumes": {
                prj_folder + "/ueransim/config": {
                    "bind": "/mnt/ueransim",
                    "mode": "rw",
                },
                prj_folder + "/log": {
                    "bind": "/mnt/log",
                    "mode": "rw",
                },
                "/dev": {"bind": "/dev", "mode": "rw"},
            },
            "cap_add": ["NET_ADMIN"],
        },
    )

    info("*** Adding ueransim-UE container\n")
    ue_srv = mgr.addContainer(
        name = "ue_srv",
        dhost = "ue",
        dimage = "rfed/ueransim:v3.2.6",
        dcmd = "bash /mnt/ueransim/open5gs_ue_init.sh",
        docker_args={
            "privileged" : True,
            "volumes": {
                prj_folder + "/ueransim/config": {
                    "bind": "/mnt/ueransim",
                    "mode": "rw",
                },
                prj_folder + "/log": {
                    "bind": "/mnt/log",
                    "mode": "rw",
                },
                "/dev": {"bind": "/dev", "mode": "rw"},
            },
            "cap_add": ["NET_ADMIN"],
        },
    )

    if not AUTOTEST_MODE:
        CLI(net)

    stop_network()
except Exception:
    traceback.print_exc() 
    stop_network()
except KeyboardInterrupt:
    stop_network()