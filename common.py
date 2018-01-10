DEFAULT_YEAR = '2017'

mapping_sector = {"1": 'Fishery, Agriculture & Forestry' ,
                    "2": 'Foods',
                    "3":'Mining',
                    "4":'Oil and Coal Products',
                    "5":'Construction',
                    "6":'Metal Products',
                    "7":'Glass and Ceramics Products',
                    "8":'Textiles and Apparels',
                    "9":'Pulp and Paper',
                    "10":'Chemicals',
                    "11":'Pharmaceutical',
                    "12":'Rubber Products',
                    "13":'Transportation Equipment',
                    "14":'Iron and Steel',
                    "15":'Nonferrous Metals',
                    "16":'Machinery',
                    "17":'Electric Appliances',
                    "18":'Precision Instruments',
                    "19":'Other Products',
                    "20":'Information & Communication',
                    "21":'Services',
                    "22":'Electric Power and Gas',
                    "23":'Land Transportation',
                    "24":'Marine Transportation',
                    "25":'Air Transportation',
                    "26":'Warehousing and Harbor Transportation',
                    "27":'Wholesale Trade',
                    "28":'Retail Trade',
                    "29":'Banks',
                    "30":'Securities and Commodities Futures',
                    "31":'Insurance',
                    "32":'Other Financing Business',
                    "33":'Real Estate'
                    }
annual_kpi = [
    "jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults"
]

annual_profitability =[
    "jpcrp_cor:BasicEarningsLossPerShareIFRSSummaryOfBusinessResults"
]

annual_anagement_effectiveness = [
    "jpcrp_cor:PriceEarningsRatioUSGAAPSummaryOfBusinessResults",
    "jpcrp_cor:PriceEarningsRatioJMISSummaryOfBusinessResults"
]

annual_income = [
    "jpcrp_cor:NetSalesSummaryOfBusinessResults",
    "jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults",
    "jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults",
    "jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults",
    "jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults",
    "jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS",
    "jpcrp_cor:RevenueJMISSummaryOfBusinessResults",
    "jpcrp_cor:RevenuesUSGAAPSummaryOfBusinessResults",
    "jpcrp_cor:NetSalesSummaryOfBusinessResults",
    "jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults",
    "jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults",
    "jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults",
    "jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults",
    "jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS",
    "jpcrp_cor:InterestAndDividendIncomeSummaryOfBusinessResultsINS",
    "jpcrp_cor:InvestmentAssetsYieldIncomeYieldSummaryOfBusinessResultsINS",
    "jpcrp_cor:InvestmentYieldRealizedYieldSummaryOfBusinessResultsINS"
]

annual_balance_sheet = [
    "jpcrp_cor:NetAssetsSummaryOfBusinessResults",
    "jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults",
    "jpcrp_cor:CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults",
    "jpcrp_cor:TotalAssetsIFRSSummaryOfBusinessResults",
    "jpcrp_cor:TotalAssetsJMISSummaryOfBusinessResults",
    "jpcrp_cor:TotalAssetsSummaryOfBusinessResults",
    "jpcrp_cor:DepositsSummaryOfBusinessResults",
    "jpcrp_cor:LoansAndBillsDiscountedSummaryOfBusinessResults",
    "jpcrp_cor:SecuritiesSummaryOfBusinessResults",
    "jpcrp_cor:EquityIncludingPortionAttributableToNonControllingInterestUSGAAPSummaryOfBusinessResults"
    "jpcrp_cor:EquityAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults",
    "jpcrp_cor:TotalAssetsUSGAAPSummaryOfBusinessResults"

]

annual_cash_flow = [
    "jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults",
    "jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults",
    "jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults",
    "jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesJMISSummaryOfBusinessResults",
    "jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesJMISSummaryOfBusinessResults",
    "jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesJMISSummaryOfBusinessResults"
]

annual_dividends_and_splits = [
    "jpcrp_cor:FirstQuarterDividendPaidPerShareSummaryOfBusinessResults",
    "jpcrp_cor:SecondQuarterDividendPaidPerShareSummaryOfBusinessResults",
    "jpcrp_cor:ThirdQuarterDividendPaidPerShareSummaryOfBusinessResults",
    "jpcrp_cor:FourthQuarterDividendPaidPerShareSummaryOfBusinessResults",
    "jpcrp_cor:FifthQuarterDividendPaidPerShareSummaryOfBusinessResults",
    "jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults"
]

annual_report_tables = [
    annual_kpi,
    annual_profitability,
    annual_anagement_effectiveness,
    annual_income,
    annual_balance_sheet,
    annual_cash_flow,
    annual_dividends_and_splits
]

# ref -> https://finance.yahoo.com/quote/HMC/key-statistics?p=HMC