from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.service import user_service, report_service
from backend.database.db import get_db
from backend.schema.Report_Schema import Report_Schema
from backend.curr_user import get_current_user
from backend.templates import templates

router = APIRouter(prefix="/report", tags=["report"])

@router.get()
def get_reports_page(request: Request, db: Session = Depends(get_db)):

    user_id = Session.get("user_id")

    if user_service.is_admin(db, user_id):

        reports = report_service.get_all_reports(db)
        report_count = report_service.get_reports_count(db)

        return templates.TemplateResponse(
            request=request,
            name="admin_dashboard.html",
            context={
                'reports': reports,
                'pending': report_count.get('pending', 0),
                'resolve': report_count.get('resolved', 0)
            }
        )
    
    else:
        raise HTTPException(status_code=400, detail="Only Admin Access.")


@router.post()
def create_report(
    report_schema: Report_Schema,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):

    try:
        data = Report_Schema.model_validate_json(report_schema)
        report = report_service.create_report(db, data, user_id)

        return True
    
    except ValueError as e:
        raise HTTPException(detail=str(e))
        