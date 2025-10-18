# 📋 Immediate TODO for Cline

## 🔴 URGENT: Create Backend Company Endpoints

### File to Create: `backend/app/api/company.py`

**Template structure:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.company import CompanyResponse, CompanyUpdate
from app.services.company_service import (
    get_user_companies,
    get_company_by_id,
    update_company,
    check_user_company_access
)
from app.api.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/api/v1/companies",
    tags=["Companies"]
)

@router.get("/")
def get_my_companies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all companies user belongs to"""
    # TODO: Implement using get_user_companies()
    pass

@router.post("/select")
def select_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Select active company"""
    # TODO: Verify access, update context
    pass

@router.get("/{company_id}")
def get_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get company details"""
    # TODO: Check access, return company
    pass

@router.put("/{company_id}")
def update_company_profile(
    company_id: int,
    company_data: CompanyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update company profile"""
    # TODO: Check access, update, return
    pass
```

### Then Add to main.py:
```python
from app.api.company import router as company_router
app.include_router(company_router)
```

---

## ✅ Expected Behavior After Implementation

1. Registration → 201 Created
2. Login → 200 OK  
3. GET /companies/ → Returns user's companies
4. Dashboard loads with company context

---

**Start with company.py - everything else depends on it!**