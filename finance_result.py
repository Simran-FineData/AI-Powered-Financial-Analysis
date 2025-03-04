import spacy
import re
import streamlit as st
import pandas as pd

# Handle exception when 'en_core_web_sm' spaCy model is not installed

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.error("Error: spaCy model not found. Run `python -m spacy download en_core_web_sm`.")
    st.stop()

# Load company names from Excel file
def load_companies_from_excel(file_path="Known_Companies_List.xlsx"):
    try:
        df = pd.read_excel(file_path)
        if "Company Name" not in df.columns:
            st.error("Error: 'Company Name' column not found in Excel file.")
            return []
        companies = df["Company Name"].dropna().astype(str).str.strip().tolist()
        return companies
    except Exception as e:
        st.error(f"Error loading companies Excel file: {e}")
        return []

# Load financial parameters from Excel file
def load_financial_parameters(file_path="Parameters.xlsx"):
    try:
        df = pd.read_excel(file_path)
        if "Item Name(Parameters)" not in df.columns:
            st.error("Error: 'Item Name(Parameters)' column not found in Excel file.")
            return []
        params = df["Item Name(Parameters)"].dropna().astype(str).str.strip().tolist()
        return params
    except Exception as e:
        st.error(f"Error loading parameters Excel file: {e}")
        return []

# Load data
known_companies = load_companies_from_excel()
financial_parameters = load_financial_parameters()

# Sort known_companies alphabetically
known_companies.sort()  # Sort alphabetically for consistent matching

# Common words to ignore
ignore_words = {"check", "tell", "show", "what", "give", "get", "find", "the", "of", "is", "was", "in"}

# Create regex pattern for financial parameters
financial_parameters.sort(key=len, reverse=True)
param_pattern = r"\b(" + "|".join(map(re.escape, financial_parameters)) + r")\b"

# Function to extract company, parameter, and year with substring matching and ambiguity check
def extract_company_and_parameter(query):
    if not query.strip():
        raise ValueError("Query cannot be empty.")
    
    query_lower = query.lower()
    doc = nlp(query)
    company_name, parameter_found, year = None, None, None

    # Step 1: Extract company name with substring matching and ambiguity check
    # First, try exact match or substring match from known_companies
    potential_matches = []
    for company in known_companies:
        company_lower = company.lower()
        # Check exact match or if any query token is in the company name
        if re.search(rf"\b{re.escape(company_lower)}\b", query_lower) or \
           any(re.search(rf"\b{re.escape(token)}\b", company_lower) for token in query_lower.split() if token not in ignore_words):
            if company_lower not in ignore_words:
                potential_matches.append(company)

    # If only one match, use it; if multiple matches, set to None (will become "Unknown")
    if len(potential_matches) == 1:
        company_name = potential_matches[0]
    elif len(potential_matches) > 1:
        company_name = None  # Ambiguity detected

    # Step 2: Fallback to spaCy entity recognition with substring validation
    if not company_name:
        potential_matches = []
        for ent in doc.ents:
            if ent.label_ == "ORG" and ent.text.lower() not in ignore_words:
                ent_clean = ent.text.lower() if not ent.text.lower().endswith("'s") else ent.text.lower()[:-2]
                # Check if entity is a substring of any known company
                for company in known_companies:
                    if ent_clean in company.lower() and company.lower() not in ignore_words:
                        potential_matches.append(company)
                break
        
        # If only one match, use it; if multiple matches, set to None
        if len(potential_matches) == 1:
            company_name = potential_matches[0]
        elif len(potential_matches) > 1:
            company_name = None  # Ambiguity detected

    # Clean possessive forms in final output
    if company_name and company_name.lower().endswith("'s"):
        company_name = company_name[:-2]

    # Step 3: Extract financial parameter
    param_match = re.search(param_pattern, query_lower, re.IGNORECASE)
    if param_match:
        parameter_found = param_match.group()
        for param in financial_parameters:
            if param.lower() == parameter_found.lower():
                parameter_found = param
                break

    # Step 4: Extract year
    year_match = re.search(r"\b(19\d{2}|20\d{2})\b", query_lower)
    year = year_match.group() if year_match else "Not Specified"

    return (
        company_name if company_name and company_name.lower() not in ignore_words else "Unknown",
        parameter_found if parameter_found else "Not Specified",
        year
    )

# Streamlit UI
st.title("📊 AI-Powered Financial Analysis")
query = st.text_input("Enter your question (e.g., What was Amazon revenue in 2021?)")

if query:
    try:
        company, parameter, year = extract_company_and_parameter(query)
        st.write("**Extracted Information:**")
        st.write(f"- **Company:** {company}")
        st.write(f"- **Financial Parameter:** {parameter}")
        st.write(f"- **Year:** {year}")
    except ValueError as e:
        st.error(str(e))

