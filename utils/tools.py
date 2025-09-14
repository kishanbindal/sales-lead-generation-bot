from langchain_core.tools import tool
import json
import streamlit as st

@tool
def save_generated_lead(email: str, lead_notes: str):
    """
    Save a json file with the email and lead notes, This would enable a sales representative to reach out to the user in case they are interested in the product.

    Inputs:
    - email: str - The email ID of the user (valid email ID format user@example.com)
    - lead_notes: str - Notes either provided by the uesr or inferred from conversation history

    Output:
    - bool - True if the lead is saved successfully, False otherwise
    """
    try:
        with open("generated_leads.json", "a") as f:
            f.write(json.dumps({"email": email, "lead_notes": lead_notes}) + "\n")
        st.session_state.generated_lead = True
        return True
    except Exception as e:
        print(e)
        return False