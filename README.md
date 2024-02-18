# Softwarize and Virtualized Mobile Networks Project - Emulating 5G Core with OAI
#### Morandin Marco (228160) - Soldera Marco (226651)

The assignment is to reproduce [this](https://github.com/fabrizio-granelli/comnetsemu_5Gnet) architecture made with Open5GS with the dockerized version of OpenAirInterface 5G Core Network and Mininet to simulate latency and limited bandwidth of the links.

## Installation
Go to the root folder of the project and run:
```
./docker-pull.sh
```
Now every needed container is downloaded and ready to run the project.

## Run Docker Compose version
The version in docker compose is the one taken by the [official OAI repository](https://gitlab.eurecom.fr/oai/cn5g/oai-cn5g-fed) and is fully working with 3 slices and 3 UEs simulated by UERANSIM.
To try it, go to the ```docker-compose``` folder and run the following commands:
```
docker-compose -f docker-compose-slicing-basic.yaml up
```
When the previous command starts logging from the containers in another terminal run:
```
docker-compose -f docker-compose-ran-ueransim.yaml up
```

To test this configuration you can enter in the Ext-Dn container  and ping one of the UERANSIM User Equipemnts or vice versa with:
```
docker exec -it oai-ext-dn ping -c 4 [UE IP address]
```
or
```
docker exec -it ueransim[slice number] ping -c 4 -I uesimtun0 8.8.8.8
```
With ```docker logs [container name]``` you can check all the logs related to every network function.

#### Known Issues
- When a UPF-VPP is used the related SMF crashes
- Other RAN simulators give errors on startup

#### Shutdown Scenario
To stop the simulation press Ctrl-C and run the following commands in the respective terminals:
```
docker-compose -f docker-compose-slicing-basic.yaml down
docker-compose -f docker-compose-ran-ueransim.yaml down
```

## Run Mininet version (RAN not working)
The Mininet version is a basic configuration compared to the one in Docker Compose. All the scenarios are runned in comnetsemu.

abbiamo fatto conf di base per intanto provare che andasse e poi eventualmente espandere ma non ci siamo riusciti

- controllare latenze links
- test con ping, tcpdump su upf e iperf3

elencare indirizzi ip su entrambe le configurazioni

#### Known Issues
- upf-vpp
- no su arm
- solo ueransim e non va

#### Shutdown Scenario

