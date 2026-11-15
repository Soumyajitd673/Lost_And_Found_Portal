from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from backend.service import user_service, report_service
from backend.database.db import get_db
from backend.schema.Report_Schema import Report_Schema
from backend.curr_user import get_current_user
from backend.templates import templates

router = APIRouter(prefix="/report", tags=["report"])

@router.get("")
def get_reports_page(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
    ):

    if user_service.is_admin(db, user_id):

        pending_reports = report_service.get_all_pending_reports(db)
        report_count = report_service.get_reports_count(db)

        return templates.TemplateResponse(
            request=request,
            name="Admin_Dashboard.html",
            context={
                'pending_reports': pending_reports,
                'pending': report_count.get('pending', 0),
                'resolve': report_count.get('resolved', 0),
                'total': sum(report_count.values()),
            }
        )

    else:
        raise HTTPException(status_code=403, detail="Only Admin Access.")


@router.post("/{report_id}/resolve")
def resolve_report(
    report_id: int,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user_service.is_admin(db, user_id):
        raise HTTPException(status_code=403, detail="Only Admin Access.")

    try:
        report_service.resolve_report(db, report_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return RedirectResponse(url="/report", status_code=303)


@router.post("")
def create_report(
    report_schema: Report_Schema,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):

    try:
        report = report_service.create_report(db, report_schema, user_id)

        return True

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
