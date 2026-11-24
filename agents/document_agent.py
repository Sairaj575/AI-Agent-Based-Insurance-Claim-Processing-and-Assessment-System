def document_verification_agent(claim):

    submitted_documents = set(claim.documents)

    required_documents = set(claim.required_documents)

    missing_documents = required_documents - submitted_documents

    if missing_documents:

        return {
            "document_status": "Incomplete",
            "missing_documents": list(missing_documents)
        }

    return {
        "document_status": "Complete",
        "missing_documents": []
    }