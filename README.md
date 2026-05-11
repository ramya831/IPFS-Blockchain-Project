# IPFS-Based Secure File Storage and Access Control 🔐

A decentralized data management system that leverages **Blockchain** for immutable access control and **IPFS** for secure, distributed storage.

## 🚀 Overview
This project solves the "Single Point of Failure" problem in traditional storage by using decentralized technologies. It allows users to upload files to IPFS and manage viewing permissions through Ethereum smart contracts (via Ganache).

## 🛠️ Tech Stack
* **Framework:** Django (Python)
* **Blockchain:** Ganache / Solidity
* **Storage:** IPFS (InterPlanetary File System)
* **Web3 Library:** Web3.py
* **Frontend:** HTML5, CSS3, JavaScript

## ✨ Key Features
- **Immutable Storage:** Every file uploaded receives a unique CID (Content Identifier) from IPFS.
- **Blockchain Authentication:** Only authorized users can fetch the file hash from the smart contract.
- **Data Integrity:** Any attempt to modify a file results in a different hash, making tampering easy to detect.
- **User Roles:** Separate dashboards for Administrators and Data Owners.

## ⚙️ Setup
1. Clone the repository.
2. Install dependencies: `pip install django web3 ipfshttpclient`.
3. Start **Ganache** and ensure your RPC server matches the one in your configuration.
4. Run the Django server: `python manage.py runserver`.
5.
