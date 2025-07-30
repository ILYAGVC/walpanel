from sqlalchemy.orm import Session
from app.db.models import PurchaseHistory
from app.log.logger_config import logger
from app.db.models import PurchaseHistory

async def purchase_hisory(db: Session, amount, purchase_date, payer, status):
    """
    recording the purchase status in the database
    """
    try:
        p_history = PurchaseHistory(
            amount=amount,
            purchase_date=purchase_date,
            payer=payer,
            status=status
        )
        db.add(p_history)
        db.commit()
        db.refresh(p_history)
    except Exception as e:
        logger.error(f"we have a problem here (purchase history): {e}")