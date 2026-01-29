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
  - [Setting Up DHCP](#setting-up-dhcp)
  - [Recovering a Forgotten Switch Password](#recovering-a-forgotten-switch-password)

---

## Background

This project is motivated by the need to train machine learning algorithms on real life datasets of the stock market by using historical data. Having a dedicated database for training or testing machine learning algorithms will improve the efficiency of related projects

---

## Overview

This project uses a local MySQL server hosted on an Ubuntu server. The server is connected to a network switch, allowing communication with development and deployment machines over Ethernet and SSH. The deployment server hosts the live API and application, which interacts with the database.

---

## Hardware

All hardware used to deploy, host, and test the project.

### Server

The server hosts the MySQL database and handles all queries from the API and application.

- **Raspberry Pi (Model X)**
  - Version: X  
  - OS: Ubuntu Server (Release: X)

### Network Switch

The network switch is used to establish communication between all hardware components.

- **Cisco Catalyst (Model X)**

### Deployment Server (API Host)

The deployment server hosts the live application and API, which manages the database and handles all incoming API requests.

- **2017 MacBook Air**
    - OS: Ubuntu Desktop (Release: X) 

### User/Developer Machine

The user/developer machine is used for application development and for testing the system from an end-user perspective.

- **2020 MacBook Pro**

---

## Software

> _List all major software components here (e.g., MySQL version, Python, etc.)._

Example:
- MySQL Server X.X
- Ubuntu Server X.X
- API Framework

---

## Documentation

Detailed setup and maintenance guides for the system.

### Netplan Configuration

Instructions for configuring network interfaces using Netplan.

### Local Reverse SSH Setup

Steps to configure a local reverse SSH tunnel for remote access.

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

How to generate and add SSH keys for secure authentication.

### Verifying Sudo Privileges

How to confirm that a user has appropriate sudo permissions.

&nbsp;&nbsp;&nbsp;&nbsp;`$ sudo -I`

---

### Connecting to Cisco Console

Instructions for connecting to the Cisco switch via console cable.

### Setting Up VLANs

Guide for creating and configuring VLANs on the switch.

### Setting Up DHCP

Instructions for configuring DHCP services for the network.

### Recovering a Forgotten Switch Password

Procedure for resetting or recovering access to the Cisco switch.

---
