# Project Setup Guide

This document describes the hardware, software, and network configuration used for this project. The system is built around a locally hosted MySQL server running on an Ubuntu server, connected through a network switch, and accessed via Ethernet and SSH.

---

## Table of Contents

- [Background](#background)
- [Overview](#overview)
- [Hardware](#hardware)
  - [Server](#server)
  - [Network Switch](#network-switch)
  - [Deployment Server (API Host)](#deployment-server-api-host)
  - [User/Developer Machine](#userdeveloper-machine)
- [Software](#software)
- [Documentation](#documentation)
  - [Netplan Configuration](#netplan-configuration)
  - [Local Reverse SSH Setup](#local-reverse-ssh-setup)
  - [Ensure MySQL Is Running](#ensure-mysql-is-running)
  - [Adding SSH Keys](#adding-ssh-keys)
  - [Verifying Sudo Privileges](#verifying-sudo-privileges)
  - [Connecting to Cisco Console](#connecting-to-cisco-console)
  - [Setting Up VLANs](#setting-up-vlans)
  - [Saving Switch Configurations](#saving-configurations-on-switch)
  - [Setting Up DHCP](#setting-up-dhcp)
  - [Other Switch Configurations](#other-switch-configirations)
  - [Recovering a Forgotten Switch Password](#recovering-a-forgotten-switch-password)

---
---

## Background

This project is motivated by the need to train machine learning algorithms on real life datasets of the stock market by using historical data. Having a dedicated database for training or testing machine learning algorithms will improve the efficiency of related projects

---
---

## Overview

This project uses a local MySQL server hosted on an Ubuntu server. The server is connected to a network switch, allowing communication with development and deployment machines over Ethernet and SSH. The deployment server hosts the live API and application, which interacts with the database.

---
---

## Hardware

All hardware used to deploy, host, and test the project.

---

### Server

The server hosts the MySQL database and handles all queries from the API and application.

- **Raspberry Pi (Model X)**
  - Version: X  
  - OS: Ubuntu Server (Release: X)

---

### Network Switch

The network switch is used to establish communication between all hardware components.

- **Cisco Catalyst (Model X)**

---

### Deployment Server (API Host)

The deployment server hosts the live application and API, which manages the database and handles all incoming API requests.

- **2017 MacBook Air**
    - OS: Ubuntu Desktop (Release: X) 

---

### User/Developer Machine

The user/developer machine is used for application development and for testing the system from an end-user perspective.

- **2020 MacBook Pro**

---
---

## Software

> _List all major software components here (e.g., MySQL version, Python, etc.)._

Example:
- MySQL Server X.X
- Ubuntu Server X.X
- API Framework
- DataGrip

---
---

## Documentation

Detailed setup and maintenance guides for the system.



### Netplan Configuration

Instructions for configuring network interfaces using Netplan.

---

### Local SSH Setup

Steps to configure a local SSH tunnel for remote access.

1. **Check mySQL is running using** `systemctl`
2. **Find IP address of server:**
    
    - In server console
    
        `$ ip -a`

    - If Wifi is **ON** set it to **DOWN**

        `$ sudo ip link dev wlan0 down`
    
3. **Connect Mac via ethernet to USB and ping server to test coneection**

    `$ ping 10.60.6.11`

4. **Once you can ping the server, create the ssh tunnel:**

    - Keep terminal open to keep connection

        `$ ssh -N -L 3307:localhost:3306 ubuntu@10.60.6.11`

        - `3307:locahost:3306` Creates a localhost on Mac forwarding part 3306 of the server to port 3307
        - `ubuntu@10.60.6.11` Is the user on the server and previous IP address found for the server
        - `-N` Flag for no remote code to executes
        - `-L` Flag for local part forwarding `[local_port]:[remote_host]:[remote_port] user@ssh_server`

5. **Open DataGrip and connect to database via localhost**

---

### Ensure MySQL Is Running

How to verify that the MySQL service is active and accepting connections.

&nbsp;&nbsp;&nbsp;&nbsp;**Check Status:**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`$ sudo systemctl status mysql`

&nbsp;&nbsp;&nbsp;&nbsp;**Start mySQL if not running:**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`$ sudo systemctl start mysql`

&nbsp;&nbsp;&nbsp;&nbsp;**Restart mySQL:**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`$ sudo systemctl restart mysql`

---

### Adding SSH Keys

Generating ssh key and storing public key on server using a usb.

1. **If you don't already have a ssh key, generate one:**

    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`$ ssh-keygen -t ed25519 -C "email@email.com"`

2. **Copy public key to USB:**

    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`$ cp ~/.ssh/id_ed25519.pub /Volumes/"UsbName"`

3. **Transfer USB to server and locate in dir:**

    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`$ lsblk`

4. **Mount USB:**

    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`$ sudo mount /dev/sdX1 /mnt/usb`

5. **Copy ssh key to authorized keys:**

    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`$ cat /mnt/usb/id_ed25519.pub >> /user/.ssh/authorized_keys`

6. **Unmount USB from server:**

    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`$ sudo umount /mnt/usb`

---

### Verifying Sudo Privileges

How to confirm that a user has appropriate sudo permissions.

&nbsp;&nbsp;&nbsp;&nbsp;`$ sudo -I`

---

### DataGrip configuration

1. **Open DataGrip and click data source and choose mySQL**

2. **Right click on db and click properties**

3. **Ensure proper configuration below:**

        Name: 'db_name'@127.0.0.1

        Host: 127.0.0.1

        Port: 3307

        User: "user created on mySQL"

        Password: "password created for mySQL user"

        Database: "db_name"

---

### Connecting to Cisco Console

Instructions for connecting to the Cisco switch via console cable.

1. **Plug in console cable to the back of the switch**

2. **Find USB that plugged in (may need to do this step while unplugged and plugged to identify):**

        ls /dev/tty.usb*

3. **Remote into switch using screen:**

        screen /dev/tty.usbxxxxxxx 

---

### Setting Up VLANs

Guide for creating and configuring VLANs on the switch once have access to console.

**Show all vlans**

    show vlan

**Create a new vlan**

1. **Enter into root (command prompt will change to `#`):**

        en

2. **Go into config mode(command prompt will change to `config#`):**

        conf t

3. **Create vlan(command prompt will change to `vlan-config#`):**

        vlan <number>

4. **Name vlan:**

        name "name-of-vlan"

5. **Use exit to get out of command prompt and back to `#`**

**Assigning port to vlan**

1. **Go into config mode(command prompt will change to `config#`):**

        conf t

2. **Example assigning port 1(command prompt will change to `config-if#`):**

        interface fastEthernet 0/1

3. **Go into access mode:**

        switchport mode access

4. **Assign port to vlan:**

        switchport access vlan <number>

5. **Exit to `#` command prompt and verify change by using `show vlan`**

**Assigning mulitple port ranges**

1. **In `config#`, example assigning port 2 to 12:**

        interface range fastEthernet 0/2-12

2. **Repeat steps from assigning port to vlan starting at step 3 to 5**

**Assigning ip address to vlan**

1. **In `config#`, enter into vlan interface(command prompt will change to `config-if#`):**

        interface vlan <number>

2. **Set ip address:**

        ip address 10.60.6.1 255.255.255.0

    * Creates usable hosts 10.60.6.1 - 10.60.6.254
    * The ip for the vlan which is 10.60.6.1 will become a gateway for other devices

3. **Exit to `#` command prompt and verify changes:**

        show ip interface brief

---

### Saving Configurations on Switch

If you do not save your configuration after doing any modifications it will not be saved if the switch gets restarted.

**Save configuration**

1. **Enter into root (command prompt will change to `#`):**

        en

2. **Save configuratoin:**

        copy running-config startup-config

3. **Reload switch (restart):**

        reload

---

### Setting Up DHCP

Configurating for DHCP services on the switch

**Help command (in `config#` command prompt)**

    ip dhcp ?

**Configure DHCP for vlan**

1. **Start in `config#` command prompt and select vlan to configure(command prompt will change to `dhcp-config#`):**

        ip dhcp pool <vlan-number>

2. **Configure which subnet it is responsible for:**

        network 10.60.6.0 /24

    * 10.60.6.0 = network address
    * /24 = subnet mask 255.255.255.0
    * network range is 10.60.6.0 - 10.60.6.255

3. **Set default router:**

        default-router 10.60.6.1

**Excluding ip addresses for static devices**

1. **Exclude a range of ip addresses(in `config#` command prompt):**

        ip dhcp excluded-address <low-ip> <high-ip>

    * low-ip can be 10.60.6.5
    * high-ip can be 10.60.6.10

2. **Verify ip addresses have been excluded(in `#` command prompt):**

        show running-config | include ip dhcp excluded-address

---

### Other Switch Configirations

**Change hostname**

1. **Enter into `config#` command prompt**

2. **Change hostname:**

        hostname <name>

**Enable password**

1. **Enter into `config#` command prompt**

2. **Enable password:**

        enable password <password>

**Setting a banner**

1. **Enter into `config#` command prompt**

2. **Set banner:**

        banner <type> <delimiter>

    * type:
        
        * motd - message of the day (shows on connection)
        * login - login banner (shows at login prompt)
        * exec - exec banner (shows after login)
        * incoming - incoming banner (shows on reverse connections)

    * delimiter = any character used for ending banner input text

---

### Recovering a Forgotten Switch Password

Procedure for resetting or recovering access to the Cisco switch.

Source link: https://www.youtube.com/watch?v=00xzIVGEtWY

1. **Have the terminal open for the switch console and unplug the power cable on the switch and plug it back in while holding the mode button when it is rebooting until you see a page boot up saying it is in password recovery mode**

2. **Type command `flash_init`**

3. **Type command `load_helper`**

4. **Type `dir flash:` to locate config file**

5. **Rename startuo config to login without a password:**

        rename flash:config.text flash:config.text.old

6. **Type command `boot`**

7. **When done loading enter into switch and say no to all inital configuration setup**

8. **Enter into root by typing `en`**

9. **Rename startup config back to original:**

        rename flash:config.text.old flash:config.text

10. **Copy startup config to running config:**

        copy flash:config.text system:running-config

11. **Optional step to set a password to switch (see Other Switch Configurations section)**

12. **If set a password ensure to save changes:**

        wr

    * writes to memory

13. **Test to ensure all steps done correctly completely `exit` until you get to return screen and try logging in**


