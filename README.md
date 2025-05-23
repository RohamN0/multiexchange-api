# 🪙 OKEX & ABAN Crypto API

A FastAPI service that aggregates wallet balances, trade history, and prices from OKEX and ABAN Tether. Includes real-time coin data, economic calendar, and news.

---

## 🔗 API Documentation

- **OKEX API Docs:** https://docs.ok-ex.io  
- **ABAN Tether API Docs:** https://docs.abantether.com

---

## 🚀 Features

- **/api/balance** - Combined wallet balances across OKEX & ABAN  
- **/api/buy_average** - Average buy prices from both platforms  
- **/api/sell_average** - Average sell prices from both platforms  
- **/api/coins** - Live OTC coin tickers from OKEX  
- **/api/news** - Latest financial headlines (scraped from Google News)  
- **/api/eco-cal** - This week’s economic calendar JSON

---

## 📦 Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-org/okex-aban-api.git
   cd okex-aban-api
   ```

2. **Create & activate virtualenv**  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   
4. **Install FastAPI Dev CLI**  
   ```bash
   pip install fastapi[all]
   ```

5. **Configure environment**  
   - Copy `.env.example` to `.env`  
   - Populate your keys:
     ```ini
     API_KEY_OKEX=your_okex_api_key
     SECRET_KEY_OKEX=your_okex_secret_key
     API_Key_ABAN=your_aban_api_key
     ```

---

## 🏃‍♂️ Running

Start in development mode with FastAPI’s CLI:

```bash
fastapi dev app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit the interactive API docs at  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔧 Usage Examples

### 1. Get Combined Balances
```bash
curl -u user:pass http://localhost:8000/api/balance
```

### 2. Get Average Buy Prices
```bash
curl -u user:pass http://localhost:8000/api/buy_average
```

### 3. Get Economic Calendar
```bash
curl -u user:pass http://localhost:8000/api/eco-cal
```

(Replace `user:pass` with your HTTP Basic credentials.)
