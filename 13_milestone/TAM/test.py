import re
from bs4 import BeautifulSoup

# Your HTML content
html_content = """<tbody>
			<tr class="active">
				<td colspan="2" style="vertical-align: middle; background-color: rgb(238, 238, 238);"><strong>Quarterly Model Portfolio Factsheets</strong></td>
				<td align="center" style="vertical-align: middle; background-color: rgb(238, 238, 238);">&nbsp;</td>
				<td align="center" style="vertical-align: middle; background-color: rgb(238, 238, 238);">&nbsp;</td>
				<td align="center" style="vertical-align: middle; background-color: rgb(238, 238, 238);">&nbsp;</td>
			</tr>
			<tr>
				<td bgcolor="#f5f5f5" style="vertical-align: middle;">&nbsp;</td>
				<td align="center" bgcolor="#f5f5f5" style="text-align: center; vertical-align: middle;"><span style="text-align: center; width: 200px;"><img alt="TAM Active" src="https://www.tamassetmanagement.com/data/uploads/product-logos/logo-tam-active.png?v=2" style="width: 132px; height: 25px;"></span></td>
				<td align="center" bgcolor="#f5f5f5" style="text-align: center; vertical-align: middle;"><span style="text-align: center; width: 200px;"><img alt="TAM Enhanced Passive" src="https://www.tamassetmanagement.com/data/uploads/product-logos/logo-tam-enhanced-passive.png?v=2" style="width: 154px; height: 25px;"></span></td>
				<td align="center" bgcolor="#f5f5f5" style="text-align: center; vertical-align: middle;"><span style="text-align: center; width: 200px;"><img alt="TAM Sustainable World" src="https://www.tamassetmanagement.com/data/uploads/product-logos/logo-tam-sustainable-world.png?v=2" style="width: 161px; height: 25px;"></span></td>
				<td align="center" bgcolor="#f5f5f5" style="text-align: center; vertical-align: middle;"><span style="text-align: center; width: 200px;"><img alt="TAM Sharia" src="https://www.tamassetmanagement.com/data/uploads/product-logos/logo-tam-sharia.png?v=2" style="width: 133px; height: 25px;"></span></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">Liquidity Plus</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/active-liquidity-plus-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;">N/A</td>
				<td align="center" style="text-align: center; vertical-align: middle;">N/A</td>
				<td align="center" style="text-align: center; vertical-align: middle;">N/A</td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">Defensive</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/active-defensive-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/enhanced-passive-defensive-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_passive_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="/data/uploads/factsheets/sustainable-world-defensive-q4-2023.pdf"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_esg_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/sharia-defensive-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sharia_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">Cautious</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/active-cautious-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/enhanced-passive-cautious-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_passive_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="/data/uploads/factsheets/sustainable-world-cautious-q4-2023.pdf"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_esg_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/sharia-cautious-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sharia_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">Balanced</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/active-balanced-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/enhanced-passive-balanced-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_passive_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="/data/uploads/factsheets/sustainable-world-balanced-q4-2023.pdf"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_esg_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/sharia-balanced-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sharia_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">Growth</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/active-growth-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/enhanced-passive-growth-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_passive_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="/data/uploads/factsheets/sustainable-world-growth-q4-2023.pdf"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_esg_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/sharia-growth-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sharia_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">Adventurous</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/active-adventurous-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/enhanced-passive-adventurous-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_passive_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="/data/uploads/factsheets/sustainable-world-adventurous-q4-2023.pdf"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_esg_sm.gif"></span></a></td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/sharia-adventurous-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sharia_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">Speculative</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/active-speculative-q4-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="center" style="vertical-align: middle;">N/A</td>
				<td align="center" style="vertical-align: middle;">N/A</td>
				<td align="center" style="vertical-align: middle;">N/A</td>
			</tr>
			<tr>
				<td colspan="5">&nbsp;</td>
			</tr>
			<tr>
				<td colspan="5" style="vertical-align: middle; background-color: rgb(238, 238, 238);"><strong>TAM Global Multi-Asset Fund</strong></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">Fund Infographic</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/infographics/tam-global-jan-2023-final.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/premier-speculative-q3-2022.pdf" target="_blank"><span style="text-align: center;"></span><span style="text-align: center;"></span></a></td>
				<td align="right" colspan="2" style="vertical-align: middle;">Fund Request Form</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/forms/tam-uk-global-fund-request-form-2022.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">Fund Factsheet&nbsp;&nbsp;</td>
				<td align="center" style="vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/factsheets/tam-global-fund-factsheet-december-2023.pdf"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="right" colspan="2" style="vertical-align: middle;">Fund Application Form</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/forms/tam-uk-global-fund-application-form-2022.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td colspan="5">&nbsp;</td>
			</tr>
			<tr class="active">
				<td colspan="5" rowspan="1" style="vertical-align: middle; background-color: rgb(238, 238, 238);"><strong>Model Portfolio Literature</strong></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">TAM for Financial Advisers</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="/data/uploads/brochures/tam-uk-adviser-brochure-q3-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="right" colspan="2" rowspan="1" style="vertical-align: middle;">TAM and Defaqto 2023<a href="/data/uploads/brochures/tam-uk-adviser-brochure-q1-2023.pdf" target="_blank"><span style="text-align: center;"></span></a></td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/infographics/tam-and-defaqto-2023-final.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">TAM for Advised Clients</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="/data/uploads/brochures/tam-uk-client-brochure-q3-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="right" colspan="2" rowspan="1" style="vertical-align: middle;">TAM Sustainable World</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/infographics/tam-sustainable-world-june-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">TAM Active</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/infographics/tam-active-june-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="right" colspan="2" rowspan="1" style="vertical-align: middle;">TAM Sustainable World - Investment Jigsaw</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/infographics/tam-sustainable-world-investment-jigsaw_0923-final.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">TAM Active - Investment Jigsaw</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/infographics/tam-active-june-2023.pdf" target="_blank"><span style="text-align: center;"></span></a><a href="/data/uploads/infographics/tam-active-investment-jigsaw-final.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a><a href="/data/uploads/infographics/tam-active-june-2023.pdf" target="_blank"><span style="text-align: center;"></span><span style="text-align: center;"></span></a><a href="/data/uploads/infographics/you-give-we-give-jan-2023-final.pdf" target="_blank"><span style="text-align: center;"></span></a></td>
				<td align="right" colspan="2" rowspan="1" style="vertical-align: middle;">TAM Sharia</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/infographics/tam-sharia-june-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">TAM Active - The Liquidity Plus Portfolio</td>
				<td align="center" style="vertical-align: middle;"><span style="text-align: center;"><a href="https://www.tamassetmanagement.com/data/uploads/infographics/tam-liquidity-plus-aug-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></span></td>
				<td align="right" colspan="2" rowspan="1" style="vertical-align: middle;">TAM Sustainability Mission</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/infographics/tam-sustainability-mission_1123-final.pdf"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a><a href="/data/uploads/infographics/tam-enhanced-passive-june-2023.pdf" target="_blank"><span style="text-align: center;"></span><span style="text-align: center;"></span></a><a href="/data/uploads/infographics/tam-sharia-june-2023.pdf" target="_blank"><span style="text-align: center;"></span></a><a href="/data/uploads/infographics/tam-sharia-june-2023.pdf" target="_blank"><span style="text-align: center;"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">TAM Enhanced Passive</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/infographics/tam-enhanced-passive_0923-final.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="right" colspan="2" style="vertical-align: middle;">You Give We Give</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/infographics/you-give-we-give-jan-2023-final.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">TAM Enhanced Passive - Investment Jigsaw</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/infographics/tam-sustainable-world-june-2023.pdf" target="_blank"><span style="text-align: center;"></span></a><a href="/data/uploads/infographics/tam-enhanced-passive-investment-jigsaw-final.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a><a href="/data/uploads/infographics/tam-sustainable-world-june-2023.pdf" target="_blank"><span style="text-align: center;"></span></a></td>
				<td align="right" colspan="2" style="vertical-align: middle;">&nbsp;</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/infographics/tam-enhanced-passive-june-2023.pdf" target="_blank"><span style="text-align: center;"></span></a></td>
			</tr>
			<tr>
				<td colspan="5">&nbsp;</td>
			</tr>
			<tr>
				<td colspan="5" style="vertical-align: middle; background-color: rgb(238, 238, 238);"><strong>User Guides</strong></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">The TAM Platform</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/brochures/tam-platform-user-guide.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="center" style="vertical-align: middle;">&nbsp;</td>
				<td align="center" style="vertical-align: middle;">&nbsp;</td>
				<td align="center" style="vertical-align: middle;">&nbsp;</td>
			</tr>
			<tr>
				<td colspan="5">&nbsp;</td>
			</tr>
			<tr class="active">
				<td colspan="5" rowspan="1" style="vertical-align: middle; background-color: rgb(238, 238, 238);"><strong>Model Portfolio Questionnaires and Application Forms</strong></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">TAM ESG Questionnaire</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="/data/uploads/forms/tam-esg-questionnaire-2020.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="right" colspan="2" rowspan="1" style="vertical-align: middle;">ISA Application 2023/24</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/forms/tam-isa-supplement-2023-24.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">TAM Proposal Request Form</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="/data/uploads/forms/tam-uk-proposal-request-form-jul-23.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="right" colspan="2" rowspan="1" style="vertical-align: middle;">Junior ISA Application 2023/24</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/forms/tam-junior-isa-supplement-2023-24.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">TAM UK DFM Application Form&nbsp;</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="/data/uploads/forms/tam-uk-dfm-application-form-sep-23.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="right" colspan="2" rowspan="1" style="vertical-align: middle;">APS ISA Application 2023/24</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/forms/tam-aps-isa-supplement-2023-24.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">TAM UK Portfolio Switch Form</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="https://www.tamassetmanagement.com/data/uploads/forms/tam-uk-portfolio-switch-form-jul-23.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="right" colspan="2" rowspan="1" style="vertical-align: middle;">Client Carbon Footprint Commitment Application</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/forms/tam-ccfc-application-form-jan-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
			</tr>
			<tr>
				<td style="vertical-align: middle;">TAM UK Withdrawal &amp; Closure Form</td>
				<td align="center" style="text-align: center; vertical-align: middle;"><a href="/data/uploads/forms/tam-uk-withdrawal-closure-form-sep-2022.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
				<td align="right" colspan="2" rowspan="1" style="vertical-align: middle;">You Give We Give Application</td>
				<td align="center" style="vertical-align: middle;"><a href="/data/uploads/forms/ygwg-application-form-jan-2023.pdf" target="_blank"><span style="text-align: center;"><img alt="" src="https://www.tamassetmanagement.com/data/uploads/ico_pdf_sm.gif"></span></a></td>
			</tr>
		</tbody>"""

# Initialize BeautifulSoup

# Dictionary to store the data
portfolios = {}

soup = BeautifulSoup(html_content, 'html.parser')
# Base URL for links that don't start with 'http'
base_url = 'https://www.tamassetmanagement.com'

# Find all the <tr> elements
for tr in soup.find_all('tr'):
    # The first <td> in each <tr> should contain the portfolio name
    tds = tr.find_all('td')
    if tds and len(tds) > 1:
        portfolio_name = tds[0].get_text(strip=True)
        # Iterate over all <td> elements, starting from the second one
        for td in tds[1:]:
            pdf_link_tag = td.find('a')
            if pdf_link_tag and 'href' in pdf_link_tag.attrs:
                link = pdf_link_tag['href']
                # Prepend base URL if needed
                if not link.startswith('http'):
                    link = base_url + link
                # Extract the type from the link and create a new key
                match = re.search(r'/(active|enhanced-passive|sustainable-world|sharia)-([^-]+)-', link)
                if match:
                    type_name = match.group(1).replace('-', ' ').title() + ' ' + portfolio_name
                    portfolios[type_name] = link


# Print the result
print(portfolios)
