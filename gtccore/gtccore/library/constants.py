from enum import Enum


class PaymentMode(Enum):
    '''Payment mode for application'''
    ONLINE = 'online'
    BANK = 'bank'


class PaymentStatus(Enum):
    '''Payment status for application'''
    PENDING = 'pending'
    NOT_PAID = 'not_paid'
    PAID = 'paid'


class ApplicationStatus(Enum):
    '''Application status for application'''
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'