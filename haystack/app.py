from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import json
import os
from datetime import datetime

app = Flask(__name__)

class EdgarScraper:
    def __init__(self):
        self.base_url = "https://www.sec.gov/Archives"
        self.headers = {
            "User-Agent": "Stock Analyzer App email@example.com"  # Replace with your email per SEC guidelines
        }

    def search_company(self, ticker):
        """Search for company by ticker and retrieve CIK number"""
        try:
            # Get CIK from ticker using SEC API
            response = requests.get(
                f"https://www.sec.gov/files/company_tickers.json",
                headers=self.headers
            )
            companies = response.json()

            # Find the company with matching ticker
            cik = None
            for _, company in companies.items():
                if company['ticker'].upper() == ticker.upper():
                    # Format CIK with leading zeros to match 10-digit format
                    cik = str(company['cik_str']).zfill(10)
                    break

            if not cik:
                return None, f"Company with ticker {ticker} not found"

            return cik, None

        except Exception as e:
            return None, f"Error searching for company: {str(e)}"

    def get_recent_10k_url(self, cik):
        """Get the most recent 10-K filing URL for a company"""
        try:
            # Use the SEC API to get the submission files
            url = f"https://data.sec.gov/submissions/CIK{cik}.json"
            response = requests.get(url, headers=self.headers)
            data = response.json()

            # Find the most recent 10-K filing
            recent_filings = data.get('filings', {}).get('recent', {})
            if not recent_filings:
                return None, "No recent filings found"

            form_types = recent_filings.get('form', [])
            filing_dates = recent_filings.get('filingDate', [])
            accession_numbers = recent_filings.get('accessionNumber', [])

            # Find the most recent 10-K
            for i, form_type in enumerate(form_types):
                if form_type == '10-K':
                    accession_number = accession_numbers[i].replace('-', '')
                    filing_date = filing_dates[i]

                    # Get the filing details to find the document URL
                    filing_details_url = f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{accession_number}/index.json"
                    details_response = requests.get(filing_details_url, headers=self.headers)
                    details_data = details_response.json()

                    # Get the HTML document filing
                    for filing in details_data.get('directory', {}).get('item', []):
                        if filing.get('name', '').endswith('.htm') and not filing.get('name', '').startswith('R'):
                            doc_url = f"{self.base_url}/edgar/data/{cik.lstrip('0')}/{accession_number}/{filing['name']}"
                            return doc_url, None

            return None, "No 10-K filing found"

        except Exception as e:
            return None, f"Error getting 10-K URL: {str(e)}"

    def extract_financial_data(self, doc_url):
        """Extract financial data from 10-K document"""
        try:
            response = requests.get(doc_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract company name
            company_name = soup.find('company-name')
            if company_name:
                company_name = company_name.text
            else:
                # Try alternative methods to find company name
                title = soup.find('title')
                if title:
                    company_name = title.text.split('|')[0].strip()
                else:
                    company_name = "Unknown"

            # Extract key financial metrics
            metrics = {
                'company_name': company_name,
                'revenue': self._extract_value(soup, ['revenue', 'total revenue', 'net revenue']),
                'net_income': self._extract_value(soup, ['net income', 'net earnings', 'net profit']),
                'total_assets': self._extract_value(soup, ['total assets']),
                'total_liabilities': self._extract_value(soup, ['total liabilities']),
                'cash_and_equivalents': self._extract_value(soup, ['cash and cash equivalents', 'cash and equivalents']),
                'long_term_debt': self._extract_value(soup, ['long-term debt', 'long term debt']),
                'operating_income': self._extract_value(soup, ['operating income', 'income from operations']),
                'fiscal_year_end': self._extract_fiscal_year(soup),
                'filing_date': self._extract_filing_date(soup)
            }

            # Calculate additional metrics
            if metrics['total_assets'] and metrics['total_liabilities']:
                metrics['equity'] = metrics['total_assets'] - metrics['total_liabilities']
            else:
                metrics['equity'] = self._extract_value(soup, ['total equity', 'stockholders equity', 'shareholders equity'])

            if metrics['revenue'] and metrics['net_income']:
                metrics['profit_margin'] = round((metrics['net_income'] / metrics['revenue']) * 100, 2)
            else:
                metrics['profit_margin'] = None

            if metrics['total_assets'] and metrics['net_income']:
                metrics['return_on_assets'] = round((metrics['net_income'] / metrics['total_assets']) * 100, 2)
            else:
                metrics['return_on_assets'] = None

            if metrics['equity'] and metrics['net_income']:
                metrics['return_on_equity'] = round((metrics['net_income'] / metrics['equity']) * 100, 2)
            else:
                metrics['return_on_equity'] = None

            if metrics['total_assets'] and metrics['total_liabilities']:
                metrics['debt_to_assets_ratio'] = round(metrics['total_liabilities'] / metrics['total_assets'], 2)
            else:
                metrics['debt_to_assets_ratio'] = None

            return metrics, None

        except Exception as e:
            return None, f"Error extracting financial data: {str(e)}"

    def _extract_value(self, soup, keywords):
        """Extract financial value based on keywords"""
        for keyword in keywords:
            # Look for tables with matching headers or labels
            for table in soup.find_all('table'):
                for row in table.find_all('tr'):
                    cells = row.find_all(['td', 'th'])
                    for i, cell in enumerate(cells):
                        if cell.text and keyword.lower() in cell.text.lower():
                            # Try to get the value from the next cell or adjacent cells
                            if i + 1 < len(cells) and cells[i + 1].text:
                                value_text = cells[i + 1].text.strip()
                                return self._parse_financial_value(value_text)

            # Try to find divs or spans with labels and values
            for elem in soup.find_all(['div', 'span', 'p']):
                if elem.text and keyword.lower() in elem.text.lower():
                    # Try to extract numbers from the text
                    value_match = re.search(r'[\$£€]?\s?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s?(?:million|billion|m|b)?', elem.text, re.IGNORECASE)
                    if value_match:
                        return self._parse_financial_value(value_match.group(0))

        return None

    def _parse_financial_value(self, value_text):
        """Parse financial value from text to number"""
        try:
            # Remove currency symbols and commas
            value_text = re.sub(r'[\$£€,]', '', value_text)

            # Handle millions/billions notation
            multiplier = 1
            if 'billion' in value_text.lower() or 'b' in value_text.lower():
                multiplier = 1_000_000_000
                value_text = re.sub(r'billion|b', '', value_text, flags=re.IGNORECASE)
            elif 'million' in value_text.lower() or 'm' in value_text.lower():
                multiplier = 1_000_000
                value_text = re.sub(r'million|m', '', value_text, flags=re.IGNORECASE)

            # Extract the numeric value
            numeric_match = re.search(r'\d+\.?\d*', value_text)
            if numeric_match:
                return float(numeric_match.group(0)) * multiplier
        except:
            pass

        return None

    def _extract_fiscal_year(self, soup):
        """Extract fiscal year from document"""
        # Look for fiscal year end date
        fiscal_year_patterns = [
            r'fiscal\s+year\s+end(?:ed|ing)?\s+(?:on)?\s*(\w+\s+\d{1,2},?\s+\d{4})',
            r'for\s+the\s+(?:fiscal\s+)?year\s+end(?:ed|ing)?\s+(?:on)?\s*(\w+\s+\d{1,2},?\s+\d{4})',
            r'(?:as\s+of|ended)\s+(\w+\s+\d{1,2},?\s+\d{4})'
        ]

        text = soup.get_text()
        for pattern in fiscal_year_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    # Attempt to parse the date
                    date_text = match.group(1).strip()
                    date = datetime.strptime(date_text, '%B %d, %Y')
                    return date.strftime('%Y-%m-%d')
                except:
                    pass

        # Fall back to extracting any date format from metadata
        for meta in soup.find_all('meta'):
            if meta.get('name') == 'documentdate' or meta.get('name') == 'period':
                date_text = meta.get('content', '')
                try:
                    # Try to parse YYYY-MM-DD format
                    date = datetime.strptime(date_text, '%Y-%m-%d')
                    return date.strftime('%Y-%m-%d')
                except:
                    pass

        return None

    def _extract_filing_date(self, soup):
        """Extract filing date from document"""
        # Look for filing date in the document
        for meta in soup.find_all('meta'):
            if meta.get('name') == 'filing-date':
                return meta.get('content')

        # Try to find it in the text
        filing_date_patterns = [
            r'filed(?:\s+on)?:\s*(\w+\s+\d{1,2},?\s+\d{4})',
            r'date\s+of\s+report[^:]*:\s*(\w+\s+\d{1,2},?\s+\d{4})'
        ]

        text = soup.get_text()
        for pattern in filing_date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    date_text = match.group(1).strip()
                    date = datetime.strptime(date_text, '%B %d, %Y')
                    return date.strftime('%Y-%m-%d')
                except:
                    pass

        return None

# Store cache of results
if not os.path.exists('cache'):
    os.makedirs('cache')

def save_to_cache(ticker, data):
    """Save data to cache file"""
    cache_file = f"cache/{ticker.upper()}.json"
    with open(cache_file, 'w') as f:
        json.dump(data, f)

def load_from_cache(ticker):
    """Load data from cache if exists"""
    cache_file = f"cache/{ticker.upper()}.json"
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    ticker = request.form.get('ticker', '').strip()

    if not ticker:
        return jsonify({"error": "Please enter a valid ticker symbol"})

    # Check cache first
    cached_data = load_from_cache(ticker)
    if cached_data:
        return jsonify(cached_data)

    # Create scraper and analyze ticker
    scraper = EdgarScraper()

    # Search for company
    cik, error = scraper.search_company(ticker)
    if error:
        return jsonify({"error": error})

    # Get recent 10-K URL
    doc_url, error = scraper.get_recent_10k_url(cik)
    if error:
        return jsonify({"error": error})

    # Extract financial data
    metrics, error = scraper.extract_financial_data(doc_url)
    if error:
        return jsonify({"error": error})

    # Add source URL to metrics
    metrics['source_url'] = doc_url
    metrics['ticker'] = ticker.upper()

    # Save to cache
    save_to_cache(ticker, metrics)

    return jsonify(metrics)

if __name__ == '__main__':
    app.run(debug=True)