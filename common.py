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
annual_kpi = {
    "jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults":"Net assets per share",
    "jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults":"Equity-to-asset ratio",
    "jpcrp_cor:EquityToAssetRatioUSGAAPSummaryOfBusinessResults":"Equity-to-asset ratio",
    "jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults":"Rate of return on equity",
    "jpcrp_cor:RateOfReturnOnEquityIFRSSummaryOfBusinessResults":"Rate of return on equity",
    "jpcrp_cor:RateOfReturnOnEquityJMISSummaryOfBusinessResults":"Rate of return on equity",
    "jpcrp_cor:RateOfReturnOnEquityUSGAAPSummaryOfBusinessResults":"Rate of return on equity",
    "jpcrp_cor:PriceEarningsRatioIFRSSummaryOfBusinessResults": "Price-earnings ratio",
    "jpcrp_cor:PriceEarningsRatioUSGAAPSummaryOfBusinessResults": "Price-earnings ratio",
    "jpcrp_cor:PriceEarningsRatioJMISSummaryOfBusinessResults": "Price-earnings ratio",
    "jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults": "Price-earnings ratio",
    "jpcrp_cor:BasicEarningsLossPerShareIFRSSummaryOfBusinessResults": "Basic earnings (loss) per share",
    "jpcrp_cor:BasicEarningsLossPerShareJMISSummaryOfBusinessResults": "Basic earnings (loss) per share",
    "jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults": "Basic earnings (loss) per share"

}

quarter_kpi = {
    "jpcrp_cor:NetAssetsPerShareSummaryOfBusinessResults":"Net assets per share",
    "jpcrp_cor:EquityToAssetRatioSummaryOfBusinessResults":"Equity-to-asset ratio",
    "jpcrp_cor:EquityToAssetRatioUSGAAPSummaryOfBusinessResults":"Equity-to-asset ratio",
    "jpcrp_cor:RateOfReturnOnEquitySummaryOfBusinessResults":"Rate of return on equity",
    "jpcrp_cor:RateOfReturnOnEquityIFRSSummaryOfBusinessResults":"Rate of return on equity",
    "jpcrp_cor:RateOfReturnOnEquityJMISSummaryOfBusinessResults":"Rate of return on equity",
    "jpcrp_cor:RateOfReturnOnEquityUSGAAPSummaryOfBusinessResults":"Rate of return on equity",
    "jpcrp_cor:PriceEarningsRatioIFRSSummaryOfBusinessResults": "Price-earnings ratio",
    "jpcrp_cor:PriceEarningsRatioJMISSummaryOfBusinessResults": "Price-earnings ratio",
    "jpcrp_cor:PriceEarningsRatioUSGAAPSummaryOfBusinessResults": "Price-earnings ratio",
    "jpcrp_cor:PriceEarningsRatioSummaryOfBusinessResults": "Price-earnings ratio",
    "jpcrp_cor:BasicEarningsLossPerShareIFRSSummaryOfBusinessResults": "Basic earnings (loss) per share",
    "jpcrp_cor:BasicEarningsLossPerShareJMISSummaryOfBusinessResults": "Basic earnings (loss) per share",
    "jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults": "Basic earnings (loss) per share"

}


annual_income = {
    "jpcrp_cor:NetSalesSummaryOfBusinessResults": "Net sales",
    "jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults": "Operating revenue",
    "jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults": "Operating revenue",
    "jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults": "Gross operating revenue",
    "jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults": "Ordinary income",
    "jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS": "Net premiums written",
    "jpcrp_cor:RevenueJMISSummaryOfBusinessResults": "Revenue",
    "jpcrp_cor:RevenuesUSGAAPSummaryOfBusinessResults": "Revenues",
    "jpcrp_cor:InterestAndDividendIncomeSummaryOfBusinessResultsINS": "Interest and dividend income",
    "jpcrp_cor:InvestmentAssetsYieldIncomeYieldSummaryOfBusinessResultsINS": "Investment assets yield (income yield)",
    "jpcrp_cor:InvestmentYieldRealizedYieldSummaryOfBusinessResultsINS":"Investment yield (realized yield)"
}

quarter_income = {
    "jpcrp_cor:NetSalesSummaryOfBusinessResults": "Net sales",
    "jpcrp_cor:OperatingRevenue1SummaryOfBusinessResults": "Operating revenue",
    "jpcrp_cor:OperatingRevenue2SummaryOfBusinessResults": "Operating revenue",
    "jpcrp_cor:GrossOperatingRevenueSummaryOfBusinessResults": "Gross operating revenue",
    "jpcrp_cor:OrdinaryIncomeSummaryOfBusinessResults": "Ordinary income",
    "jpcrp_cor:NetPremiumsWrittenSummaryOfBusinessResultsINS": "Net premiums written",
    "jpcrp_cor:RevenueJMISSummaryOfBusinessResults": "Revenue",
    "jpcrp_cor:RevenuesUSGAAPSummaryOfBusinessResults": "Revenues",
    "jpcrp_cor:InterestAndDividendIncomeSummaryOfBusinessResultsINS": "Interest and dividend income",
    "jpcrp_cor:InvestmentAssetsYieldIncomeYieldSummaryOfBusinessResultsINS": "Investment assets yield (income yield)",
    "jpcrp_cor:InvestmentYieldRealizedYieldSummaryOfBusinessResultsINS":"Investment yield (realized yield)"
}


annual_balance_sheet = {
    "jpcrp_cor:NetAssetsSummaryOfBusinessResults":"Net assets",
    "jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults":"Cash and cash equivalents",
    "jpcrp_cor:CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults":"Cash and cash equivalents",
    "jpcrp_cor:TotalAssetsIFRSSummaryOfBusinessResults":"Total assets",
    "jpcrp_cor:TotalAssetsJMISSummaryOfBusinessResults":"Total assets",
    "jpcrp_cor:TotalAssetsSummaryOfBusinessResults":"Total assets",
    "jpcrp_cor:DepositsSummaryOfBusinessResults":"Deposits",
    "jpcrp_cor:LoansAndBillsDiscountedSummaryOfBusinessResults":"Loans and bills discounted",
    "jpcrp_cor:SecuritiesSummaryOfBusinessResults":"Securities",
    "jpcrp_cor:EquityIncludingPortionAttributableToNonControllingInterestUSGAAPSummaryOfBusinessResults":"Equity including portion attributable to non-controlling interest",
    "jpcrp_cor:EquityAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults":"Equity attributable to owners of parent",
    "jpcrp_cor:TotalAssetsUSGAAPSummaryOfBusinessResults":"Total assets"
}

quarter_balance_sheet = {
    "jpcrp_cor:NetAssetsSummaryOfBusinessResults":"Net assets",
    "jpcrp_cor:CashAndCashEquivalentsSummaryOfBusinessResults":"Cash and cash equivalents",
    "jpcrp_cor:CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults":"Cash and cash equivalents",
    "jpcrp_cor:TotalAssetsIFRSSummaryOfBusinessResults":"Total assets",
    "jpcrp_cor:TotalAssetsJMISSummaryOfBusinessResults":"Total assets",
    "jpcrp_cor:TotalAssetsSummaryOfBusinessResults":"Total assets",
    "jpcrp_cor:DepositsSummaryOfBusinessResults":"Deposits",
    "jpcrp_cor:LoansAndBillsDiscountedSummaryOfBusinessResults":"Loans and bills discounted",
    "jpcrp_cor:SecuritiesSummaryOfBusinessResults":"Securities",
    "jpcrp_cor:EquityIncludingPortionAttributableToNonControllingInterestUSGAAPSummaryOfBusinessResults":"Equity including portion attributable to non-controlling interest",
    "jpcrp_cor:EquityAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults":"Equity attributable to owners of parent",
    "jpcrp_cor:TotalAssetsUSGAAPSummaryOfBusinessResults":"Total assets"
}



annual_cash_flow = {
    "jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults":"Net cash provided by (used in) operating activities",
    "jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults":"Net cash provided by (used in) investing activities",
    "jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults":"Net cash provided by (used in) financing activities",
    "jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesJMISSummaryOfBusinessResults":"Cash flows from (used in) operating activities",
    "jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesJMISSummaryOfBusinessResults":"Cash flows from (used in) investing activities",
    "jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesJMISSummaryOfBusinessResults":"Cash flows from (used in) financing activities",
    "jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesUSGAAPSummaryOfBusinessResults":"Cash flows from (used in) operating activities",
    "jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesUSGAAPSummaryOfBusinessResults":"Cash flows from (used in) investing activities",
    "jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesUSGAAPSummaryOfBusinessResults":"Cash flows from (used in) financing activities"

}

quarter_cash_flow = {
    "jpcrp_cor:NetCashProvidedByUsedInOperatingActivitiesSummaryOfBusinessResults":"Net cash provided by (used in) operating activities",
    "jpcrp_cor:NetCashProvidedByUsedInInvestingActivitiesSummaryOfBusinessResults":"Net cash provided by (used in) investing activities",
    "jpcrp_cor:NetCashProvidedByUsedInFinancingActivitiesSummaryOfBusinessResults":"Net cash provided by (used in) financing activities",
    "jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesJMISSummaryOfBusinessResults":"Cash flows from (used in) operating activities",
    "jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesJMISSummaryOfBusinessResults":"Cash flows from (used in) investing activities",
    "jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesJMISSummaryOfBusinessResults":"Cash flows from (used in) financing activities",
    "jpcrp_cor:CashFlowsFromUsedInOperatingActivitiesUSGAAPSummaryOfBusinessResults":"Cash flows from (used in) operating activities",
    "jpcrp_cor:CashFlowsFromUsedInInvestingActivitiesUSGAAPSummaryOfBusinessResults":"Cash flows from (used in) investing activities",
    "jpcrp_cor:CashFlowsFromUsedInFinancingActivitiesUSGAAPSummaryOfBusinessResults":"Cash flows from (used in) financing activities"
}

annual_dividends_and_splits = {
    "jpcrp_cor:FirstQuarterDividendPaidPerShareSummaryOfBusinessResults":"First quarter dividend paid per share",
    "jpcrp_cor:SecondQuarterDividendPaidPerShareSummaryOfBusinessResults":"Second quarter dividend paid per share",
    "jpcrp_cor:ThirdQuarterDividendPaidPerShareSummaryOfBusinessResults":"Third quarter dividend paid per share",
    "jpcrp_cor:FourthQuarterDividendPaidPerShareSummaryOfBusinessResults":"Fourth quarter dividend paid per share",
    "jpcrp_cor:FifthQuarterDividendPaidPerShareSummaryOfBusinessResults":"Fifth quarter dividend paid per share",
    "jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults":"Basic earnings (loss) per share",
}

quarter_dividends_and_splits = {
    "jpcrp_cor:FirstQuarterDividendPaidPerShareSummaryOfBusinessResults":"First quarter dividend paid per share",
    "jpcrp_cor:SecondQuarterDividendPaidPerShareSummaryOfBusinessResults":"Second quarter dividend paid per share",
    "jpcrp_cor:ThirdQuarterDividendPaidPerShareSummaryOfBusinessResults":"Third quarter dividend paid per share",
    "jpcrp_cor:FourthQuarterDividendPaidPerShareSummaryOfBusinessResults":"Fourth quarter dividend paid per share",
    "jpcrp_cor:FifthQuarterDividendPaidPerShareSummaryOfBusinessResults":"Fifth quarter dividend paid per share",
    "jpcrp_cor:BasicEarningsLossPerShareSummaryOfBusinessResults":"Basic earnings (loss) per share",
}

annual_report_list = [
    ["KPI",annual_kpi],
    ["income",annual_income],
    ["Balance Sheet",annual_balance_sheet],
    ["Cash Flow", annual_cash_flow],
    ["Dividends and Splits", annual_dividends_and_splits]
]



quarter_report_list = [
    ["KPI",quarter_kpi],
    ["income",quarter_income],
    ["Balance Sheet",quarter_balance_sheet],
    ["Cash Flow", quarter_cash_flow],
    ["Dividends and Splits", quarter_dividends_and_splits]]

# ref -> https://finance.yahoo.com/quote/HMC/key-statistics?p=HMC