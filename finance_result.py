import spacy
import re
import streamlit as st
import pandas as pd
import refine_util_function as refineutil
import sqlite3
from spacy.pipeline import EntityRuler

#need to handle the exception when 'en_core_web_sm' (not able to lead spaCy NLP model) not installed
try:  
    nlp = spacy.load("en_core_web_trf")
    # Add custom entity recognition rule
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [{"label": "ORG", "pattern": "10X Genomics"},  # Ensure proper company recognition
            {"label": "FINANCIAL_TERM", "pattern": "NPAT"},
            {"label": "FINANCIAL_TERM", "pattern": "% growth in NPAT"},
            {"label": "FINANCIAL_TERM", "pattern": [{"TEXT": "%"}, {"LOWER": "growth"}, {"LOWER": "in"}, {"LOWER": "npat"}]},
            {"label": "FINANCIAL_TERM", "pattern": " % Change in Net Tangible Asset Value"},
            {"label": "FINANCIAL_TERM", "pattern": [{"TEXT": "%"}, {"LOWER": "change"}, {"LOWER": "in"}, 
                                            {"LOWER": "net"}, {"LOWER": "tangible"}, 
                                            {"LOWER": "asset"}, {"LOWER": "value"}]},
            {"label": "FINANCIAL_TERM", "pattern": "% Growth in EBIT"},
            {"label": "FINANCIAL_TERM", "pattern": [{"TEXT": "%"}, {"LOWER": "growth"}, {"LOWER": "in"}, {"LOWER": "ebit"}]},
            {"label": "FINANCIAL_TERM", "pattern": "% Growth in PBT"},
            {"label": "FINANCIAL_TERM", "pattern": [{"TEXT": "%"}, {"LOWER": "growth"}, {"LOWER": "in"}, {"LOWER": "pbt"}]},
            {"label": "FINANCIAL_TERM", "pattern": "npat"}]  # Tag NPAT correctly
    ruler.add_patterns(patterns)
except OSError:   
    st.error("Error: spaCy model not found. Run `python -m spacy download en_core_web_sm`.")
    st.stop()

#Loading the excel file for the company name 
def load_companies_from_excel(file_path="Known_Companies_List.xlsx"):
    try:
        df = pd.read_excel(file_path)

        # Ensure the required column exists
        if "Company Id" in df.columns and "Company Name" in df.columns:
            #mapping the company id and company name together 
            #return {row["Company Name"]: row ["Company Id"] for _, row in df.iterrows()}
            return {row["Company Name"].split(" ")[0]: row ["Company Id"] for _, row in df.iterrows()}
            #return df["Company Name"].dropna().astype(str).tolist()
        else:
            st.error("Error: 'Company Name' column not found in the Excel file.")
            return []
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return []
    
    #loading companies for excel file 
companies_list = refineutil.get_companies()
#print(companies_list)
known_companies = list(load_companies_from_excel().keys())

# Ignore common non-company words at the start
ignore_words = {"check", "tell", "show", "what", "give", "get", "find", "the","in","and"}

# Load financial parameters from Excel file
def load_financial_parameters(file_path="Parameters.xlsx"):
    try:
        df = pd.read_excel(file_path, usecols=["Item Name(Parameters)"])
        return df["Item Name(Parameters)"].dropna().tolist()
    except Exception as e:
        st.error(f"Error loading financial parameters: {e}")
        return []

financial_parameters_data = refineutil.get_parameters()
financial_parameters = []
for parameter in financial_parameters_data:
    financial_parameters.append(parameter["item_name"].split("##")[0].lower())
#print(financial_parameters)

# Sort financial parameters by length in descending order (to match longer phrases first)
#financial_parameters.sort(key=len, reverse=False)

# Convert multi-word parameters into a set of individual words for easier detection
financial_keywords = {word for phrase in financial_parameters for word in phrase.split()}

# Manually defined company names (to handle missing spaCy cases)
# known_companies = ["Amazon", "Apple", "Tesla", "Microsoft", "Google", "Meta", "Netflix"]

def extract_company_and_parameter(query):
    # handling the null values of query 
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    doc = nlp(query.lower()) # Convert to lowercase for better matching
    company_name , parameter_found, year = None, None, None
    #print(doc)
    for ent in doc.ents:
        #print(ent)
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
          #  if re.search(rf"\b{company}\b", query, re.IGNORECASE): # Match whole word
             if re.search(rf"\b{re.escape(company)}\b", query, re.IGNORECASE):
                company_name = company
                break
# Extract financial parameter (match multi-word phrases first)
    for token in doc.ents:
        print(token)
        for phrase in financial_parameters:
            if re.search(rf"\b{re.escape(phrase.lower())}\b", token.text.lower()):
                parameter_found = token.text.lower()
                break
    if not parameter_found:
        # Extract financial parameter (match multi-word phrases first)
        for phrase in financial_parameters:
            #print(phrase)
            if re.search(rf"\b{re.escape(phrase.lower())}\b", query.lower()):
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
refineutil.init_db()
# Display past queries
st.sidebar.subheader("📌 Past Queries")
past_queries = refineutil.fetch_from_db()

if past_queries:
    unique_queries = list({query[0]: query for query in past_queries}.values())
    for query in unique_queries:
        st.sidebar.write(f"Query: {query[0]}")
        st.sidebar.write(f"Response: {query[1]}")
        st.sidebar.write(f"-----------------------------------")
else:
    st.sidebar.write("No past queries found.")


query = st.text_input("Enter your question: (e.g., What was Apple's revenue in 2021?)")

if query:
    #handling potential query occur during calling extract_company_and_parameter
    try:
        company, parameter, year = extract_company_and_parameter(query)
        #print(companies_list)
        parameter_list = refineutil.get_parameters()
        #print(parameter_list)
        parameter_tag = refineutil.getObjectValueParameter(financial_parameters_data,parameter)

        companyid = refineutil.getObjectValue(companies_list,company)
        if(companyid['company_id']):
            data = refineutil.getCompanyData(companyid['company_id'],parameter_tag,year)
        st.write(f"**Company:** {company}")
        st.write(f"**Financial Parameter:** {parameter}")
        st.write(f"**Year:** {year}")

        st.write(f"**Query:** {query}")
        responsedata = "Company Name : "+ company + "\n  Parameter : " + parameter + "\n Year : "+year
        refineutil.save_to_db(query, responsedata)


        # Create DataFrame
        df = pd.DataFrame(data)
        print(data)
        #print(df.columns.tolist())  # Get exact column names
        #df = df.reset_index(drop=True)
        if(len(data) > 0):
            df = df.set_index("year")
            df.rename(columns={"year": "Year", "fiscal_period": "Fiscal Period","item_name": "Item Name","value": "Value","actual_value": "Actual Value","INR_value": "INR Value","USD_value": "USD Value","unit_currency":"Currency"}, inplace=True)
            st.write(df)
        else:
            st.write("Data not found for the query")
        # Display as a table
        #print(df.head())  # Check actual column names
        
        #st.table(df)
       
    except ValueError as e:
        st.error(str(e))





