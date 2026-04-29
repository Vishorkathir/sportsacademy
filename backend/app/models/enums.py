import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    student = "student"


class AdmissionStatus(str, enum.Enum):
    pending = "pending"
    admitted = "admitted"
    rejected = "rejected"


class NotificationStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class PaymentSource(str, enum.Enum):
    manual = "manual"
    notification = "notification"


class DerivedPaymentStatus(str, enum.Enum):
    nopaid = "nopaid"
    halfpayed = "halfpayed"
    fulpayed = "fulpayed"


class StudentSkill(str, enum.Enum):
    batting = "Batting"
    bowling = "Bowling"
    wicket_keeping = "Wicket Keeping"
