from typing import Optional
from app.modules.payment.schema import TransactionReadDTO
from app.modules.user.dto import UserReadDTO

class CourseTransactionReadDTO(TransactionReadDTO):
    user: UserReadDTO
    card_type: Optional[str] = None
