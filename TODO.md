# Project TODO List

### Backend Foundation
- [x] FastAPI setup with project structure
- [x] PostgreSQL database connection
- [x] User authentication system (JWT tokens)
- [x] Password hashing with bcrypt
- [x] Protected endpoints with auth guards
- [x] API documentation (/docs)

### Database Schema (Multi-Company)
- [x] User model (without role - now per-company)
- [x] Company model (complete business profile)
- [x] CompanyMember model (user-company-role junction)
- [x] Invitation model (admin invites with role)
- [x] Database migration to multi-company system

### Company Profile Fields
- [x] Display name & legal name
- [x] Business registration number
- [x] Business structure (Sole prop, Partnership, LLP, Sdn Bhd, Bhd)
- [x] Industry classification
- [x] Tax ID (optional)
- [x] Company description & logo support
- [x] Contact details (email, phone, mobile, fax, website)
- [x] Social media links (Facebook, Instagram, LinkedIn, Twitter)
- [x] Mailing & billing addresses (with "same as" option)
- [x] Invoice display preferences

### Frontend Foundation
- [x] Vue.js 3 setup with Vite
- [x] Tailwind CSS v3 configuration
- [x] Vue Router with auth guards
- [x] Pinia state management
- [x] API service layer (Axios)
- [x] Auth store with login/logout
- [x] Beautiful login page
- [x] Dashboard page (old - needs update)

---

## 🏗️ IN PROGRESS (Current Session)

### Backend - Multi-Company Features
- [ ] Update registration service (create company + user as owner)
- [ ] Update registration endpoint
- [ ] Add company profile update endpoint
- [ ] Add company selection endpoint (for users with multiple companies)
- [ ] Add invitation endpoints (admin invites users)
- [ ] Update auth service for company context

### Frontend - Registration & Company Management
- [ ] Update registration form (add company fields)
- [ ] Add company settings page (update profile)
- [ ] Add company selector (if user has multiple companies)
- [ ] Update dashboard to show current company
- [ ] Add logo upload functionality

---

## 📋 NEXT UP (Phase 2)

### Multi-Company Complete
- [ ] Company switcher component
- [ ] Invitation system UI (admin sends invites)
- [ ] Accept invitation flow
- [ ] User management page (admin manages team)
- [ ] Role-based UI (different views per role)

### Email Features (Before Production)
- [ ] Email verification on registration
- [ ] Email service setup (SendGrid/SMTP)
- [ ] Verification email template
- [ ] Password reset flow
- [ ] Invitation emails

### Accounting Module
- [ ] Chart of accounts
- [ ] Invoices (create, edit, view, PDF generation)
- [ ] Purchase orders
- [ ] Payments tracking
- [ ] Expense management
- [ ] Financial reports

### Inventory Module
- [ ] Product/item master
- [ ] Stock tracking
- [ ] Barcode scanning (web camera)
- [ ] Stock adjustments
- [ ] Low stock alerts
- [ ] Warehouse management

### POS System
- [ ] Product catalog
- [ ] Cart management
- [ ] Payment processing
- [ ] Receipt generation
- [ ] Sales reports
- [ ] Kitchen Display System integration

### HRM Module
- [ ] Employee management
- [ ] Attendance tracking
- [ ] Payroll (basic)
- [ ] Leave management

---

## 🚀 FUTURE (Phase 3+)

### Real-Time Features (Node.js Service)
- [ ] WebSocket server setup
- [ ] In-app chat (Slack-like)
- [ ] Real-time notifications
- [ ] Live dashboard updates
- [ ] Kitchen Display System (real-time orders)

### IoT Integration
- [ ] MQTT broker setup
- [ ] CCTV integration
- [ ] Fire alarm monitoring
- [ ] Gate/shutter control
- [ ] Sensor dashboard

### Machine Learning
- [ ] Fraud detection (transactions)
- [ ] Sales forecasting
- [ ] Inventory optimization
- [ ] Customer behavior analysis

### Blockchain/Islamic Finance
- [ ] Smart contract integration
- [ ] P2P financing system
- [ ] Profit-sharing automation
- [ ] Sharia-compliant transactions

### Mobile App (Flutter)
- [ ] Mobile login/dashboard
- [ ] Mobile POS
- [ ] Barcode scanning (camera)
- [ ] Push notifications

---

## 🐛 Known Issues
- None yet (fresh migration)

---

## 💡 Notes

### Current Architecture
- **Backend:** Python/FastAPI (localhost:8000)
- **Frontend:** Vue.js 3 (localhost:5173)
- **Database:** PostgreSQL (multi-company schema)
- **Auth:** JWT tokens with role per company

### Test Users (After Re-registration)
- Will need to re-register after migration
- First user becomes company owner/superadmin

### Business Structures Supported
- Sole Proprietorship
- Partnership
- LLP (Limited Liability Partnership)
- PLT (Perkongsian Liabiliti Terhad)
- Sdn. Bhd. (Sendirian Berhad)
- Bhd. (Berhad)

### Invoice Display Preferences
- Configurable: email, phone, mobile, fax, website, social media
- Billing address can copy from mailing address
- Logo optional but supported