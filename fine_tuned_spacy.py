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
]

financial_parameters_data = refineutil.get_parameters()
financial_parameters = []
for parameter in financial_parameters_data:
    financial_parameters.append(parameter["item_name"].split("##")[0].lower())
    patterns.append({"label":"FINANCIAL_TERM","pattern":parameter["item_name"]})
    patterns.append({"label":"FINANCIAL_TERM","pattern":parameter["item_name"].lower()})
    patterns.append({"label":"FINANCIAL_TERM","pattern":parameter["item_name"].upper()})
    patterns.append({"label":"FINANCIAL_TERM","pattern":parameter["item_name"].capitalize()})
    patterns.append({"label":"FINANCIAL_TERM","pattern":parameter["item_name"].casefold()})
    patterns.append({"label":"FINANCIAL_TERM","pattern":parameter["item_name"].swapcase()})

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

# Train model
optimizer = nlp.resume_training()
for itn in range(30):  # Increase iterations
    losses = {}
    nlp.update(examples, drop=0.2, losses=losses)  # Lower dropout
    nlp.update(examples_lower, drop=0.2, losses=losses)  # Lower dropout
    nlp.update(examples_upper, drop=0.2, losses=losses)  # Lower dropout
    nlp.update(examples_capitalize, drop=0.2, losses=losses)  # Lower dropout
    nlp.update(examples_casefold, drop=0.2, losses=losses)  # Lower dropout
    nlp.update(examples_swapcase, drop=0.2, losses=losses)  # Lower dropout
    print(f"Iteration {itn}, Losses: {losses}")


# Save the fine-tuned model
nlp.to_disk("custom_financial_ner")
