#!/bin/bash

docker pull ubuntu/bind9:latest
docker pull mysql:8.0
docker pull oaisoftwarealliance/oai-udr:v2.0.1
docker pull oaisoftwarealliance/oai-udm:v2.0.1
docker pull oaisoftwarealliance/oai-nssf:v2.0.1
docker pull oaisoftwarealliance/oai-ausf:v2.0.1
docker pull oaisoftwarealliance/oai-nrf:v2.0.1
docker pull oaisoftwarealliance/oai-amf:v2.0.1
docker pull oaisoftwarealliance/oai-smf:v2.0.1
docker pull oaisoftwarealliance/oai-upf:v2.0.1
docker pull oaisoftwarealliance/oai-upf-vpp:v2.0.1
docker pull oaisoftwarealliance/trf-gen-cn5g:latest
docker pull rohankharade/ueransim:latest
docker pull rfed/myueransim_v3-2-6

docker tag rfed/myueransim_v3-2-6 rfed/ueransim:v3.2.6
docker rmi rfed/myueransim_v3-2-6:latest
