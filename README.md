# OpenWRT WiFi Switch for Home Assistant

Switch your WiFi on and off using Home Assistant.

This fork adds key-pair auth and pseudo-commands to enchance security for root access to OpenWRT.

### Setup

## HAOS


https://lazyadmin.nl/smart-home/enable-ssh-home-assistant/


Enable Advanced Mode:  
Your profile → General tab → Advanced Mode: enable

Install `Terminal & SSH` Add-On:  
Add-On Store → Search: "SSH" → `Terminal & SSH` → Install  
Watchdog: enable  
Start

In the terminal:

Generate public/private key pair (no passphrase):  
`ssh-keygen -t ed25519 -C "openwrt-key" -f ~/.ssh/openwrt-key`

Copy contents of public key:  
`cat ~/.ssh/openwrt-key.pub`



Add-on: File editor




In the terminal create folder for custom_components:  
`mkdir ~/config/custom_components`

Go to folder and clone this repo:  
```
cd ~/config/custom_components

```

Execute `git clone https://github.com/kludda/homeassistant-openwrt-wifi-switch.git`


Add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
openwrt_wifi_switch:
- ifname: "<wifi-interface-ifname>"
  host: "<ssh-host>"
  key_filename: "<path-to-private-key-file>"
  port: "<ssh-port>"
```

```yaml
# Example configuration.yaml entry
openwrt_wifi_switch:
- ifname: "wifinet3"
  host: "192.168.1.1"
  port: "22"
  key_filename: !secret openwrt-key

```
  key_filename: "/config/.ssh/openwrt-key"



### OpenWRT

Add user for homeassistant  
`echo "homeassistant:!:9999:0::/home/root:/bin/false" >> /etc/passwd`

`echo "homeassistant:!:9999:9999::/home/homeassistant:/bin/ash" >> /etc/passwd`
`echo "homeassistant:x:9999:" >> /etc/group`

root:x:0:homeassistant

mkdir -p /home/homeassistant/.ssh
`touch ~/home/homeassistant/.ssh/authorized_keys`

chmod -R homeassistant:homeassistant /home/homeassistant


Creata a whitelist script  
`vi ~/ha-commands.sh`

Paste contents of
[ha-commands.sh](./ha-commands.sh)

Make it executable  
`chmod +x ~/ha-commands.sh`

Create ssh folder if it does not exist  
`mkdir ~/.ssh`

Create `authorized_keys` file if it does not exist  
`touch ~/.ssh/authorized_keys`

Bind SSH key
`vi ~/.ssh/authorized_keys`

Enter the following, replace <key> with contents of `~/.ssh/openwrt-key.pub` in HAOS:
`command="~/ha-commands.sh",no-port-forwarding,no-X11-forwarding,no-agent-forwarding <key>`
(hold shift and drag with mouse to copy text in web terminal in home assistant.



ssh -o PasswordAuthentication=no  -i /root/.ssh/openwrt-key homeassistant@192.168.1.1 wifi-down wifinet3
ssh -o 'IdentitiesOnly=yes' -i /root/.ssh/openwrt-key homeassistant@192.168.1.1 'wifi-down wifinet3'