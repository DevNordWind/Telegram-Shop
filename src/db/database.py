"""Database class with all-in-one features."""
from sqlalchemy.ext.asyncio import AsyncSession

from .repositories import UserRepo, WalletRepo, CategoryRepo, PositionRepo, PurchaseRepo, ItemRepo, RefillRepo, WithdrawRepo


class Database:

    """ User repository """
    user: UserRepo
    wallet: WalletRepo
    category: CategoryRepo
    position: PositionRepo
    purchase: PurchaseRepo
    item: ItemRepo
    refill: RefillRepo
    withdraw: WithdrawRepo

    def __init__(
            self,
            session: AsyncSession,
            user: UserRepo = None,
            wallet: WalletRepo = None,
            category: CategoryRepo = None,
            position: PositionRepo = None,
            purchase: PurchaseRepo = None,
            item: ItemRepo = None,
            refill: RefillRepo = None,
            withdraw: WithdrawRepo = None
    ):
        """Initialize Database class.

        :param session: AsyncSession to use
        :param user
        """
        self.session = session
        self.user = user or UserRepo(session=session)
        self.wallet = wallet or WalletRepo(session=session)
        self.category = category or CategoryRepo(session=session)
        self.position = position or PositionRepo(session=session)
        self.purchase = purchase or PurchaseRepo(session=session)
        self.item = item or ItemRepo(session=session)
        self.refill = refill or RefillRepo(session=session)
        self.withdraw = withdraw or WithdrawRepo(session=session)