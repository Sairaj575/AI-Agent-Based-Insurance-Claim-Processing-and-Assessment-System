# AI Agent-Based Insurance Claim Processing and Assessment System

An AI-powered multi-agent insurance claim processing system that automates document verification, claim eligibility assessment, risk analysis, and claim summarization using specialized agents coordinated through LangGraph.

**Live Application:** https://ai-agent-based-insurance-claim-processing-and-assessment-syste.streamlit.app/

**GitHub Repository:** https://github.com/Sairaj575/AI-Agent-Based-Insurance-Claim-Processing-and-Assessment-System

---

## Project Overview

Insurance claim processing involves several stages, including document verification, policy eligibility checking, risk assessment, and claim evaluation.

This project demonstrates how a multi-agent AI architecture can automate these stages through specialized agents working together in a coordinated workflow.

The system consists of three specialized agents and a rule-based decision engine. LangGraph manages the execution flow and conditional routing, while Groq LLM generates natural-language insurance claim summaries.

The application provides a Streamlit-based interface through which users can enter claim details, submit documents, and view the processing results.

## Key Features

- **Multi-Agent Architecture:** Multiple specialized agents handle different insurance claim processing tasks.
- **Document Verification:** Identifies missing documents by comparing submitted and required documents.
- **Eligibility Assessment:** Checks insurance policy status and claim amount against policy coverage.
- **Risk Assessment:** Calculates an illustrative risk score and assigns a risk level.
- **AI-Powered Claim Summary:** Uses Groq LLM to generate a natural-language claim summary.
- **LangGraph Orchestration:** Coordinates agents and manages workflow execution.
- **Conditional Routing:** Routes claims to approval, rejection, or manual review outcomes.
- **Interactive Web Interface:** Streamlit frontend for submitting and processing insurance claims.
- **Fallback Mechanism:** Provides a Python-based summary when the LLM is unavailable.

## System Architecture

```text
                 USER
                   |
                   v
           STREAMLIT INTERFACE
                   |
                   v
           INSURANCE CLAIM DATA
                   |
                   v
       +---------------------------+
       |  DOCUMENT VERIFICATION    |
       |          AGENT            |
       +---------------------------+
                   |
                   v
       +---------------------------+
       |  ELIGIBILITY AND RISK     |
       |     ASSESSMENT AGENT      |
       +---------------------------+
                   |
                   v
       +---------------------------+
       |     CLAIM SUMMARY        |
       |         AGENT            |
       |       (Groq LLM)          |
       +---------------------------+
                   |
                   v
       +---------------------------+
       |      DECISION ENGINE      |
       +---------------------------+
                   |
                   v
          CONDITIONAL ROUTING
             /     |      \
            /      |       \
           v       v        v
        APPROVE  REJECT  MANUAL REVIEW
```

## Multi-Agent System Components

### 1. Document Verification Agent

Responsible for checking whether all required insurance documents have been submitted.

**Responsibilities:**
- Compares submitted documents with required documents.
- Identifies missing documents.
- Returns document verification status.

**Output:**
- Document status: Complete or Incomplete.
- List of missing documents.

### 2. Eligibility and Risk Assessment Agent

Evaluates the insurance claim based on policy status and coverage amount.

**Responsibilities:**
- Checks whether the insurance policy is active.
- Checks whether the claim amount exceeds the policy coverage.
- Calculates an illustrative risk score.
- Assigns a risk level.

**Risk assessment rules:**

| Condition | Risk Score |
|---|---:|
| Inactive insurance policy | +50 |
| Claim amount exceeds 80% of policy coverage | +20 |
| Claim amount exceeds policy coverage | +40 |

Risk levels:

| Risk Score | Risk Level |
|---|---|
| Below 20 | Low |
| 20–49 | Medium |
| 50 and above | High |

These are illustrative project rules, not validated insurance or fraud-detection criteria.

### 3. Claim Summary Agent

Generates a natural-language summary using the claim information and outputs from the previous agents.

**Responsibilities:**
- Summarizes insurance claim information.
- Explains document verification results.
- Explains eligibility and risk assessment.
- Highlights missing documents and risk reasons.

**Technology:** Groq API with LangChain integration.

The LLM generates summaries only. It does not independently approve or reject claims.

### 4. Decision Engine

A Python-based decision engine evaluates the outputs from the agents and determines the final recommended workflow outcome.

**Decision rules:**

| Condition | Recommended Outcome |
|---|---|
| Required documents are missing | Manual Review |
| Claim is not eligible | Rejection |
| Risk level is Medium or High | Manual Review |
| Documents complete, eligible and Low risk | Approval |

### 5. LangGraph Workflow Orchestration

LangGraph coordinates the execution of the agents.

**Workflow responsibilities:**
- Maintains shared claim state.
- Passes information between agents.
- Executes agents in sequence.
- Uses conditional edges for decision-based routing.
- Routes claims to the appropriate outcome node.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangGraph | Multi-agent workflow orchestration |
| LangChain | LLM integration |
| Groq API | LLM inference |
| Pydantic | Data validation and schema management |
| Streamlit | Interactive web application |
| python-dotenv | Environment variable management |

## Project Structure

```text
AI-Agent-Based-Insurance-Claim-Processing-and-Assessment-System/
│
├── agents/
│   ├── __init__.py
│   ├── document_agent.py
│   ├── eligibility_agent.py
│   └── summary_agent.py
│
├── schemas/
│   ├── __init__.py
│   └── claim.py
│
├── workflow/
│   ├── __init__.py
│   └── graph.py
│
├── app.py
├── main.py
├── test_workflow.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Groq API key (if using the Groq-powered summary)

### 1. Clone the repository

```bash
git clone https://github.com/Sairaj575/AI-Agent-Based-Insurance-Claim-Processing-and-Assessment-System.git
```

### 2. Navigate to the project directory

```bash
cd AI-Agent-Based-Insurance-Claim-Processing-and-Assessment-System
```

### 3. Create a virtual environment

```bash
python -m venv agentinsu
```

Activate the environment on Windows:

```powershell
agentinsu\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Obtain an API key from:

https://console.groq.com/

Never commit your `.env` file or expose your API key publicly.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Running Tests

Run the workflow test cases using:

```bash
python test_workflow.py
```

The project includes test scenarios for:

| Test Scenario | Expected Result |
|---|---|
| Active policy, complete documents, low risk | Approve |
| Active policy, complete documents, medium risk | Manual Review |
| Inactive policy | Reject |
| Missing required documents | Manual Review |

## Deployment

The application is deployed using Streamlit Community Cloud.

**Live Application:**

https://ai-agent-based-insurance-claim-processing-and-assessment-syste.streamlit.app/

The Groq API key is configured through Streamlit Secrets for secure deployment.



## Project Objective

The primary objective of this project is to demonstrate how a multi-agent AI architecture can automate different stages of insurance claim processing through specialized agents, LLM integration, and workflow orchestration.



## 👨‍💻 Author

**Sairaj Umbarkar**  
Aspiring Data Science Enthusiast  


⭐ If you find this project useful, feel free to star the repository!
