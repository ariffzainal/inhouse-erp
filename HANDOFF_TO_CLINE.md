# 🔄 Claude → Cline Handoff Document

**Date:** 2025-10-13
**Status:** Multi-company registration working, needs company management endpoints

---

## ✅ What's Working

### Backend
- Multi-company database schema (users, companies, company_members, invitations)
- User registration creates company + assigns user as owner with admin role
- POST `/api/v1/auth/register` - Working ✅
- POST `/api/v1/auth/login` - Working ✅
- GET `/api/v1/auth/me` - Working ✅

### Frontend
- Registration form with company fields - Working ✅
- Login page - Working ✅
- Dashboard - Working (but needs company context) ⚠️
- Auth store configured for multi-company
- API service calls defined

---

## ❌ What's Missing (DO NEXT)

### Backend Endpoints Needed

**File:** `backend/app/api/company.py` (needs to be created)

**Required endpoints:**

1. **GET `/api/v1/companies/`**
   - Get all companies current user belongs to
   - Returns: `[{company, role, is_owner}]`

2. **POST `/api/v1/companies/select`**
   - Select active company for session
   - Body: `{company_id: int}`
   - Returns: Updated user with current_company context

3. **GET `/api/v1/companies/{company_id}`**
   - Get specific company details
   - Returns: Full company profile

4. **PUT `/api/v1/companies/{company_id}`**
   - Update company profile
   - Body: CompanyUpdate schema
   - Returns: Updated company

**Also need:**
- Import company router in `backend/app/main.py`
- Add router: `app.include_router(company_router)`

---

## 📂 Project Structure
```
backend/
├── app/
│   ├── api/
│   │   ├── auth.py          ✅ Complete
│   │   └── company.py       ❌ NEEDS TO BE CREATED
│   ├── services/
│   │   ├── auth_service.py  ✅ Complete
│   │   └── company_service.py ✅ Complete (has helper functions)
│   ├── models/
│   │   ├── user.py          ✅ (no role column)
│   │   ├── company.py       ✅ (full business profile)
│   │   ├── company_member.py ✅
│   │   └── invitation.py    ✅
│   └── schemas/
│       ├── user.py          ✅
│       └── company.py       ✅

frontend/erp-frontend/
├── src/
│   ├── stores/
│   │   └── auth.js          ✅ Complete
│   ├── services/
│   │   └── api.js           ✅ Complete (calls endpoints that don't exist yet)
│   └── views/
│       ├── LoginView.vue    ✅ Working
│       ├── RegisterView.vue ✅ Working
│       └── DashboardView.vue ⚠️ Needs company context update
```

---

## 🎯 Immediate Next Steps (Priority Order)

### Step 1: Create Company Endpoints (30 mins)
Create `backend/app/api/company.py` with 4 endpoints listed above

### Step 2: Import Router (2 mins)
Add to `backend/app/main.py`:
```python
from app.api.company import router as company_router
app.include_router(company_router)
```

### Step 3: Update Dashboard (15 mins)
Show current company name and user's role in that company

### Step 4: Test Complete Flow (10 mins)
1. Register → creates user + company
2. Login → returns user companies
3. Dashboard → shows company info

---

## 🗄️ Database Schema Reference

### companies table
- id, display_name, legal_name, slug
- business_registration_number, business_structure, industry
- tax_id, description, logo_url
- Contact: email, phone, mobile, fax, website
- Social: facebook, instagram, linkedin, twitter
- Addresses: mailing_address, billing_address, billing_same_as_mailing
- Invoice settings: show_* fields
- is_active, created_at, updated_at

### company_members table
- id, user_id, company_id
- role (admin, manager, accountant, inventory_staff, etc.)
- status (active, inactive, pending)
- is_owner (boolean)
- joined_at, updated_at

### users table
- id, email, full_name, hashed_password
- is_active, is_verified
- created_at, updated_at
- **NOTE:** NO role column (role is per-company in company_members)

---

## 🔑 Key Business Logic

### Registration Flow
1. User registers with company details
2. Create user in `users` table
3. Create company in `companies` table
4. Create company_member linking them (role=admin, is_owner=true)
5. Return user with current_company context

### Login Flow
1. Authenticate user
2. Fetch user's companies from company_members
3. If only 1 company → auto-select it
4. If multiple → user selects later
5. Return user with current company context

### Company Selection
1. User has multiple companies
2. POST /companies/select with company_id
3. Verify user is member of that company
4. Update session context
5. Return user with new current_company

---

## 🧪 Test Credentials

**After registration:**
- Email: ahmad@tsbandtps.com
- Password: SecurePass123!
- Company: TSB & TPS Sdn Bhd
- Role: admin (owner)

---

## 🎨 Frontend Theme

**Custom colors in tailwind.config.js:**
- primary: #2F4F4F (Obsidian Green)
- accent: #B8860B (DarkGoldenRod)
- light-neutral: #F8F8F8 (WhiteSmoke)
- dark-neutral: #36454F (Charcoal)

---

## 📋 Dependencies

**Backend:**
- Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL
- Database: erpdb, user: erpuser, password: securepassword123

**Frontend:**
- Vue 3, Vite, Tailwind CSS v3, Pinia, Vue Router, Axios

---

## 🚀 To Resume Development

**Backend:**
```bash
cd ~/sideprojects/inhouse-erp/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd ~/sideprojects/inhouse-erp/frontend/erp-frontend
pnpm run dev
```

**URLs:**
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

---

## 💡 Important Notes

1. **Import Style:** Use absolute imports (`from app.x import y`) NOT relative (`from ..x import y`)
2. **No localStorage in artifacts** - but regular code can use it
3. **Email verification** - Postponed to Phase 2
4. **Role assignment** - Admin invites users, assigns roles (not self-selected)

---

## 🎯 End Goal

**Complete multi-company ERP like Xero where:**
- One email can belong to multiple companies
- Each company has different roles per user
- Admins invite team members
- Users can switch between companies
- Role-based UI shows different features per role

---

**Good luck! The foundation is solid!** 🚀