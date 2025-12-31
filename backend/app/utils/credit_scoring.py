"""
Credit scoring algorithm
Based on industry-standard FICO-like scoring model
"""
from typing import Dict, List, Optional
from datetime import date, timedelta
from app.models.credit_account import CreditAccount, AccountStatus, PaymentStatus
from app.models.consumer import Consumer


def calculate_credit_score(consumer: Consumer, credit_accounts: List[CreditAccount]) -> Dict:
    """
    Calculate credit score based on credit accounts
    Returns score (300-850) and scoring factors
    """
    if not credit_accounts:
        return {
            "score": 0,
            "factors": {
                "payment_history": "No credit history",
                "credit_utilization": "No credit history",
                "length_of_history": "No credit history",
                "credit_mix": "No credit history",
                "new_credit": "No credit history"
            }
        }
    
    # Filter out closed accounts older than 7 years
    active_accounts = [
        acc for acc in credit_accounts
        if acc.account_status != AccountStatus.CLOSED or 
        (acc.close_date and (date.today() - acc.close_date).days < 2555)  # 7 years
    ]
    
    if not active_accounts:
        return {
            "score": 0,
            "factors": {"message": "No active credit history"}
        }
    
    # Payment History (35% of score)
    payment_history_score = calculate_payment_history_score(active_accounts)
    
    # Credit Utilization (30% of score)
    utilization_score = calculate_utilization_score(active_accounts)
    
    # Length of Credit History (15% of score)
    history_length_score = calculate_history_length_score(active_accounts)
    
    # Credit Mix (10% of score)
    credit_mix_score = calculate_credit_mix_score(active_accounts)
    
    # New Credit (10% of score)
    new_credit_score = calculate_new_credit_score(active_accounts)
    
    # Calculate weighted score (300-850 range)
    base_score = 300
    max_points = 550
    
    weighted_score = (
        payment_history_score * 0.35 +
        utilization_score * 0.30 +
        history_length_score * 0.15 +
        credit_mix_score * 0.10 +
        new_credit_score * 0.10
    )
    
    final_score = int(base_score + (weighted_score * max_points))
    final_score = max(300, min(850, final_score))  # Clamp between 300-850
    
    return {
        "score": final_score,
        "factors": {
            "payment_history": f"{payment_history_score:.1f}%",
            "credit_utilization": f"{utilization_score:.1f}%",
            "length_of_history": f"{history_length_score:.1f}%",
            "credit_mix": f"{credit_mix_score:.1f}%",
            "new_credit": f"{new_credit_score:.1f}%"
        }
    }


def calculate_payment_history_score(accounts: List[CreditAccount]) -> float:
    """Calculate payment history score (0-100)"""
    if not accounts:
        return 0.0
    
    total_score = 0.0
    for account in accounts:
        if account.payment_status == PaymentStatus.CURRENT:
            total_score += 100
        elif account.payment_status == PaymentStatus.LATE_30:
            total_score += 70
        elif account.payment_status == PaymentStatus.LATE_60:
            total_score += 50
        elif account.payment_status == PaymentStatus.LATE_90:
            total_score += 30
        elif account.payment_status == PaymentStatus.LATE_120_PLUS:
            total_score += 10
        elif account.payment_status == PaymentStatus.NO_PAYMENT:
            total_score += 0
        else:
            total_score += 50  # Default
    
    return total_score / len(accounts)


def calculate_utilization_score(accounts: List[CreditAccount]) -> float:
    """Calculate credit utilization score (0-100)"""
    if not accounts:
        return 0.0
    
    total_balance = sum(float(acc.current_balance or 0) for acc in accounts)
    total_limit = sum(float(acc.credit_limit or 0) for acc in accounts if acc.credit_limit)
    
    if total_limit == 0:
        return 50.0  # No credit limit data
    
    utilization_ratio = total_balance / total_limit
    
    # Lower utilization is better
    if utilization_ratio <= 0.10:
        return 100.0
    elif utilization_ratio <= 0.30:
        return 90.0
    elif utilization_ratio <= 0.50:
        return 70.0
    elif utilization_ratio <= 0.70:
        return 50.0
    elif utilization_ratio <= 0.90:
        return 30.0
    else:
        return 10.0


def calculate_history_length_score(accounts: List[CreditAccount]) -> float:
    """Calculate length of credit history score (0-100)"""
    if not accounts:
        return 0.0
    
    oldest_account = min(accounts, key=lambda x: x.open_date)
    days_since_open = (date.today() - oldest_account.open_date).days
    years = days_since_open / 365.25
    
    # More years is better
    if years >= 10:
        return 100.0
    elif years >= 7:
        return 85.0
    elif years >= 5:
        return 70.0
    elif years >= 3:
        return 55.0
    elif years >= 1:
        return 40.0
    else:
        return 20.0


def calculate_credit_mix_score(accounts: List[CreditAccount]) -> float:
    """Calculate credit mix score (0-100)"""
    if not accounts:
        return 0.0
    
    account_types = set(acc.account_type for acc in accounts)
    
    # More diverse credit types is better
    if len(account_types) >= 4:
        return 100.0
    elif len(account_types) == 3:
        return 80.0
    elif len(account_types) == 2:
        return 60.0
    else:
        return 40.0


def calculate_new_credit_score(accounts: List[CreditAccount]) -> float:
    """Calculate new credit score (0-100)"""
    if not accounts:
        return 0.0
    
    # Check accounts opened in last 6 months
    six_months_ago = date.today() - timedelta(days=180)
    recent_accounts = [acc for acc in accounts if acc.open_date >= six_months_ago]
    
    # Fewer new accounts is better (but some is okay)
    if len(recent_accounts) == 0:
        return 100.0
    elif len(recent_accounts) == 1:
        return 80.0
    elif len(recent_accounts) == 2:
        return 60.0
    elif len(recent_accounts) <= 3:
        return 40.0
    else:
        return 20.0

