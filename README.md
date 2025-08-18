# 🛡️ Decentralized Identity Verification System - Backend

This repository contains the backend for the **Decentralized Identity Verification System**, built using **Django**, **IPFS**, and **Ethereum Smart Contracts**.  
The system allows authorities to issue verified documents and users to upload their own documents securely. All records are hashed on the blockchain for tamper-proof verification.

---

## 🚀 Features
- 🔐 **User Authentication** (JWT-based)
- 🏢 **Authority Issued Documents** (e.g., Certificates, Passports, Visas)
- 📂 **User Uploaded Documents** (with lost/stolen flag support)
- 🌐 **IPFS Integration** for secure decentralized file storage
- ⛓️ **Smart Contract Integration** with Ethereum (Ganache for local testing)
- ✅ **Document Verification** via blockchain hash lookup
- 🗂️ RESTful API endpoints for frontend integration

---

## 🛠️ Tech Stack
- **Backend:** Django, Django REST Framework  
- **Blockchain:** Solidity, Ganache (Local Ethereum)  
- **File Storage:** IPFS  
- **Database:** PostgreSQL / SQLite (for testing)  
- **Auth:** JWT (djangorestframework-simplejwt)  

---

## 📂 Project Structure
```text
core/
│── admin/ # For Monitoring
│── core/ # Django project config
│── users/ # User auth & profiles
│── documents/ # Document management
│── blockchain/ # Smart contract integration
│── requirements.txt # Python dependencies
│── manage.py # Django entrypoint
```


---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/decentralized-id-verification-backend.git

cd decentralized-id-verification-backend
```
---

### 2️⃣ Create Virtual Environment & Install Dependencies
```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate

pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables
``` 
Create a .env file in the root directory:

SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Database (SQLite example)
DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

```

### 4️⃣ Run Migrations & Start Server
``` bash
python manage.py migrate
python manage.py runserver
```

## 🔗 Getting the Contract Address

To integrate the smart contract with the backend, you need the deployed contract address. Follow these steps:

1. **Open Remix IDE**  
   Go to [https://remix.ethereum.org](https://remix.ethereum.org).

2. **Create/Open `DocumentStorage.sol`**  
   - Create a new file in the `contracts` folder.  
   - Paste your `DocumentStorage.sol` code.

3. **Compile the Contract**  
   - Click on the **Solidity Compiler** tab (🛠 icon).  
   - Select the correct compiler version.  
   - Click **Compile DocumentStorage.sol**.

4. **Deploy the Contract**  
   - Go to the **Deploy & Run Transactions** tab (🚀 icon).  
   - Choose **Environment**:  
     - **JavaScript VM** → Local testing  
     - **Injected Web3** → MetaMask network  
     - **Web3 Provider** → Custom RPC (e.g., Ganache)  
   - Select your contract in the **Contract** dropdown.  
   - Click **Deploy**.

5. **Copy the Contract Address**  
   - After deployment, find your contract under **Deployed Contracts**.  
   - Copy the **Contract at [address]**.  
   - Paste this address in `core/blockchain/service.py` as `CONTRACT_ADDRESS`.

> **Note:** Each deployment gives a new address. Use a testnet or local Ganache for persistent testing.


### 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### 📜 License

MIT License © 2025 Nagelli Karthikeya Goud
