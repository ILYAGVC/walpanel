from fastapi.exceptions import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.schema._input import CreatePlan, Edit_Plan
from app.db.models import Plans, PurchaseHistory
from app.admin_services.api import panels_api
from app.log.logger_config import logger


class PlansQuery:

    async def get_plans(self, db: Session):
        try:
            plans = db.query(Plans).all()
            plans_count = len(plans)
            if not plans:
                return {"status": False, "count": plans_count, "message": "No plans found", "plans": []}
            return {
                "status": True,
                "count": plans_count,
                "plans": [
                    {
                        "id": plan.id,
                        "price": plan.price,
                        "traffic": plan.traffic,
                        "deadline": plan.days,
                    }
                    for plan in plans
                ],
            }
        except Exception as e:
            logger.error(f"Error in get_plans: {e}")
            return {"status": False, "message": "Error in get_plans", "error": str(e)}

    async def add_plan(self, db: Session, request: CreatePlan):
        try:
            new_plan = Plans(
                traffic=request.traffic, days=request.days, price=request.price
            )
            db.add(new_plan)
            db.commit()
            db.refresh(new_plan)
            return {
                "status": True,
                "message": "Plan added successfully",
                "id": new_plan.id,
            }
        except Exception as e:
            db.rollback()
            logger.error(f"Error in add_plan: {e}")
            return {"status": False, "message": "Failed to add plan", "error": str(e)}

    async def delete_plan(self, db: Session, id: int):
        try:
            plan = db.query(Plans).filter(Plans.id == id).first()
            if not plan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="plan not found with this id",
                )
            db.delete(plan)
            db.commit()
            await self.reorder_ids(db)
            return {"status": True, "message": "The plan was deleted"}
        except Exception as e:
            logger.error(f"Error in delete_plan: {e}")
            return {
                "status": False,
                "message": "Failed to delete this plan",
                "error": str(e),
            }

    async def edit_plan(self, db: Session, request: Edit_Plan):
        try:
            plan = db.query(Plans).filter(Plans.id == request.id).first()
            if not plan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="plan not found.",
                )
            plan.traffic = request.traffic
            plan.days = request.days
            plan.price = request.price
            db.commit()
            db.refresh(plan)
            return {
                "status": True,
                "message": "Plan edited successfully",
                "id": plan.id,
            }
        except Exception as e:
            logger.error(f"Error in edit_plan: {e}")
            return {"status": False, "message": "Failed to edit plan", "error": str(e)}

    async def reorder_ids(self, db: Session):
        try:
            plans = db.query(Plans).order_by(Plans.id).all()
            for index, plan in enumerate(plans, start=1):
                plan.id = index
            db.commit()
            return True
        except:
            return False

    async def get_a_plan_by_id(self, db: Session, id: int):
        try:
            plan = db.query(Plans).filter(Plans.id == id).first()
            if not plan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="plan not found with this id",
                )
            return {
                "status": True,
                "traffic": plan.traffic,
                "days": plan.days,
                "price": plan.price,
            }
        except Exception as e:
            logger.error(f"Error in get_a_plan_by_id: {e}")
            return {
                "status": False,
                "message": "Error in get_a_plan_by_id",
                "error": str(e),
            }
        
    async def purchase_history(self, db: Session):
        try:
            p_history = db.query(PurchaseHistory).all()
            count_history = len(p_history)
            if not p_history:
                return {"status": False, "count": count_history, "message": "No history found", "purchases": []}
            
            return {
                "status": True,
                "count": count_history,
                "purchases": [
                    {
                        "payer": purchase.payer,
                        "date": purchase.purchase_date,
                        "amount": purchase.amount,
                        "status": purchase.status
                    }
                    for purchase in p_history
                ]
            }
        except Exception as e:
            logger.error(f"Error in get purchases history from database: {e}")

plans_query = PlansQuery()
