from datetime import date
from database import get_monthly_spending, get_monthly_income

# ── Constants ────────────────────────────────────────────────────────────────
HOURLY_RATE        = 18          # dollars per hour
HOURS_PER_WEEK     = 11          # scheduled weekly hours
MONTHLY_INCOME     = round(HOURLY_RATE * HOURS_PER_WEEK * 52 / 12, 2)
# 52 weeks ÷ 12 months gives the average — more accurate than assuming 4 weeks
# round(..., 2) keeps it to two decimal places like real currency

PERSONAL_BUDGET_PCT = 0.35       # 35% of monthly income for personal spending
EBT_MONTHLY_BENEFIT = 298.00     # dollars, resets on the 6th

GO_OUT_EBT_THRESHOLD      = 50   # must have at least this much EBT remaining
GO_OUT_PERSONAL_THRESHOLD = 20   # must have at least this much personal budget remaining

# ── EBT calculations ─────────────────────────────────────────────────────────
def get_ebt_remaining():
    """Return how much EBT balance is left this month."""
    today = date.today()
    spent = get_monthly_spending("EBT", today.year, today.month)
    return round(EBT_MONTHLY_BENEFIT - spent, 2)
    # round(..., 2) prevents floating point issues like 298 - 47.82 = 250.17999999

# ── Personal budget calculations ──────────────────────────────────────────────
def get_personal_budget_limit():
    """Return the total personal budget for this month (35% of monthly income)."""
    return round(MONTHLY_INCOME * PERSONAL_BUDGET_PCT, 2)

def get_personal_budget_remaining():
    """Return how much personal budget is left this month."""
    today = date.today()
    spent = get_monthly_spending("personal", today.year, today.month)
    limit = get_personal_budget_limit()
    return round(limit - spent, 2)

def get_personal_budget_used_pct():
    """Returns percentage of personal budget you've used this month as a float 0 - 100"""
    spent = get_personal_budget_limit() - get_personal_budget_remaining()
    return round((spent / get_personal_budget_limit()) * 100, 1)

# ── Go out tonight? ───────────────────────────────────────────────────────────
def can_go_out_tonight():
    """Return True if both EBT and personal budget are above safe thresholds."""
    ebt_ok      = get_ebt_remaining() > GO_OUT_EBT_THRESHOLD
    personal_ok = get_personal_budget_remaining() > GO_OUT_PERSONAL_THRESHOLD
    return ebt_ok and personal_ok
    # Both conditions must be True — if either is False, the answer is False