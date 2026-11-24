
import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def claim_summary_agent(claim, document_result, eligibility_result,use_gemini=True):

    model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2,
)

    # Prepare the information for Gemini
    claim_data = claim.model_dump()

    prompt = f"""
    You are an insurance claim summary assistant.

    Analyze the following insurance claim information.

    Claim Information:
    {json.dumps(claim_data, indent=2)}

    Document Verification Result:
    {json.dumps(document_result, indent=2)}

    Eligibility and Risk Assessment:
    {json.dumps(eligibility_result, indent=2)}

    Instructions:
    1. Summarize the insurance claim.
    2. Explain the document verification result.
    3. Explain the eligibility and risk assessment.
    4. Mention any missing documents or risk reasons.
    5. Do not invent information.
    6. Do not make the final approval or rejection decision.

    Generate a clear and professional summary.
    """

    # # Send prompt to Gemini
    # response = model.invoke(prompt)

    # return {
    #     "claim_summary": response.content
    # }
    try:
        response = model.invoke(prompt)

        return {
            "claim_summary": response.content,
            "status": "success"
        }

    except Exception as e:


        print("Gemini API error:", e)

    # Generate fallback summary using Python

        summary = f"""
        Insurance Claim Summary

        Claim ID: {claim.claim_id}

        Customer: {claim.customer_name}

        Document Status:
            {document_result['document_status']}

        Eligibility:
            {eligibility_result['eligibility']}

        Risk Score:
            {eligibility_result['risk_score']}

        Risk Level:
            {eligibility_result['risk_level']}

        Risk Reasons:
            {eligibility_result['risk_reasons']}

        Note: This summary was generated using
        Python fallback logic because Gemini was unavailable.
        """

        return {
            "claim_summary": summary,
            "status": "fallback"
        }