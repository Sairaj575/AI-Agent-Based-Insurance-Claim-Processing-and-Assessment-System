
from typing import TypedDict

from schemas.claim import InsuranceClaim

from agents.document_agent import document_verification_agent
from agents.eligibility_agent import eligibility_risk_agent
from agents.summary_agent import claim_summary_agent

from langgraph.graph import StateGraph, START, END


# 1. Define the workflow state
class ClaimState(TypedDict, total=False):
    claim: InsuranceClaim
    document_result: dict
    eligibility_result: dict
    summary_result: dict
    decision: str
    decision_reason: str
    final_status: str


# 2. Document verification node
def document_node(state: ClaimState):
    claim = state["claim"]
    result = document_verification_agent(claim)

    return {"document_result": result}


# 3. Eligibility and risk assessment node
def eligibility_node(state: ClaimState):
    claim = state["claim"]
    result = eligibility_risk_agent(claim)

    return {"eligibility_result": result}


# 4. Claim summary node
def summary_node(state: ClaimState):
    claim = state["claim"]

    result = claim_summary_agent(
        claim,
        state["document_result"],
        state["eligibility_result"],
        use_gemini=True
    )

    return {"summary_result": result}


# 5. Decision engine
def decision_node(state: ClaimState):

    document_result = state["document_result"]
    eligibility_result = state["eligibility_result"]

    if document_result["document_status"] == "Incomplete":
        decision = "manual_review"
        reason = "Required insurance documents are missing."

    elif eligibility_result["eligibility"] == "Not Eligible":
        decision = "reject"
        reason = "The claim does not satisfy the insurance policy eligibility criteria."

    elif eligibility_result["risk_level"] in ["Medium", "High"]:
        decision = "manual_review"
        reason = "The claim requires additional review due to its assessed risk level."

    else:
        decision = "approve"
        reason = "All required documents are submitted and the claim satisfies the defined eligibility criteria."

    return {
        "decision": decision,
        "decision_reason": reason
    }


# 6. Conditional routing function
def route_decision(state: ClaimState):

    return state["decision"]


# 7. Final outcome nodes
def approved_node(state: ClaimState):
    return {"final_status": "Claim recommended for approval"}


def rejected_node(state: ClaimState):
    return {"final_status": "Claim recommended for rejection"}


def manual_review_node(state: ClaimState):
    return {"final_status": "Claim requires manual review"}


# 8. Build the LangGraph workflow
builder = StateGraph(ClaimState)

builder.add_node("document", document_node)
builder.add_node("eligibility", eligibility_node)
builder.add_node("summary", summary_node)
builder.add_node("decision", decision_node)

builder.add_node("approved", approved_node)
builder.add_node("rejected", rejected_node)
builder.add_node("manual_review", manual_review_node)


# 9. Normal sequential edges
builder.add_edge(START, "document")
builder.add_edge("document", "eligibility")
builder.add_edge("eligibility", "summary")
builder.add_edge("summary", "decision")


# 10. Conditional edges
builder.add_conditional_edges(
    "decision",
    route_decision,
    {
        "approve": "approved",
        "reject": "rejected",
        "manual_review": "manual_review"
    }
)


# 11. Connect outcomes to END
builder.add_edge("approved", END)
builder.add_edge("rejected", END)
builder.add_edge("manual_review", END)


# 12. Compile workflow
claim_workflow = builder.compile()
