import spacy
import re
import streamlit as st

#need to handle the exception when 'en_core_web_sm' (not able to lead spaCy NLP model) not installed
try:  
    nlp = spacy.load("en_core_web_sm")
except OSError:   
    st.error("Error: spaCy model not found. Run `python -m spacy download en_core_web_sm`.")
    st.stop()

# Ignore common non-company words at the start
ignore_words = {"check", "tell", "show", "what", "give", "get", "find"}

# Multi-word and single-word financial terms
financial_parameters = [  "stock price", "market cap", "net income", "cash flow",
    "dividends", "earnings per share", "return on equity",
    "return on capital employed", "operating income", "revenue", "profit", "assets"
    ]

# Convert multi-word parameters into a set of individual words for easier detection
financial_keywords = {word for phrase in financial_parameters for word in phrase.split()}

# Manually defined company names (to handle missing spaCy cases)
known_companies = ["Amazon", "Apple", "Tesla", "Microsoft", "Google", "Meta", "Netflix"]

def extract_company_and_parameter(query):
    # handling the null values of query 
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    doc = nlp(query.lower()) # Convert to lowercase for better matching
    company_name , parameter_found, year = None, None, None

    for ent in doc.ents:
        if ent.label_ in ["ORG", "GPE", "PERSON"]:
            company_name = ent.text.title()   # Title case for proper formatting
            break

# Handle possessive forms ("Tesla's" → "Tesla")
    if company_name and company_name.endswith("'s"):
        company_name = company_name[:-2]

 # Ensure company name is not a common ignored word
    if company_name in ignore_words:
        company_name = None

# Fallback: Check manually if a known company exists in the query
    if not company_name:
        for company in known_companies:
            if re.search(rf"\b{company}\b", query, re.IGNORECASE): # Match whole word
                company_name = company
                break

 # Extract financial parameter (match multi-word phrases first)
    for phrase in financial_parameters:
        if phrase in query.lower():
            parameter_found = phrase
            break

     # If no multi-word phrase was found, check single-word financial terms
    if not parameter_found:
        for token in doc:
            if token.text.lower() in financial_keywords:
                parameter_found = token.text.lower()
                break

#Handling the exception for specify the  year 
    try:
        # Extract year using regex (looking for 4-digit numbers from 1900-2099)
        match = re.search(r"\b(19\d{2}|20\d{2})\b", query)
        year = match.group() if match else "Not Specified"
    except re.error:
        year = "Regex Error"

    return company_name or "Unknown", parameter_found or "Not Specified", year

# User interface definition
st.title("📊 AI-Powered Financial Analysis")

query = st.text_input("Enter your question: (e.g., What was Apple's revenue in 2021?)")

if query:
    #handling potential query occur during calling extract_company_and_parameter
    try:
        company, parameter, year = extract_company_and_parameter(query)
        st.write(f"**Company:** {company}")
        st.write(f"**Financial Parameter:** {parameter}")
        st.write(f"**Year:** {year}")
    except ValueError as e:
        st.error(str(e))
