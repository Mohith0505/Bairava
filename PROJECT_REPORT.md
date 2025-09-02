# Algo Bridge Web Platform (Project Report)

## 1. Vision
A web-based algorithmic trading bridge for Indian markets and beyond.  
Key goals:
- Browser-only (no VPS, no desktop client).
- Connect to 70+ brokers (AngelOne, Zerodha, Dhan, Fyers, 5paisa, AliceBlue, etc.).
- Include advanced modules:  
  - Quick Trade Panel (QTP)  
  - Multi-leg Options Builder  
  - Option Chain Trading  
  - Risk Management  
  - Order Slicing  
  - Multi-account execution  
  - Virtual Trading sandbox (19-day free trial)  
- Auto-subscription management with Razorpay (recurring, expiry, grace).  
- Admin Console for user management, subscription control, and payments.

---

## 2. Tech Stack
- **Backend** → FastAPI (Python 3.11+)
- **Frontend** → React (Vite, Tailwind, shadcn/ui)
- **Database** → SQLite (dev), PostgreSQL (production)
- **Auth** → JWT-based with trial + auto-renew
- **Payments** → Razorpay
- **Realtime data** → Broker APIs, Amibroker, TradingView webhooks

---

## 3. Roadmap (Modules)
### M1 — Auth & Subscription
- Login / Signup / Logout
- JWT token auth
- Free trial (19 days)
- Auto subscription expiry
- Razorpay integration (auto-renew)

### M2 — Broker Integration
- Paper broker (sandbox)
- AngelOne integration
- Account linking (via credentials)

### M3 — Orders & PnL
- Send market/limit orders
- Track fills and positions
- Compute realized/unrealized PnL
- Basic dashboard

### M4 — Option Chain & Strategy Builder
- Live option chain (NIFTY, BANKNIFTY, FINNIFTY)
- Multi-leg strategy builder
- Greeks & IV calculations
- One-click execution

### M5 — Risk Management & Order Slicing
- Define max daily loss
- Define max daily trades
- Auto-square off if breached
- Order slicing (e.g., break 100 lots into 10×10 lots)

### M6 — Multi-account & Virtual Trading
- Manage multiple broker accounts
- Execute same trade in all accounts
- Virtual trading sandbox with mock fills

### M7 — Admin Console
- Manage subscriptions
- View users and accounts
- Control expiries and payments
- Logs & monitoring

---

## 4. Database Models (simplified)
- **User** → id, email, password_hash, role, is_active
- **Subscription** → id, user_id, plan, status, trial_until, expiry_date
- **Broker** → id, name, type, credentials
- **Account** → id, user_id, broker_id, label, status
- **Order** → id, account_id, symbol, qty, side, status, timestamps
- **Position** → id, account_id, symbol, qty, avg_price
- **Trade** → id, order_id, fill_price, qty
- **RiskRule** → id, user_id, max_loss, max_trades, auto_squareoff

---

## 5. Page Flow
- Login → Dashboard
- Dashboard → Brokers → Accounts
- Dashboard → Orders → Positions → PnL
- Option Chain → Strategy Builder → Execute
- Settings → Risk Rules, Credentials
- Admin → Subscriptions, Payments, Users

---

## 6. Dev Principles
- Vertical slices: backend + frontend feature by feature.
- All APIs documented in Swagger (FastAPI auto).
- GitHub repo is the **single source of truth**.
- Commit convention: `feat/*`, `fix/*`, `chore/*`.
- PROJECT_REPORT.md updated every milestone.

---
