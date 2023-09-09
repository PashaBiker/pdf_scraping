import re
from bs4 import BeautifulSoup

html_content = """
<div class="product-data-list data-points-en_GB">
<div class="float-left in-left col-totalNetAssetsFundLevel ">
<span class="caption" data-label="" data-hascontent="no">
Net Assets of Fund
<span class="as-of-date">
as of 08/Sep/2023
</span>
</span>
<span class="data">
GBP 5,331,195
</span>
</div>
<div class="float-left in-right col-inceptionDate " style="height: 36px;">
<span class="caption" data-label="" data-hascontent="no">
Share Class launch date
<span class="as-of-date">
</span>
</span>
<span class="data">
26/Jul/2021
</span>
</div>
<div class="float-left in-left col-launchDate " style="height: 16px;">
<span class="caption" data-label="" data-hascontent="no">
Fund Launch Date
<span class="as-of-date">
</span>
</span>
<span class="data">
26/Jul/2021
</span>
</div>
<div class="float-left in-right col-seriesBaseCurrencyCode ">
<span class="caption" data-label="" data-hascontent="no">
Share Class Currency
<span class="as-of-date">
</span>
</span>
<span class="data">
GBP
</span>
</div>
<div class="float-left in-left col-baseCurrencyCode " style="height: 16px;">
<span class="caption" data-label="" data-hascontent="no">
Fund Base Currency
<span class="as-of-date">
</span>
</span>
<span class="data">
GBP
</span>
</div>
<div class="float-left in-right col-assetClass ">
<span class="caption" data-label="" data-hascontent="no">
Asset Class
<span class="as-of-date">
</span>
</span>
<span class="data">
Multi Asset
</span>
</div>
<div class="float-left in-left col-constraintBenchmark ">
<span class="caption" data-label="" data-hascontent="no">
Constraint Benchmark 1
<a role="button" class="product-info-bubble " href="#" data-hasqtip="1625" title=""></a>
<span class="as-of-date">
</span>
</span>
<span class="data">
MSCI World Index (50%), Bloomberg Global Aggregate Bond Index USD Hedged (50%)
</span>
</div>
<div class="float-left in-right col-sfdr " style="height: 48px;">
<span class="caption" data-label="" data-hascontent="no">
SFDR Classification
<a role="button" class="product-info-bubble " href="#" data-hasqtip="1626" title=""></a>
<span class="as-of-date">
</span>
</span>
<span class="data">
Other
</span>
</div>
<div class="float-left in-left col-investmentAssociationCategory " style="height: 16px;">
<span class="caption" data-label="" data-hascontent="no">
Investment Association Category
<span class="as-of-date">
</span>
</span>
<span class="data">
-
</span>
</div>
<div class="float-left in-right col-initialCharge ">
<span class="caption" data-label="" data-hascontent="no">
Initial Charge
<span class="as-of-date">
</span>
</span>
<span class="data">
0.00%
</span>
</div>
<div class="float-left in-left col-onch ">
<span class="caption" data-label="" data-hascontent="no">
Ongoing Charges Figures
<a role="button" class="product-info-bubble " href="#" data-hasqtip="1627" title="" aria-describedby="qtip-1627"></a>
<span class="as-of-date">
</span>
</span>
<span class="data">
0.28%
</span>
</div>
<div class="float-left in-right col-isin " style="height: 18px;">
<span class="caption" data-label="" data-hascontent="no">
ISIN
<span class="as-of-date">
</span>
</span>
<span class="data">
GB00BN08ZB07
</span>
</div>
<div class="float-left in-left col-mer ">
<span class="caption" data-label="" data-hascontent="no">
Annual Management Fee
<a role="button" class="product-info-bubble " href="#" data-hasqtip="1628" title="" aria-describedby="qtip-1628"></a>
<span class="as-of-date">
</span>
</span>
<span class="data">
0.23%
</span>
</div>
<div class="float-left in-right col-bscf " style="height: 18px;">
<span class="caption" data-label="" data-hascontent="no">
Performance Fee
<span class="as-of-date">
</span>
</span>
<span class="data">
0.00%
</span>
</div>
<div class="float-left in-left col-minimumInitialInvestment " style="height: 16px;">
<span class="caption" data-label="" data-hascontent="no">
Minimum Initial Investment
<span class="as-of-date">
</span>
</span>
<span class="data">
GBP 100,000.00
</span>
</div>
<div class="float-left in-right col-minimumSubsequentInvestment ">
<span class="caption" data-label="" data-hascontent="no">
Minimum Subsequent Investment
<span class="as-of-date">
</span>
</span>
<span class="data">
GBP 100.00
</span>
</div>
<div class="float-left in-left col-useOfProfitsCode " style="height: 16px;">
<span class="caption" data-label="" data-hascontent="no">
Use of Income
<span class="as-of-date">
</span>
</span>
<span class="data">
Accumulating
</span>
</div>
<div class="float-left in-right col-domicile ">
<span class="caption" data-label="" data-hascontent="no">
Domicile
<span class="as-of-date">
</span>
</span>
<span class="data">
United Kingdom
</span>
</div>
<div class="float-left in-left col-emeaLegalStructure " style="height: 16px;">
<span class="caption" data-label="" data-hascontent="no">
Regulatory Structure
<span class="as-of-date">
</span>
</span>
<span class="data">
UCITS
</span>
</div>
<div class="float-left in-right col-fundManagementCompany ">
<span class="caption" data-label="" data-hascontent="no">
Management Company
<span class="as-of-date">
</span>
</span>
<span class="data">
BlackRock Fund Managers Ltd
</span>
</div>
<div class="float-left in-left col-morningstarCategory " style="height: 16px;">
<span class="caption" data-label="" data-hascontent="no">
Morningstar Category
<span class="as-of-date">
</span>
</span>
<span class="data">
-
</span>
</div>
<div class="float-left in-right col-dealingSettlementTranslated ">
<span class="caption" data-label="" data-hascontent="no">
Dealing Settlement
<span class="as-of-date">
</span>
</span>
<span class="data">
Trade Date + 3 days
</span>
</div>
<div class="float-left in-left col-dealingFrequencyTranslated " style="height: 16px;">
<span class="caption" data-label="" data-hascontent="no">
Dealing Frequency
<span class="as-of-date">
</span>
</span>
<span class="data">
Daily, forward pricing basis
</span>
</div>
<div class="float-left in-right col-bloombergTicker ">
<span class="caption" data-label="" data-hascontent="no">
Bloomberg Ticker
<span class="as-of-date">
</span>
</span>
<span class="data">
MY4SIDA
</span>
</div>
<div class="float-left in-left col-sedolMutualFund ">
<span class="caption" data-label="" data-hascontent="no">
SEDOL
<span class="as-of-date">
</span>
</span>
<span class="data">
BN08ZB0
</span>
</div>
<div class="clear"></div>
</div>
"""

# Инициализация BeautifulSoup объекта
soup = BeautifulSoup(html_content, 'html.parser')

# Поиск нужного элемента с использованием регулярного выражения
ocf_element = soup.find('span', string=re.compile(r'\s*Ongoing Charges Figures\s*'))
if ocf_element:
    ocf_value = ocf_element.find_next_sibling('span', class_='data').get_text(strip=True)
    print(f'Ongoing Charges Figures: {ocf_value}')
else:
    print('Element not found.')