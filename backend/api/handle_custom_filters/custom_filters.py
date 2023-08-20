from .abstract_custom_filters import (
                                        ByAttrFilterBackend,
                                        ByRangeFilterBackend
                                     )


class ByApplicantAttrFilterBackend(ByAttrFilterBackend):
    """
    Filter by Applicant attributes.
    """

    attrs = ['first_name', 'last_name', 'dni', 'gender', 'email']

class ByLoanRequestAttrFilterBackend(ByAttrFilterBackend):
    """
    Filter by LoanRequest attributes.
    """

    attrs = ['amount', 'approved']

class ByAmountRangeFilterBackend(ByRangeFilterBackend):
    """
    Filter by amount range.
    """

    attr = "amount"