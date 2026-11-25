import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except FileNotFoundError:
    pass

from schemas.claim import InsuranceClaim
from workflow.graph import claim_workflow


# Page configuration
st.set_page_config(
    page_title="AI Insurance Claim Processing",
    page_icon="📄",
    layout="wide"
)


# Application title
st.title("AI-Based Insurance Claim Processing System")
st.write(
    "Automated insurance claim analysis using "
    "multiple AI agents and LangGraph."
)

st.divider()


# Claim details form
st.header("Enter Insurance Claim Details")

with st.form("claim_form"):

    col1, col2 = st.columns(2)

    with col1:
        claim_id = st.text_input(
            "Claim ID",
            value="CLM1001"
        )

        customer_name = st.text_input(
            "Customer Name",
            value="Rahul"
        )

        claim_amount = st.number_input(
            "Claim Amount (₹)",
            min_value=1.0,
            value=40000.0
        )

    with col2:
        policy_amount = st.number_input(
            "Policy Coverage Amount (₹)",
            min_value=1.0,
            value=100000.0
        )

        policy_active = st.selectbox(
            "Is the insurance policy active?",
            ["Yes", "No"]
        )

        incident_description = st.text_area(
            "Incident Description",
            value="Hospitalization due to accident"
        )

    st.subheader("Document Verification")

    available_documents = [
        "identity_proof",
        "medical_bill",
        "hospital_report"
    ]

    documents = st.multiselect(
        "Select submitted documents",
        available_documents,
        default=available_documents
    )

    submitted = st.form_submit_button(
        "Process Insurance Claim",
        type="primary"
    )


# Process claim
if submitted:

    if not claim_id.strip() or not customer_name.strip():
        st.error("Claim ID and customer name are required.")

    else:

        try:
            claim = InsuranceClaim(
                claim_id=claim_id.strip(),
                customer_name=customer_name.strip(),
                claim_amount=claim_amount,
                policy_amount=policy_amount,
                policy_active=(policy_active == "Yes"),
                documents=documents,
                required_documents=available_documents,
                incident_description=incident_description
            )

            with st.spinner("Processing insurance claim..."):

                result = claim_workflow.invoke({
                    "claim": claim
                })

            st.success("Claim processing completed!")

            st.divider()

            # Document verification
            st.header("1. Document Verification")

            doc_result = result["document_result"]

            st.write(
                "Document Status:",
                doc_result["document_status"]
            )

            if doc_result["missing_documents"]:
                st.warning(
                    "Missing Documents: "
                    + ", ".join(doc_result["missing_documents"])
                )
            else:
                st.success("All required documents submitted.")

            # Eligibility and risk
            st.header("2. Eligibility and Risk Assessment")

            eligibility = result["eligibility_result"]

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Eligibility",
                eligibility["eligibility"]
            )

            col2.metric(
                "Risk Score",
                eligibility["risk_score"]
            )

            col3.metric(
                "Risk Level",
                eligibility["risk_level"]
            )

            if eligibility["risk_reasons"]:
                st.write("Risk Reasons:")
                for reason in eligibility["risk_reasons"]:
                    st.write("- " + reason)

            # Claim summary
            st.header("3. Claim Summary")

            st.write(
                result["summary_result"]["claim_summary"]
            )

            st.caption(
                "Summary method: "
                + result["summary_result"]["status"]
            )

            # Final decision
 
            st.header("4. Final Decision")

            decision = result["decision"]

            if decision == "approve":
                st.success("Claim Recommended for Approval")

            elif decision == "reject":
                st.error("Claim Recommended for Rejection")

            else:
                st.warning("Claim Requires Manual Review")

            st.write("Reason:", result["decision_reason"])

            st.caption(
                "This is a demonstration system. Final insurance "
                "decisions require appropriate human review."
            )

        except Exception as e:
            st.error(f"Error processing claim: {e}")
