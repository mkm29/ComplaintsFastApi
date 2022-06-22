import enum


class RoleType(enum.Enum):
    approver = "approver"
    complainer = "complainer"
    admin = "admin"


class State(enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class CurrencyType(enum.Enum):
    # only allow IBAN transfers for now
    EUR = "EUR"
    GBP = "GBP"
