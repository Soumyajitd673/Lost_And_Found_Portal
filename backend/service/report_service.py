from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from backend.schema.Report_Schema import Report_Schema
from backend.models.report import Report
from backend.service import user_service

def create_report(db: Session, data: Report_Schema, reporter_id: int, ):

    reported_user_id = user_service.get_user_by_email(db, data.reported_user_email).id

    if (reported_user_id == reporter_id):
        raise ValueError("Cannot report yourself.")

    report = Report(
        reporter_id=reporter_id,
        reported_user_id=reported_user_id,
        report_description=data.report_description
    )

    db.add(report)

    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(str(e))

    db.refresh(report)

    return report


def get_all_pending_reports(db: Session):
    return db.scalars(select(Report).where(Report.status == "Pending")).all()

def get_reports_count(db: Session):

    query = select(Report.status, func.count(Report.id).label('count')).group_by(Report.status)

    result = {}

    for status, count in db.execute(query).all():
        result[status] = count

    return result

