import spacy
from spacy.training import Example
import refine_util_function as refineutil
TRAIN_DATA = [
    # Financial Terms
    ("What was Abbott Limited India's revenue in 2024?",
     {"entities": [(31, 39, "FINANCIAL_TERM")]}),  # "revenue"
    ("What was Abbott Limited India's % Growth in EBIT 2024?",
     {"entities": [(31, 48, "FINANCIAL_TERM")]}),  # "% Growth in EBIT"

    ("Apple's % Change in Net Tangible Asset Value 2024?",
     {"entities": [(8, 44, "FINANCIAL_TERM")]}),  # "% Change in Net Tangible Asset Value"

    ("What is Tesla's Year-over-Year Revenue Growth for Q4 2024?",
     {"entities": [(16, 53, "FINANCIAL_TERM")]}),  # "Year-over-Year Revenue Growth"

    ("What was Abbott Limited India's % Change in Equity Value 2024?",
     {"entities": [(31, 56, "FINANCIAL_TERM")]}),  # "% Change in Equity Value"

    ("What was Abbott Limited India's % Change in Mcap 2024?",
     {"entities": [(31, 48, "FINANCIAL_TERM")]}),  # "% Change in Mcap"

    ("Apple's growth in NPAT 2024?",
     {"entities": [(8, 22, "FINANCIAL_TERM")]}),  # "growth in NPAT"

    ("Amazon's % Increase in Gross Profit Margin 2024?",
     {"entities": [(9, 42, "FINANCIAL_TERM")]}),  # "% Increase in Gross Profit Margin"

    ("Google's % Growth in Free Cash Flow 2023?",
     {"entities": [(9, 35, "FINANCIAL_TERM")]}),  # "% Growth in Free Cash Flow"

    ("Meta's % Change in EBITDA for Q3 2024?",
     {"entities": [(7, 25, "FINANCIAL_TERM")]}),  # "% Change in EBITDA"

    ("Apple's % Change in Market Cap in 2024?",
     {"entities": [(8, 30, "FINANCIAL_TERM")]}),  # "% Change in Market Cap"

    ("Tesla's % Change in Return on Equity 2024?",
     {"entities": [(8, 36, "FINANCIAL_TERM")]}),  # "% Change in Return on Equity"
     ("What is 10X Genomics's net margin (based on p&l) in 2024?", 
     {"entities": [(22, 48, "FINANCIAL_TERM")]}),  # "net margin (based on p&l)"

    # Organization Names
    ("What is 10X Genomics's net margin (based on p&l) in 2024?", 
     {"entities": [(8, 20, "ORG")]}),  # "10X Genomics"

    ("What is Apple's revenue in 2024?", 
     {"entities": [(8, 13, "ORG")]}),  # "Apple"

    ("Microsoft and OpenAI are collaborating on AI research.", 
     {"entities": [(0, 9, "ORG"), (14, 20, "ORG")]}),  # "Microsoft", "OpenAI"

    ("Apple Inc. announced new products at WWDC.", 
     {"entities": [(0, 10, "ORG")]}),  # "Apple Inc."

     ("Cadence Design Systems Inc reported revenue of $3.2B.", 
      {"entities": [(0, 27, "ORG"), (37, 43, "FINANCIAL_TERM")]}),

    ("Chevron Corporation's net income was $6.5B in Q4.",
      {"entities": [(0, 20, "ORG"), (22, 32, "FINANCIAL_TERM")]}),

      ( "Illumina's Market Capitalisation has increased over the last 5 years.",
      {"entities": [[0, 8, "ORG"], (11, 32, "FINANCIAL_TERM")]}),
    
    ("Incyte Corp reported a Net Profit After Tax (NPAT) of $2 billion.",
      {"entities": [[0, 11, "ORG"], (25, 53, "FINANCIAL_TERM")]}
    ),

    ("Indiamart's Revenue for the Company grew by 10% in 2024.",
      {"entities": [[0, 9, "ORG"], (12, 36, "FINANCIAL_TERM")]}),

    ("Indigo Paints recorded an Operating Cash Margin of 15%.",
      {"entities": [[0, 13, "ORG"], (29, 51, "FINANCIAL_TERM")]}),
    
    (  "Infoedge had a Total number of Shares Outstanding of 500M.",
      {"entities": [[0, 8, "ORG"], (12, 46, "FINANCIAL_TERM")]}),

    ("Infosys Technologies' Price to Earning Ratio - 10 Years Average is at an all-time high.",
      {"entities": [[0, 21, "ORG"], (24, 65, "FINANCIAL_TERM")]}),

    ("Ingersoll Rand Inc. has seen a rise in Market Capitalisation - Last 3 Years (CAGR %).",
      {"entities": [[0, 19, "ORG"], (40, 82, "FINANCIAL_TERM")]}),

    ("Intel Corporation's Net Cash generations from Investing Activities is improving.",
      {"entities": [[0, 18, "ORG"], (22, 64, "FINANCIAL_TERM")]}),

    ("Intellia announced an increase in MD Salary as % of Revenue.",
      {"entities": [[0, 8, "ORG"], (31, 59, "FINANCIAL_TERM")]}),

    ("IBM's Return on Closing Capital Employed is showing steady growth.",
      {"entities": [[0, 3, "ORG"], (6, 43, "FINANCIAL_TERM")]}),

    ("Interpublic Group of Companies Inc experienced an improvement in Working Capital Days.",
      {"entities": [[0, 37, "ORG"], (58, 79, "FINANCIAL_TERM")]}),

    ("Intuit Inc. saw a 5% growth in Price to Earning Ratio - Latest.",
      {"entities": [[0, 11, "ORG"], (34, 65, "FINANCIAL_TERM")]}),

    ("Intuitive Surgical Inc posted strong performance in Minority Interest (% of Total).",
      {"entities": [[0, 24, "ORG"], (50, 82, "FINANCIAL_TERM")]}),

    ("Invesco Ltd reported higher than expected Net Profit Margin % (W/o Exceptional Items).",
      {"entities": [[0, 11, "ORG"], (39, 87, "FINANCIAL_TERM")]}),

    ("Invitae's Total Revenue grew by 12% this quarter.",
      {"entities": [[0, 7, "ORG"], (11, 24, "FINANCIAL_TERM")]}),

    ("IPG Photonics Corp has a new restructuring plan to improve Return on Beginning Capital Employed.",
      {"entities": [[0, 19, "ORG"], (61, 97, "FINANCIAL_TERM")]}),

    ("Iqvia Holdings Inc is showing positive movement in Net Current Asset Value.",
      {"entities": [[0, 19, "ORG"], (46, 71, "FINANCIAL_TERM")]}),

    ("Iron Mountain Inc reported strong growth in Total Liabilities to Equity Ratio.",
      {"entities": [[0, 18, "ORG"], (48, 81, "FINANCIAL_TERM")]})
  ]

# Load a pretrained model
nlp = spacy.load("en_core_web_trf")
ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    {"label": "FINANCIAL_TERM", "pattern": "revenue"},
    {"label": "FINANCIAL_TERM", "pattern": "% Growth in EBIT"},
    {"label": "FINANCIAL_TERM", "pattern": "% Growth in NPAT"},
    {"label": "FINANCIAL_TERM", "pattern": "% Growth in PBT"},
    {"label": "FINANCIAL_TERM", "pattern": "% Change in Equity Value"},
    {"label": "FINANCIAL_TERM", "pattern": "% Change in Equity Value"},
    {"label": "FINANCIAL_TERM", "pattern": "% Change in Net Tangible Asset Value"},
    {"label": "FINANCIAL_TERM", "pattern": "Year-over-Year Revenue Growth"},
    {"label": "FINANCIAL_TERM", "pattern": "Net Tangible Asset Value"},
    {"label": "FINANCIAL_TERM", "pattern": "Total Liabilities to Equity Ratio"},
    {"label": "FINANCIAL_TERM", "pattern": "Net Current Asset Value"},
    {"label": "FINANCIAL_TERM", "pattern": "Return on Beginning Capital Employed"},
    {"label": "FINANCIAL_TERM", "pattern": "Total Revenue"},
    {"label": "FINANCIAL_TERM", "pattern": "Price to Earning Ratio - Latest"},
    {"label": "FINANCIAL_TERM", "pattern": "Return on Closing Capital Employed"},
    {"label": "FINANCIAL_TERM", "pattern": "Minority Interest (% of Total)"},
    {"label": "FINANCIAL_TERM", "pattern": "Net Profit Margin % (W/o Exceptional Items)"},
    {"label": "FINANCIAL_TERM", "pattern": "Market Capitalisation - Last 3 Years (CAGR %)"},
    {"label": "FINANCIAL_TERM", "pattern": " Price to Earning Ratio"},
    {"label": "FINANCIAL_TERM", "pattern": "Total number of Shares Outstanding"},
    {"label": "FINANCIAL_TERM", "pattern": "Operating Cash Margin"},
    {"label": "FINANCIAL_TERM", "pattern": "Net Profit After Tax (NPAT)"},
    {"label": "FINANCIAL_TERM", "pattern": "Market Capitalisation"},
    {"label": "FINANCIAL_TERM", "pattern": "net income"},
    {"label": "FINANCIAL_TERM", "pattern": "Gross Profit Margin"}
]

FINANCIAL_TERMs_data = refineutil.get_parameters()
FINANCIAL_TERMs = []
for parameter in FINANCIAL_TERMs_data:
    FINANCIAL_TERMs.append(parameter["item_name"].split("##")[0].lower())


financial_parameters_data = refineutil.get_parameters()
financial_parameters = []
for parameter in financial_parameters_data:
    financial_parameters.append(parameter["item_name"].split("##")[0].lower())
    patterns.append({"label":"FINANCIAL_TERM","pattern":parameter["item_name"]}) # original case
    
    patterns.append({"label":"FINANCIAL_TERM","pattern":parameter["item_name"].lower()}) #lowercase
    patterns.append({"label":"FINANCIAL_TERM","pattern":parameter["item_name"].upper()}) #uppercase
    patterns.append({"label":"FINANCIAL_TERM","pattern":parameter["item_name"].capitalize()})#first letter capital
    patterns.append({"label":"FINANCIAL_TERM","pattern":parameter["item_name"].casefold()}) #for better lowercase matching
    patterns.append({"label":"FINANCIAL_TERM","pattern":parameter["item_name"].swapcase()}) #Converts uppercase to lowercase and vice versa.
    patterns.append({"label":"FINANCIAL_TERM","pattern":parameter["item_name"].title()}) # Capitalizes the first letter of each word.
    patterns.append({"label": "FINANCIAL_TERM", "pattern": parameter["item_name"].replace(" ", "_").lower()})  # Converts spaces to underscores (_) and lowercase.
    patterns.append({"label": "FINANCIAL_TERM", "pattern": parameter["item_name"].replace(" ", "-").lower()})  # Converts spaces to hyphens (-) and lowercase.
    patterns.append({"label": "FINANCIAL_TERM", "pattern": parameter["item_name"].replace(" ", "_").upper()})  # Uppercase version of snake case.
    patterns.append({"label": "FINANCIAL_TERM", "pattern": ''.join(word.capitalize() if i != 0 else word.lower() for i, word in enumerate(parameter["item_name"].split()))})  # Removes spaces and capitalizes words except the first one.
    patterns.append({"label": "FINANCIAL_TERM", "pattern": ''.join(word.capitalize() for word in parameter["item_name"].split())})  #  Like camel case, but capitalizes the first letter too
    patterns.append({"label": "FINANCIAL_TERM", "pattern": parameter["item_name"][::-1]})  # The text is reversed character by character.

ruler.add_patterns(patterns)
# Get the NER pipeline
ner = nlp.get_pipe("ner")

# Add new entity labels
ner.add_label("FINANCIAL_TERM")
ner.add_label("ORG")

# Convert training data to spaCy format
examples = [Example.from_dict(nlp.make_doc(text), annotations) for text, annotations in TRAIN_DATA]
examples_lower = [Example.from_dict(nlp.make_doc(text.lower()), annotations) for text, annotations in TRAIN_DATA]
examples_upper = [Example.from_dict(nlp.make_doc(text.upper()), annotations) for text, annotations in TRAIN_DATA]
examples_capitalize = [Example.from_dict(nlp.make_doc(text.capitalize()), annotations) for text, annotations in TRAIN_DATA]
examples_casefold = [Example.from_dict(nlp.make_doc(text.casefold()), annotations) for text, annotations in TRAIN_DATA]
examples_swapcase = [Example.from_dict(nlp.make_doc(text.swapcase()), annotations) for text, annotations in TRAIN_DATA]
examples_title = [Example.from_dict(nlp.make_doc(text.title()), annotations) for text, annotations in TRAIN_DATA]
examples_snake_lower = [Example.from_dict(nlp.make_doc(text.replace(" ", "_").lower()), annotations) for text, annotations in TRAIN_DATA]
examples_kebab_lower = [Example.from_dict(nlp.make_doc(text.replace(" ", "-").lower()), annotations) for text, annotations in TRAIN_DATA]
examples_snake_upper = [Example.from_dict(nlp.make_doc(text.replace(" ", "_").upper()), annotations) for text, annotations in TRAIN_DATA]
examples_camel = [Example.from_dict(nlp.make_doc(''.join(word.capitalize() if i != 0 else word.lower() for i, word in enumerate(text.split()))), annotations) for text, annotations in TRAIN_DATA]
examples_pascal = [Example.from_dict(nlp.make_doc(''.join(word.capitalize() for word in text.split())), annotations) for text, annotations in TRAIN_DATA]
examples_reversed = [Example.from_dict(nlp.make_doc(text[::-1]), annotations) for text, annotations in TRAIN_DATA]

# Train model
optimizer = nlp.resume_training()
for itn in range(30):  # Increase iterations
    losses = {}
    nlp.update(examples, drop=0.2, losses=losses)  # Lower dropout
    nlp.update(examples_lower, drop=0.2, losses=losses)  # Lower dropout
    nlp.update(examples_upper, drop=0.2, losses=losses)  # Lower dropout
    nlp.update(examples_capitalize, drop=0.2, losses=losses)  # Lower dropout
    nlp.update(examples_casefold, drop=0.2, losses=losses)  # Lower dropout
    nlp.update(examples_swapcase, drop=0.2, losses=losses)
    nlp.update(examples_title, drop=0.2, losses=losses)  # Title Case
    nlp.update(examples_snake_lower, drop=0.2, losses=losses)  # Snake Case (lower)
    nlp.update(examples_kebab_lower, drop=0.2, losses=losses)  # Kebab Case (lower)
    nlp.update(examples_snake_upper, drop=0.2, losses=losses)  # Snake Case (upper)
    nlp.update(examples_camel, drop=0.2, losses=losses)  # Camel Case
    nlp.update(examples_pascal, drop=0.2, losses=losses)  # Pascal Case
    nlp.update(examples_reversed, drop=0.2, losses=losses)
    print(f"Iteration {itn}, Losses: {losses}")


# Save the fine-tuned model
nlp.to_disk("custom_financial_ner")
