
def eligibility_risk_agent(claim):

    risk_score = 0
    reasons = []

    # Check 1: Policy status
    if not claim.policy_active:
        risk_score += 50
        reasons.append("Insurance policy is inactive")

    # Check 2: Claim amount vs policy coverage
    if claim.claim_amount > claim.policy_amount:
        risk_score += 40
        reasons.append("Claim exceeds policy coverage")

    # Check 3: High claim amount
    elif claim.claim_amount > 0.8 * claim.policy_amount:
        risk_score += 20
        reasons.append("Claim amount is above 80% of coverage")

    # Determine risk category
    if risk_score >= 50:
        risk_level = "High"

    elif risk_score >= 20:
        risk_level = "Medium"

    else:
        risk_level = "Low"

    # Determine eligibility
    if not claim.policy_active:
        eligibility = "Not Eligible"

    elif claim.claim_amount > claim.policy_amount:
        eligibility = "Not Eligible"

    else:
        eligibility = "Eligible"

    return {
        "eligibility": eligibility,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_reasons": reasons
    }
