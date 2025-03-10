#!/usr/local/bin/python3.9
# %%
# Connection&Fetching
import pandas as pd
from rapidfuzz import process
import sqlite3
from mysql_connect_refine import execute_query
import re
# %%

#importing all the helper function from the file
import refine_util_function
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#sys.stdout = open("print_statements_refine_util.txt", "w")

def string_to_int(value):
  '''Changes string to int/float
  Attribute{string}
  '''
  try:
    value = float(value)
  except ValueError:
    value = 0
  return value
# 📌 Initialize Database

def init_db_query():
    conn = sqlite3.connect("financial_default_queries.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            response TEXT
        )
    """)
    conn.commit()
    conn.close()

# 📌 Initialize Database
def init_db():
    conn = sqlite3.connect("financial_queries_trained.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            response TEXT
        )
    """)
    conn.commit()
    conn.close()

#  Check if Query Exists in DB
def fetch_from_db():
    conn = sqlite3.connect("financial_queries_trained.db")
    cursor = conn.cursor()
    cursor.execute("SELECT query,response FROM queries")
    result = cursor.fetchall()
    
    conn.close()
    return list(result) if list(result) else None

#  Check if Query Exists in DB
def fetch_from_db_query():
    conn = sqlite3.connect("financial_default_queries.db")
    cursor = conn.cursor()
    cursor.execute("SELECT query,response FROM queries")
    result = cursor.fetchall()
    
    conn.close()
    return list(result) if list(result) else None

#  Store Query & Response in DB
def save_to_db(query, response):
    conn = sqlite3.connect("financial_queries_trained.db")
    cursor = conn.cursor()
    #print(query)
    #print(response)
    cursor.execute("INSERT INTO queries (query, response) VALUES (?, ?)", (query, response))
    conn.commit()
    conn.close()

#  Store Query & Response in DB
def save_to_db_query(query, response):
    conn = sqlite3.connect("financial_default_queries.db")
    cursor = conn.cursor()
    #print(query)
    #print(response)
    cursor.execute("INSERT INTO queries (query, response) VALUES (?, ?)", (query, response))
    conn.commit()
    conn.close()


#find out the parameter from the calculated
def get_parameters():
    tags = ["%ChangeinEquityValue","%ChangeinMcap","%ChangeinNetTangibleAssetValue","%GrowthinEBIT","%GrowthinNPAT","%GrowthinNPAT(W/oExceptionalItems)","%GrowthinPBT","(Increase)/DecreaseinCash","(Increase)/DecreaseinOverallEquity","(Invested)/generatedfromNetWorkingAssets","0%#-0.24$$OCI-Derivatives","0%#-3.99$$Commonstockwithheldrelatedtonetsharesettlementofequityawards","0%#0.01$$OCI-Forex","0%#0.74$$OCI-AFS","0%#1.75$$ESOP-TaxBenefits","0%#2.14$$Increase/(decrease)inDebt","0%#2.59$$ChangeofAccountingPrinciple","0%#2.65$$ChangeofAccountingPrinciple","1%#-16.1$$(Increase)/DecreaseinCash","1%#-3.99$$Commonstockwithheldrelatedtonetsharesettlementofequityawards","1%#-4.43$$(Invested)/generatedfromNetWorkingAssets","1%#-5.21$$(Invested)/generatedfromNetWorkingAssets","1%#-6.67$$DebtServiceCostPaid","1%#-6.72$$OCI","1%#-7.62$$OCI","1%#-8.2$$OCI","1%#5.99$$(Increase)/DecreaseinCash","1%#8.19$$ESOP-TaxBenefits","10%#-45.1$$Dividend&DividendTaxPaid","10%#32.45$$ESOP","10%#47.54$$ESOP","11%#-162.14$$Dividend&DividendTaxPaid","11%#-73.65$$Dividend&DividendTaxPaid","12%#-137.96$$Dividend&DividendTaxPaid","12%#-180.82$$Investments/Loans&Advances","12%#-45.01$$DividendPaid","13%#-49.46$$(Increase)/DecreaseinOverallEquity","13%#-73.53$$DividendPaid","14%#-160.21$$Taxation","14%#-200.13$$Taxation","14%#-64.35$$Taxation","14%#-99.24$$Taxation","16%#-138.01$$DividendPaid","17%#-162.42$$DividendPaid","2%#-12.36$$DebtServiceCostPaid","2%#-21.89$$Investments/Loans&Advances","2%#-22.72$$DebtServiceCostPaid","2%#-23.06$$DebtServiceCostPaid","2%#-26.45$$(Increase)/DecreaseinCash","2%#-36.44$$OtherFinancingRelateditems","2%#-7.33$$OCI","2%#15.27$$Investments/Loans&Advances","3%#-18.36$$Equity","3%#-25.57$$Equity","3%#-26.23$$Equity","3%#-38.28$$OtherFinancingRelateditems","3%#-9.71$$Equity","3%#15.71$$Investments/Loans&Advances","3%#20.28$$(Increase)/DecreaseinCash","3%#33.9$$(Invested)/generatedfromNetWorkingAssets","4%#-16.02$$Increase/(decrease)inDebt","4%#-18.2$$OtherFinancingRelateditems","4%#-28.64$$OtherFinancingRelateditems","4%#56.68$$(Invested)/generatedfromNetWorkingAssets","49%#-715.62$$Increase/(decrease)inequity","5%#-49.46$$(Increase)/DecreaseinOverallEquity","57%#-652.71$$Increase/(decrease)inequity","58%#-261.9$$Increase/(decrease)inequity","6%#-49.46$$(Increase)/DecreaseinOverallEquity","61%#-418.24$$Increase/(decrease)inequity","69%#-263.08$$ShareBuyback","7%#-31.42$$NETCapex","7%#-49.81$$NETCapex","7%#85.5$$Increase/(decrease)inDebt","73%#-421.1$$ShareBuyback","74%#-659.28$$ShareBuyback","74%#-727.57$$ShareBuyback","8%#121$$Increase/(decrease)inDebt","8%#82.4$$ESOP","88%#1294.81$$OperatingCashMargin","9%#-127.83$$NETCapex","9%#-49.46$$(Increase)/DecreaseinOverallEquity","9%#-99.39$$NETCapex","9%#71.93$$ESOP","90%#1029.87$$OperatingCashMargin","90%#290.53$$NetProfitAfterTax","90%#442.63$$NetProfitAfterTax","90%#704.84$$NetProfitAfterTax","90%#882.9$$NetProfitAfterTax","95%#427.18$$OperatingCashMargin","95%#648.69$$OperatingCashMargin","AcidRatio","AdjustmentItem","AppleReturn","Borrowing","Borrowing(%ofTotal)","BorrowingstoEBITDARatio","BorrowingstoEquityRatio","CashandCashEquivalents","CashAvailabletoSatisfyFinanceProviders","CashFlowAvailabilitybeforeFinancingYield","CashFlowAvailabletoSatisfyFinanceProvidersYield","CFOSalary","CFOSalaryas%ofRevenue","ChangeofAccountingPrinciple","Commonstockwithheldrelatedtonetsharesettlementofequityawards","CompanySecretarySalary","CompanySecretarySalaryas%ofRevenue","CostofSales","CurrentassetstoCurrentliabilitiesRatio","CurrentBorrowing","CurrentBorrowing(%ofTotal)","DaysofInventory","DaysofPayable","DaysofReceivable","DebtServiceCapability(CashFlow)","DebtServiceCapability(Profit&Loss)","DebtServiceCost","DebtServiceCost(P&L)%","DebtServiceCostCoverageRatio","DebtServiceCostPaid","DebtServiceCostPaid(CashFlow)%","DebtServiceCosts","DebtServiceCosts(%ofRevenue)","DebtServiceCostsLeases","Depreciation&Amortisation","Depreciation/Amortisation-LeasesAs%ofRightofAssetUse","DepreciationandAmortisation","DepreciationandAmortisation(%ofRevenue)","Depreciationas%ofFixedAssets/Intangibles","Dividend&DividendTaxPaid","Dividend&Taxes(BasedonCashFlow)","Dividend&Taxes(BasedonEquityStatement)","DividendPaid","DividendPayoutRatio","DividendPayoutRatio(BasedonNPATw/oExceptionalItems)","DividendProposed","DividendTax","DividendYield","DowJonesReturn","EarningBeforeInterestandTax(EBIT)","EarningPerShare(Calculated)","EarningPerShare(Reported)","EarningPerShareBasedonNetProfitAfterTax(W/oExceptionalItems)(Calculated)","EarningYield-10YearsAverage##2015&&2024","EarningYield-3YearsAverage##2022&&2024","EarningYield-5YearsAverage##2020&&2024","EarningYield-AllYearsAverage##2006&&2024","EarningYield-Latest##2024","EBIT%","ebitallyear","ebitfiveyear","ebitoneyear","ebitthreeyear","Equity","Equity(%ofTotal)","EquityValue","ESOP","ESOP-TaxBenefits","Exceptionalitem","ExceptionalItems","ExcessCashMargin%","ExcessCashMargin%(W/oExceptionalItems)","Expenses","freecashfive","FreeCashFlow(2006-2024AverageBasedValuation)","FreeCashFlow(2015-2024AverageBasedValuation)","FreeCashFlow(2020-2024AverageBasedValuation)","FreeCashFlow(2022-2024AverageBasedValuation)","FreeCashFlow(2024BasedValuation)","FreeCashFlows","FreeCashFlows-AverageAllTime(CAGR%)","FreeCashFlows-Last3Years(CAGR%)","FreeCashFlows-Last5Years(CAGR%)","FreeCashFlows-LastYear(AnnualChange%)","FreeCashFlowsNotesData","FreeCashFlowstoDereiveMarketCap","freecashten","Increase/(decrease)inDebt","Increase/(decrease)inequity","Investments/Loans&Advances","Ipad","Ipad%","Ipad(%ofTotal)","Iphone","Iphone%","Iphone(%ofTotal)","Ipod","Ipod%","Ipod(%ofTotal)","Mac-Desktop","Mac-Desktop%","Mac-Desktop(%ofTotal)","Mac-Portable","Mac-Portable%","Mac-Portable(%ofTotal)","ManagingDirector(MD)Salary","marketcapallfive","marketcapallten","marketcapallyear","marketcapfive","marketcapfiveyear","MarketCapitalisation","MarketCapitalisation(Mcap)","MarketCapitalisation-AverageAllTime(CAGR%)","MarketCapitalisation-Last3Years(CAGR%)","MarketCapitalisation-Last5Years(CAGR%)","MarketCapitalisation-LastYear(AnnualChange%)","MarketCapitalisationtoEquityValue","MarketCapitalisationtoNetTangibleAssetValue","MarketCapitalisationtoRevenue","marketcaponeyear","marketcapten","marketcapthreeyear","MDSalaryas%ofRevenue","MinorityInterest","MinorityInterest(%ofTotal)","MinorityInterest/AssociateProfitandLoss","MusicRelatedProduct/Services","MusicRelatedProduct/Services%","MusicRelatedProduct/Services(%ofTotal)","NetCapex","NetCashAssetValue","NetCashgenerated/(Absorbed)beforeFinancing","NetCashgenerationfromFinancingActivities","NetCashgenerationsfromInvestingActivities","NetCashgenerationsfromOperatingActivities","NetCashintheCompany","NetCashMargin%(BasedonCashFlow)","NetCurrentAssetValue","NetIncrease/(decrease)incashandcashequivalents","NetMargin%(BasedonP&L)","NetProfitAfterTax","NetProfitAfterTax(NPAT)","NetProfitAfterTax(W/oExceptionalItems)(NPAT)","NetProfitAfterTax-AverageAllTime(CAGR%)","NetProfitAfterTax-Last3Years(CAGR%)","NetProfitAfterTax-Last5Years(CAGR%)","NetProfitAfterTax-LastYear(AnnualChange%)","NetProfitBasedPERatio","NetProfitBeforeExceptionalItemsBasedPERatio","netprofitfive","NetProfitMargin%(W/oExceptionalItems)(BasedonP&L)","netprofitten","netprofitwoexcallyear","netprofitwoexcfiveyear","netprofitwoexconeyear","netprofitwoexcthreeyear","NetTangibleAssetValue","Non-CurrentBorrowing","Non-CurrentBorrowing(%ofTotal)","NonOperatingRevenue","NonOperatingRevenue%","NonOperatingRevenue(%ofTotal)","NPAT%","NPAT(W/oExcep.Items)BasedEarningYield-10YearsAverage##2015&&2024","NPAT(W/oExcep.Items)BasedEarningYield-3YearsAverage##2022&&2024","NPAT(W/oExcep.Items)BasedEarningYield-5YearsAverage##2020&&2024","NPAT(W/oExcep.Items)BasedEarningYield-AllYearsAverage##2006&&2024","NPAT(W/oExcep.Items)BasedEarningYield-Latest##2024","NPAT(W/oExcep.Items)BasedPricetoEarningRatio-10YearsAverage##2015&&2024","NPAT(W/oExcep.Items)BasedPricetoEarningRatio-3YearsAverage##2022&&2024","NPAT(W/oExcep.Items)BasedPricetoEarningRatio-5YearsAverage##2020&&2024","NPAT(W/oExcep.Items)BasedPricetoEarningRatio-AllYearsAverage##2006&&2024","NPAT(W/oExcep.Items)BasedPricetoEarningRatio-Latest##2024","OCI","OCI-AFS","OCI-Derivatives","OCI-Forex","OperatingCashMargin","OperatingCashMargin%","OperatingCashMargin-AverageAllTime(CAGR%)","OperatingCashMargin-Last3Years(CAGR%)","OperatingCashMargin-Last5Years(CAGR%)","OperatingCashMargin-LastYear(AnnualChange%)","operatingfive","OperatingRevenue-CoreOperations","OperatingRevenue-CoreOperations%","OperatingRevenue-CoreOperations(%ofTotal)","operatingten","OtherDirectorsSalary","OtherDirectorsSalaryas%ofRevenue","OtherExpenses","OtherExpenses(%ofRevenue)","OtherFinancingRelateditems","OtherHardware","OtherHardware%","OtherHardware(%ofTotal)","Otherincome/(expense),net","Otherincome/(expense),net%","Otherincome/(expense),net(%ofTotal)","Others","Others%","Others(%ofTotal)","OthersShareholding(%ofTotal)","PERatiofor10yearTreasury","PreferenceShares","PreferenceShares(%ofTotal)","pricetoearnfive","PricetoEarningRatio-10YearsAverage##2015&&2024","PricetoEarningRatio-3YearsAverage##2022&&2024","PricetoEarningRatio-5YearsAverage##2020&&2024","PricetoEarningRatio-AllYearsAverage##2006&&2024","PricetoEarningRatio-AverageAllTime(CAGR%)","PricetoEarningRatio-Last3Years(CAGR%)","PricetoEarningRatio-Last5Years(CAGR%)","PricetoEarningRatio-LastYear(AnnualChange%)","PricetoEarningRatio-Latest##2024","pricetoearnten","pricetoearnwoallyear","pricetoearnwofive","pricetoearnwofiveyear","pricetoearnwooneyear","pricetoearnwoten","pricetoearnwothreeyear","ProfitBeforeTax(PBT)","profitbeforetaxallyear","profitbeforetaxfiveyear","profitbeforetaxoneyear","profitbeforetaxthreeyear","PromoterShareholding(%ofTotal)","RatioofNetCapextoDepreciation&Amortisation","Restructuring","Restructuring(%ofRevenue)","RetainedEarningProgression","RetainedEarningProgressionNotesData","ReturnonBeginningCapitalEmployed","ReturnonBeginningCapitalEmployed(BasedonNPATw/oExceptionalItems)","ReturnonBeginningEquity","ReturnonBeginningEquity(BasedonNPATw/oExceptionalItems)","ReturnonClosingCapitalEmployed","ReturnonClosingCapitalEmployed(BasedonNPATw/oExceptionalItems)","ReturnonClosingEquity","ReturnonClosingEquity(BasedonNPATw/oExceptionalItems)","ReturnonNetTangibleAssets","ReturnonNetTangibleAssets(BasedonNPATw/oExceptionalItems)","ReturnonNetTangibleCapitalEmployed","ReturnonNetTangibleCapitalEmployed(BasedonNPATw/oExceptionalItems)","Revenue%Growth","Revenue-AverageAllTime(CAGR%)","Revenue-Last3Years(CAGR%)","Revenue-Last5Years(CAGR%)","Revenue-LastYear(AnnualChange%)","revenuefive","RevenuefortheCompany","RevenuefortheCompany%","RevenuefortheCompany(%ofTotal)","Revenuesofthecompany","Revenuesofthecompany%","Revenuesofthecompany(%ofTotal)","revenueten","RND","RND(%ofRevenue)","sensaxallallyear","sensaxallfive","sensaxallfiveyear","sensaxalloneyear","sensaxallten","sensaxallthreeyear","sensaxallyear","sensaxfive","sensaxfiveyear","sensaxoneyear","sensaxten","sensaxthreeyear","sensaxyearonyearchangepercentage","SGA","SGA(%ofRevenue)","ShareBuyback","Software/Services","Software/Services%","Software/Services(%ofTotal)","Stockoptionsas%ofOutstandingShares","TaxAssets","Taxation","TaxationExpense","TaxesAccruedinP&L(As%ofProfitBeforeTax)","TaxesPaidinCashFlow(As%ofProfitBeforeTax)","TaxLiabilities","TotalChangeinFinancing","TotalLiabilitiestoEquityRatio","TotalnumberofSharesOutstanding","TotalnumberofSharesOutstanding%growth","TotalRevenue","Un-ExplainedItem","WorkingCapitalDays","Yield%of10YearTreasury"]
    #tags = ["TotalRevenue","NetProfitAfterTax","NetProfitBasedPERatio","MarketCapitalisation(Mcap)","OperatingCashMargin","FreeCashFlows","EquityValue","NetTangibleAssetValue","TotalNumberofSharesOutstanding","NetCashAssetValue","Borrowing","MinorityInterest","TotalLiabilitiestoEquityRatio","CashandCashEquivalents","NetCashintheCompany","DebtServiceCostCoverageRatio","DaysofReceivable","DaysofPayable","DaysofInventory","WorkingCapitalDays","NetCapex","Depreciation&Amortisation","RatioofNetCapextoDepreciation&Amortisation","Depreciationas%ofFixedAssets/Intangibles","CurrentassetstoCurrentliabilitiesRatio","AcidTestRatio","ProfitBeforeTax","TaxAccruedinP&L(As%ofProfitBeforeTax)","TaxesPaidinCashFlow(As%ofProfitBeforeTax)","TaxAssets","TaxLiabilities","NetCashMargin%(BasedonCashFlow)","NetMargin%(BasedonP&L)","ExcessCashMargin%","EarningPerShare(Reported)","EarningPerShare(Calculated)","DividendYield","DividendPayoutRatio","ReturnonBeginningEquity","ReturnonNetTangibleAssets","ReturnonBeginningCapitalEmployed","ReturnonNetTangibleCapitalEmployed","PricetoEarningRatio-Latest","PricetoEarningRatio-3YearsAverage","PricetoEarningRatio-5YearsAverage","PricetoEarningRatio-10YearsAverage","PricetoEarningRatio-AllYearsAverage","EarningYield-Latest","EarningYield-3YearsAverage","EarningYield-5YearsAverage","EarningYield-10YearsAverage","EarningYield-AllYearsAverage","PricetoBookValue","PricetoSalesValue","TotalnumberofSharesOutstanding%growth","Revenue-LastYear(AnnualChange%)","Revenue-Last3Years(CAGR%)","Revenue-Last5Years(CAGR%)","Revenue-AverageAllTime(CAGR%)","NetProfitAfterTax-LastYear(AnnualChange%)","NetProfitAfterTax-Last3Years(CAGR%)","NetProfitAfterTax-Last5Years(CAGR%)","NetProfitAfterTax-AverageAllTime(CAGR%)","OperatingCashMargin-LastYear(AnnualChange%)","OperatingCashMargin-Last3Years(CAGR%)","OperatingCashMargin-Last5Years(CAGR%)","OperatingCashMargin-AverageAllTime(CAGR%)","FreeCashFlows-LastYear(AnnualChange%)","FreeCashFlows-Last3Years(CAGR%)","FreeCashFlows-Last5Years(CAGR%)","FreeCashFlows-AverageAllTime(CAGR%)","MarketCapitalisation-LastYear(AnnualChange%)","MarketCapitalisation-Last3Years(CAGR%)","MarketCapitalisation-Last5Years(CAGR%)","MarketCapitalisation-AverageAllTime(CAGR%)","PricetoEarningRatio-LastYear(AnnualChange%)","PricetoEarningRatio-Last3Years(CAGR%)","PricetoEarningRatio-Last5Years(CAGR%)","PricetoEarningRatio-AverageAllTime(CAGR%)","Revenue%Growth","%GrowthinPBT","%GrowthinNPAT","EarningBeforeInterestandTax(EBIT)","%GrowthinEBIT","EBIT%","NPAT%","NetProfitAfterTax(NPAT)","ReturnonClosingCapitalEmployed","BorrowingstoEquityRatio"]
    # Prepare SQL query with placeholders
    query = "SELECT tag, item_name FROM refine_companies_calculated_data where tag IN ({}) group by tag,item_name".format(','.join(['%s'] * len(tags)))
    #refine.cursor.execute(query,tags)
    parameters = execute_query(query,tags)
    # Convert to a dictionary (removing duplicates)
    unique_dict = dict(parameters)

    # Convert to a list of unique keys
    unique_keys = list(unique_dict.keys())

    # Convert to a list of unique values
    unique_values = list(unique_dict.values())
    #print(parameters)
    return list(parameters)

#find out the parameter from the calculated
def get_companies():
    # Prepare SQL query with placeholders
    query = "SELECT company_name,company_id FROM refine_companies_calculated_data group by company_name"
    #refine.cursor.execute(query)
    companies = execute_query(query)
    # Convert to a dictionary (removing duplicates)
    unique_dict = list(companies)

    # Convert to a list of unique keys
    #unique_keys = list(unique_dict.keys())

    # Convert to a list of unique values
    #unique_values = list(unique_dict.values())
    return unique_dict

def getCompanyData(company,parameter,year):
    tags = []
    tags = [parameter]
    print("----------------------")
    print (company)
    print (parameter)
    print (year)
    print("+++++++++++++++++++")
    if(year != None and year != 'Not Specified'):
      query = "SELECT year,fiscal_period,item_name,value,actual_value,INR_value,USD_value,unit_currency FROM refine_companies_calculated_data where fiscal_period='FY' AND financial_type='consolidated' AND company_id=%s AND year=%s AND tag IN ({})".format(','.join(['%s'] * len(tags)))
      data = execute_query(query,(company,year,tags))
    else:
      query = "SELECT year,fiscal_period,item_name,value,actual_value,INR_value,USD_value,unit_currency FROM refine_companies_calculated_data where fiscal_period='FY' AND financial_type='consolidated' AND company_id=%s AND tag IN ({})".format(','.join(['%s'] * len(tags)))
      #print(query)
      #print(tags)
      data = execute_query(query,(company,tags))

    #data = refine.cursor.fetchall()
    
    return list(data)

def getObjectValue(data, key_to_find):
    for obj in data:
      if key_to_find in obj["company_name"]:
        #print(obj)
        return obj

def getObjectValueParameter(data, key_to_find):
    keywordsparm = ""
    #print(key_to_find)
    match key_to_find:
      case _ if key_to_find.lower() in ["revenue", "sales", "turnover"]:
          keywordsparm = "Total Revenue"
      case _ if key_to_find.lower() in ["price to earning", "price to earning ratio", "pe ratio"]:
          keywordsparm = "Net Profit Based PE Ratio"
      case _ if key_to_find.lower() in ["price to earning", "price to earning ratio", "pe ratio"]:
          keywordsparm = "Net Profit Before Exceptional Items Based PE Ratio"
      case _:
          keywordsparm =  key_to_find.lower()
    print(keywordsparm)
    cleaned_data = ""
    for obj in data:
      #print(obj["item_name"].lower().strip())
      #if re.search(rf"\b{re.escape(keywordsparm.lower().strip())}\b", obj["item_name"].lower().strip()):
      if keywordsparm.lower().strip() == obj["item_name"].lower().strip():
          match = obj["tag"]
          cleaned_data = match.replace(" ", "")
          break
    if not cleaned_data:
      for obj in data:  
        if keywordsparm.lower() in obj["item_name"].lower():
          match = obj["tag"]
          cleaned_data = match.replace(" ", "")
          break
    return cleaned_data
  #para = [item["item_name"] for item in data]
  #print(para)
  #match, score, _ = process.extractOne(key_to_find, para)
  # Remove spaces from keys
  
  
  #if score > 75:  # Set similarity threshold
  #matched_keywords[kw] = match

