

import re
from pdfminer.high_level import extract_text
from PyPDF2 import PdfReader
import pdfplumber

file = '11_milestone\Schroder\Schroder PDFs\Schroder Blended Portfolio 5.pdf'
text = ''
with pdfplumber.open(file) as pdf:
    first_line_found = False
    for page in pdf.pages:
        text = page.extract_text()
        text = text.split('\n')
        # print(text)

    # data = ['Risk considerations Synthetic risk & reward indicator (SRRI)', 'Counterparty risk: The fund may have contractual agreements with counterparties. If a LOWER RISK HIGHER RISK', 'counterparty is unable to fulfil their obligations, the sum that they owe to the fund may be Potentially lower reward Potentially higher reward', 'lost in part or in whole.', 'Credit risk: A decline in the financial health of an issuer could cause the value of its bonds to', '1 2 3 4 5 6 7', 'fall or become worthless.', 'Currency risk: The fund may lose value as a result of movements in foreign exchange rates, The risk category was calculated using historical', 'otherwise known as currency rates. performance data and may not be a reliable', 'High yield bond risk: High yield bonds (normally lower rated or unrated) generally carry indicator of the fund’s future risk profile. The', 'greater market, credit and liquidity risk meaning greater uncertainty of returns. fund’s risk category is not guaranteed to remain', 'IBOR risk: The transition of the financial markets away from the use of interbank offered fixed. Please see the Key Investor Information', 'rates (IBORs) to alternative reference interest rates may impact the valuation of certain Document for more information.', 'holdings and disrupt liquidity in certain instruments. This may impact the investment', 'Risk Rating', 'performance of the fund.', 'Liquidity risk: In difficult market conditions, the fund may not be able to sell a security for full', 'value or at all. This could affect performance and could cause the fund to defer or suspend 1 2 3 4 5 6 7 8 9 10',
    #         'redemptions of its shares, meaning investors may not be able to have immediate access to', 'their holdings.', 'Market risk: The value of investments can go up and down and an investor may not get back', 'the amount initially invested.', 'Operational risk: Operational processes, including those related to the safekeeping of assets,', 'may fail. This may result in losses to the fund. Failures at service providers could lead to', 'disruptions of fund operations or losses.', 'Performance risk: Investment objectives express an intended result but there is no', 'guarantee that such a result will be achieved. Depending on market conditions and the macro', 'economic environment, investment objectives may become more difficult to achieve.', 'Risk statistics & financial ratios', 'Fund Comparator', 'Annual volatility (%) 6.8 7.1', '(3y)', 'Beta (3y) 0.9 -', 'Sharpe ratio (3y) 0.3 0.0', 'Source: Morningstar. The above ratios are based', 'on bid to bid price based performance data.', 'Asset allocation', 'Asset class (%) Region (%)', 'Liquid Assets 13.9', 'Global 46.4', 'Government bonds 13.1', 'Global Equity 12.8', 'Europe ex-UK/Middle East 24.2', 'Alternatives 11.4', 'UK Equity 10.2', 'USA Equity 8.9 United Kingdom 15.0', 'Aggregate Bonds 6.8', 'Europe Equity 4.8 Americas 8.9', 'Investment Grade Bonds 3.4', 'Absolute Return 3.0 Liquid Assets 2.7', 'Property 3.0', 'Emerging Market Debt Bonds 2.8 Japan 2.0', 'Japan Equity 2.0', 'Emerging Market Equity 1.7', 'Pacific ex-Japan 0.8', 'Other Equity 1.6', '0% 3% 5% 8% 10% 13% 0% 10% 20% 30% 40%', 'Fund Fund', "Learn more about Schroders' funds visit: schroders.co.uk 2"]
# data = ['Portfolio objectives & investment policy', 'The Portfolio aims to provide capital growth over the long-term by investing', 'actively managed and can invest in a range of investment vehicles such as c', 'estate investment trusts and exchange traded funds which themselves inve', '2. fixed income securities (including government bonds and corporate bond', 'funds that use absolute return strategies or funds that invest indirectly in re', 'Portfolio range, which offers nine model portfolios with different expected c', 'which aims to be the highest risk portfolio in this range with a 100% allocati', 'average annual volatility (a measure of how much the portfolio’s returns ma', '110% of that of global stock markets (represented by the MSCI All Country W', 'measure of risk.', 'Past performance is not a guide to future performance and may not be', 'go down as well as up and investors may not get back the amounts orig', 'investments to fall as well as rise.', 'Performance (%)', 'Cumulative', '1 month 3 months 6 months YTD 1 year 3 years', 'performance', 'Model (Net of fees) 1.8 2.4 0.0 5.4 4.6 19.7', 'Benchmark 1.2 1.0 -0.1 3.4 1.6 16.3', 'Jul 13', 'Discrete yearly Jul 14 -Jul 15 -Jul 16Jul 17 -Jul 18 -Jul 19 - Ju', '- Jul', 'performance (%) Jul 15 Jul 16- Jul 17Jul 18 Jul 19 Jul 20 - J', '14', 'Model (Net of fees) 2.6 -1.3 17.2 22.3 5.0 8.0 -1.1 2', 'Benchmark 4.1 6.9 6.6 13.0 5.8 4.3 -2.4 1', 'Calendar year', '2013 2014 2015 2016 2017 2018 2019 2', 'performance', 'Model (Net of fees) 1.2 3.3 -2.9 26.3 23.0 -10.4 18.5 1', 'Benchmark 14.8 4.8 2.1 14.2 11.1 -6.6 15.6', 'Performance over 10 years (%)', '50.0%', '2 05 .. 00 %% 14.8% 14.8% 14.8% 26.3% 26.3% 26.3% 14.2% 14.2% 14.2% 23.0% 23.0% 23.0% 11.1% 11.1% 11.1% 18.5% 18.5% 18.5% 15.6% 15.6% 15.6% 19.3% 19.3% 19.3%', '1.2% 1.2% 1.2% 3.3% 3.3% 3.3% 4.8% 4.8% 4.8% 2.1% 2.1% 2.1% 7.0% 7.0% 7.0%', '-2.9%-2.9%-2.9% -10.4%-10.4%-10.4% -6-6-6.6%.6%.6%', '-25.0%', '2013 2014 2015 2016 2017 2018 2019 2020', 'Schroder Active Portfolio 10 Flexible Investment', '10 year return of GBP 10,000', '22,500', '20,000', '17,500', '15,000', '12,500', '10,000', '7,500', 'Jan-14 Jan-15 Jan-16 Jan-17 Jan-18 Jan-19 Jan-20 Jan-21 Jan-22 Ja', 'Schroder Active Portfolio 10 Flexible Investment', 'The chart is for illustrative purposes only and does not reflect an actual retu', 'investment.', 'Returns are calculated bid to bid (which means performance does not includ', 'initial charges), net income reinvested, net of fees.', 'Risk considerations', 'Credit risk: A decline in the financial health of an issuer could cause the valu', 'fall or become worthless.', 'Derivatives Risk: Derivatives, which are financial instruments deriving their', 'underlying asset, may be used to manage the portfolio efficiently. The portf', 'materially invest in derivatives including using short selling and leverage tec', 'aim of making a return. A derivative may not perform as expected, may crea', 'than the cost of the derivative and may result in losses to the fund.', 'Currency risk:The portfolio may lose value as a result of movements in fore', 'rates, otherwise known as currency rates.', 'Interest rate risk: The portfolios may lose value as a direct result of interes', 'Negative Yields Risk: If interest rates are very low or negative, this may ha', 'impact on the performance of the portfolios.', 'Money Market & Deposits Risk: A failure of a deposit institution or an issu', 'market instrument could have a negative impact on the performance of the', 'Leverage Risk: The portfolio uses derivatives for leverage, which makes it m', 'certain market or interest rate movements and may cause above average vo', 'loss.', 'Equity Risk: Equity prices fluctuate daily, based on many factors including g', 'industry or company news.', 'Counterparty Risk: The portfolios may have contractual agreements with c', 'counterparty is unable to fulfil their obligations, the sum that they owe to th', 'be lost in part or in whole.', 'Capital Risk: All capital invested is at risk. You may not get back some or all', 'investment.', 'High yield bond risk: High yield bonds (normally lower rated or unrated) ge', 'greater market, credit and liquidity risk.', 'Liquidity risk:In difficult market conditions, the portfolio may not be able to', 'full value or at all. This could affect performance and could cause the portfo', 'suspend redemptions of its shares, meaning investors may not be able to h', 'access to their holdings.', 'Asset allocation', 'Source: Schroders. Top holdings and asset allocation are at Portfolio level.', 'Asset class (%)', 'Stock 95.5', 'Cash 4.0', 'Other 0.5', 'Bond 0.1', '0% 10% 20% 30% 40% 50% 60% 70% 80% 90% 100%', 'Portfolio', 'Region (%)', 'Developed country 67.8', 'Emerging Market 27.7', 'Asia - Emerging 20.8', 'United States 20.3', 'United Kingdom 14.6', 'Asia - Developed 13.6', 'Eurozone 9.9', 'Japan 4.5', 'Latin America 4.5', 'Europe - ex euro 3.5', 'Africa 1.7', 'Europe - Emerging 0.6', 'Other 1.3', '0% 10% 20% 30% 40% 50% 60% 70%', 'Portfolio', 'Contact information', 'Schroder Investment Solutions', '1 London Wall Place, London Wall, Barbican', 'London', 'United Kingdom', 'London', 'EC2Y 5AU', 'Tel: 020 7658 6000', 'Fax:', 'For your security, communications may be taped or monitored.', 'Information relating to changes in portfolio manager, investm', 'Benchmarks:', 'Benchmark names in this document may be abbreviated. Please refer to the', 'The investment manager invests on a discretionary basis and there are no r', 'may deviate from the benchmark. The investment manager will invest in com', 'advantage of specific investment opportunities.', 'Source and ratings information', 'Source of all performance data, unless otherwise stated: Morningstar, bid to', 'These portfolios were managed under a different brand prior to the 5th of M', 'Investment Solutions Brand.', 'Important information', 'Costs:', 'Certain costs associated with your investment in the fund may be incurred i', 'increase or decrease as a result of currency and exchange rate fluctuations.', 'If a performance fee is applicable to this fund, details of the performance fe', 'prospectus. This includes a description of the performance fee calculation m', 'of how the performance fee is calculated in relation to the fund’s performan', 'investment objective or investment policy.', 'For further information regarding the costs and charges associated with you', 'report.', 'General:', 'This information is a marketing communication. For help in understanding a', 'gb/uk/individual/education-hub/glossary/Any reference to sectors/countries', 'recommendation to buy or sell any financial instrument/securities or adopt', 'should not be relied on for, accounting, legal or tax advice, or investment re', 'information in the material when taking individual investment and/or strate', 'and may not be repeated. The value of investments and the income from th', 'amounts originally invested. Exchange rate changes may cause the value of', 'and opinions in this webpage and these may change. Information herein is', 'or accuracy. Insofar as liability under relevant laws cannot be excluded, no S', 'material or for any resulting loss or damage (whether direct, indirect, conse', 'your personal data. For information on how Schroders might process your p', 'www.Schroders.com/en/privacy-policy or on request should you not have ac', 'provider and may not be reproduced or extracted and used for any other pu', 'without any warranties of any kind. The data provider and issuer of the info', 'data.Schroders Investment Solutions is the trading name for the following p', 'Index Portfolios, and the Schroder Sustainable Portfolios. These Model Port', 'Wall Place, London EC2Y 5AU. Registered number 2280926 England. Author', 'Financial Conduct Authority and the Prudential Regulation Authority. Issued', 'recorded or monitored.The timing of the data shown on this page and the fr', 'publication date shown on all material. Please contact the Portfolio Manage', 'jurisdiction where prohibited by law and must not be used in any way that w', 'Schroders will be a data controller in respect of your personal data. For info', 'view our Privacy Policy available at www.Schroders.com/en/privacy-policy or', 'data is owned or licensed by the data provider and may not be reproduced o', 'consent. Third party data is provided without any warranties of any kind. Th', 'connection with the third party data. Issued by Schroders & Co Ltd, 1 Londo', 'Authorised and regulated by the Financial Conduct Authority.', 'The timing of the data shown on this page and the frequency of report upda', 'material. Please contact the Portfolio Manager for further explanation.', 'g in a diversified range of assets and markets worldwide. The Portfolio is', 'collective investment schemes, closed ended investment schemes, real', 'est worldwide in any of the following: 1. equity or equity related securities;', 'ds); 3. currencies; and 4. alternative assets. Alternative assets may include', 'eal estate and commodities. The portfolio is part of the Schroder Active', 'combinations of investment risk and return. This portfolio is risk level 10,', 'ion to equity. Please note, the risk level of this portfolio has a target', 'ay vary over a year) over a rolling five year period of between 85% to', 'World index). However, it is important to note that volatility is only one', 'e repeated. The value of investments and the income from them may', 'ginally invested. Exchange rate changes may cause the value of', 'Ratings and accreditation', 's 5 years 10 years', '27.9 94.9', '18.5 68.2', 'Please refer to the Source and ratings', 'information section for details on the icons', 'Jul 20 Jul 21 -Jul 22 - shown above.', 'Jul 21 Jul 22 Jul 23', 'Model facts', '25.7 -9.0 4.6', 'Portfolio manager Alex Funk', '19.7 -4.4 1.6 Managed Portfolio 05.08.2019', 'Since', 'Portfolio management Schroder Investment', '2020 2021 2022 company Solutions', 'Domicile United Kingdom', '19.3 8.1 -12.2 Launch Date 02.01.2008', '7.0 11.4 -9.1 Base Currency GBP', 'Benchmark Flexible Investment', 'Dealing frequency Not Applicable', 'Distribution frequency No Distribution', 'Fees & expenses', '%%%', '8.1% 8.1% 8.1% 11.4 11.4 11.4 OCF (Incl MPS Fee) 0.90%', 'Model portfolio fee 0.15%', '-12.2%-12.2%-12.2% -9.1%-9.1%-9.1%', '2021 2022', '1', 'Purchase details', '125.0% Providers', '100.0%', '75.0%', '50.0%', '25.0%', '0.0%', '-25.0%', 'an-23', 'urn on any', 'de the effect of any', 'ue of its bonds to', 'r value from an', 'folio may also', 'chniques with the', 'ate losses greater', 'eign exchange', 'st rate changes.', 'Risk Rating', 'ave a negative', 'uer of a money 1 2 3 4 5 6 7 8 9 10', 'e portfolios.', 'more sensitive to', 'olatility and risk of', 'general, economic,', 'The portfolio is also risk mapped to the risk tools', 'counterparties. If a', 'shown.', 'he portfolios may', 'Risk statistics & financial ratios', 'l of your', 'Portfolio Benchmark', 'enerally carry', 'Annual volatility (%) 11.2 8.5', '(3y)', 'o sell a security for', 'olio to defer or Beta (3y) 1.2 -', 'have immediate', 'Sharpe ratio (3y) 0.5 0.5', 'Source: Morningstar. The above ratios are based', 'on bid to bid price based performance data.', '2', 'Sector (%)', 'Financial services 20.0', 'Technology 18.4', 'Industrials 13.9', 'Consumer cyclical 9.7', 'Communication Services 7.8', 'Consumer defensive 7.5', 'Healthcare 7.3', 'Basic materials 4.3', 'Cash & equivalents 4.0', 'Utilities 2.8', 'Energy 2.5', 'Real estate 1.1', 'Other 0.1', '0% 5% 10% 15% 20%', 'Portfolio', 'Top 10 holdings (%)', 'Holding name %', 'Fidelity Emerg Mkts R Acc 17.5', 'Lazard Global Thematic Focus J Acc GBP 11.6', 'Artemis SmartGARP Glb EM Eq I Acc GBP 11.1', 'FSSA Asia Focus B GBP Acc 10.9', 'Fidelity Global Dividend W Acc 8.8', 'JOHCM UK Dynamic M Acc 6.6', 'Schroder Global Sust Val Eq Q1Cap 5.9', 'Federated Hermes GEMs SMID Eq L GBP Acc 4.4', 'TB Evenlode Income C Inc 4.2', 'Other 19.0', 'ment objective, benchmark and corporate action information', 'e funds’ legal documents for the full benchmark name.', "restrictions on the extent to which the fund's portfolio and performance", 'mpanies or sectors not included in the benchmark in order to take', '3', 'o bid, net income reinvested, net of fees.', 'May 2021. As of this date they are managed under the Schroders', 'in a different currency to that of your investment. These costs may', '.', 'ee model and its computation methodology can be found in the fund’s', 'methodology, the dates on which the performance fee is paid and details', 'nce fee benchmark, which may differ from the benchmark in the fund’s', 'ur investment, please consult the funds’ offering documents and annual', 'any terms used, please visit address https://www.schroders.com/en-', 's/stocks/securities are for illustrative purposes only and not a', 'any investment strategy. The material is not intended to provide, and', 'ecommendations. Reliance should not be placed on any views or', 'egic decisions. Past performance is not a guide to future performance', 'hem may go down as well as up and investors may not get back the', 'f investments to fall as well as rise.Schroders has expressed its own views', 'believed to be reliable but Schroders does not warrant its completeness', 'Schroders entity accepts any liability for any error or omission in this', 'equential or otherwise). Schroders will be a data controller in respect of', 'personal data, please view our Privacy Policy available at', 'ccess to this webpage. Third party data is owned or licensed by the data', "urpose without the data provider's consent. Third party data is provided", 'ormation shall have no liability in connection with the third party', 'products and services: Schroder Active Portfolios, Schroder Strategic', 'tfolios are provided by Schroders & Co Ltd. Registered office at 1 London', 'rised by the Prudential Regulation Authority and regulated by the', 'd by Schroders & Co. Limited. For your security, communications may be', 'requency of report updates may differ. The data is correct on the', 'er for further explanation. This material must not be issued in any', 'would be contrary to local law or regulation.', 'ormation on how Schroders might process your personal data, please', 'r on request should you not have access to this webpage. Third party', "or extracted and used for any other purpose without the data provider's", 'he data provider and issuer of the information shall have no liability in', 'on Wall Place, London EC2Y 5AU. Registration No 2280926 England.', 'ates may differ. The data is correct on the publication date shown on all', '4', '']
data = [  'Asset class (%)', 'Stock 95.5', 'Cash 4.0', 'Other 0.5', 'Bond 0.1', '0% 10% 20% 30% 40% 50% 60% 70% 80% 90% 100%', 'Portfolio', 'Region (%)', 'Developed country 67.8', 'Emerging Market 27.7', 'Asia - Emerging 20.8', 'United States 20.3', 'United Kingdom 14.6', 'Asia - Developed 13.6', 'Eurozone 9.9', 'Japan 4.5', 'Latin America 4.5', 'Europe - ex euro 3.5', 'Africa 1.7', 'Europe - Emerging 0.6', 'Other 1.3', 'Sector (%)', 'Financial services 20.0', 'Technology 18.4', 'Industrials 13.9', 'Consumer cyclical 9.7', 'Communication Services 7.8', 'Consumer defensive 7.5', 'Healthcare 7.3', 'Basic materials 4.3', 'Cash & equivalents 4.0', 'Utilities 2.8', 'Energy 2.5', 'Real estate 1.1', 'Other 0.1', '0% 5% 10% 15% 20%', 'Portfolio', 'Top 10 holdings (%)', 'Holding name %', 'Fidelity Emerg Mkts R Acc 17.5', 'Lazard Global Thematic Focus J Acc GBP 11.6', 'Artemis SmartGARP Glb EM Eq I Acc GBP 11.1', 'FSSA Asia Focus B GBP Acc 10.9', 'Fidelity Global Dividend W Acc 8.8', 'JOHCM UK Dynamic M Acc 6.6', 'Schroder Global Sust Val Eq Q1Cap 5.9', 'Federated Hermes GEMs SMID Eq L GBP Acc 4.4', 'TB Evenlode Income C Inc 4.2', 'Other 19.0', ]
# reader = PdfReader(file)
# number_of_pages = len(reader.pages)
# page = reader.pages[1]
# text = page.extract_text()
# print(text.strip().split('\n'))


# text = extract_text(file)

# data = (text.strip().split('\n'))
# filtered_data = [item for item in data if item != '']
# print(filtered_data)


asset_labels = ['Bond',
                'Cash',
                'Stock',
                'Other',
                'Convertible',
                'Preferred',
                'Government bonds',
                'Liquid Assets',
                'Alternatives',
                'Aggregate Bonds',
                'Global Equity',
                'UK Equity',
                'Investment Grade Bonds',
                'USA Equity',
                'Property',
                'Absolute Return',
                'Emerging Market Debt Bonds',
                'Europe Equity',
                'Japan Equity',
                'Emerging Market Equity',
                'Other Equity',
                'Global',
                'Europe ex-UK/Middle East',
                'United Kingdom',
                'Americas',
                'Japan',
                'Pacific ex-Japan',
                'Developed country',
                'United States',
                'Eurozone',
                'Europe - ex euro',
                'Emerging Market',
                'Asia - Developed',
                'Asia - Emerging',
                'Canada',
                'Australasia',
                'Latin America',
                'Derivatives',
                'Corporate',
                'Government',
                'Technology',
                'Financial services',
                'Healthcare',
                'Industrials',
                'Consumer cyclical',
                'Consumer defensive',
                'Real estate',
                'Communication Services',
                'Cash & equivalents',
                'Energy',
                'Basic materials',
                'Utilities',
                'Hedge Funds',
                'Asia Pacific ex Japan Equity',
                'Commodities', ]


asset_labels.sort(key=len, reverse=True)

# Создаем словарь для хранения процентов каждого актива
percentages = {}
# Создаем словарь для отслеживания, сколько раз каждая метка актива была найдена
label_counts = {}

# Проходим по каждому элементу списка
for item in data:
    # Копируем строку для последующего редактирования
    temp_item = item
    # Для каждой метки актива пытаемся найти ее в элементе
    for label in asset_labels:
        while label in temp_item:
            # Если метка найдена, пытаемся извлечь число (процент) после нее
            match = re.search(f'{re.escape(label)} (\d+\.\d+)', temp_item)
            if match:
                # Подсчитываем количество раз, которое мы видели эту метку
                label_counts[label] = label_counts.get(label, 0) + 1

                # Изменяем метку на основе количества раз, которое она была найдена
                if label == 'Liquid Assets' and label_counts[label] == 1:
                    key = 'Liquid Assets class'
                elif label == 'Liquid Assets' and label_counts[label] == 2:
                    key = 'Liquid Assets Region'
                else:
                    key = label

                percentages[key] = float(match.group(1))
                print(percentages)
                # Удаляем найденную метку и процент из временной строки
                temp_item = temp_item.replace(match.group(0), '', 1)
                # print(percentages).sort(key=len, reverse=True)
    # total_percentage = sum(percentages.values())
    # print(total_percentage)

