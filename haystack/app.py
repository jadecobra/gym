import flask
import requests
import bs4
import re
import pandas
import json
import os
import datetime

app = flask.Flask(__name__)

class EdgarScraper:
    BASE_URL = "https://www.sec.gov/Archives"
    HEADERS = {"User-Agent": "Stock Analyzer App email@example.com"}  # Replace with your email

    def __init__(self):
        self.base_url = EdgarScraper.BASE_URL
        self.headers = EdgarScraper.HEADERS

    def _fetch_json(self, url):
        """Atomically fetches JSON data from a URL and returns the parsed JSON or None."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")  # Log the error
            return None

    def _extract_text(self, soup):
        """Atomically extracts all text from a BeautifulSoup object."""
        return soup.get_text()

    def _find_in_soup(self, soup, selector):
        """Atomically finds an element in BeautifulSoup using a CSS selector or tag name."""
        return soup.find(selector)

    def _find_all_in_soup(self, soup, selector):
        """Atomically finds all elements in BeautifulSoup using a CSS selector or tag name."""
        return soup.find_all(selector)

    def _parse_date(self, date_string, formats=('%B %d, %Y', '%Y-%m-%d')):
        """Atomically parses a date string with multiple formats."""
        for fmt in formats:
            try:
                return datetime.datetime.strptime(date_string, fmt).strftime('%Y-%m-%d')
            except (ValueError, TypeError):
                pass  # Try the next format
        return None

    def _parse_financial_value(self, value_text):
        """Atomically parses a financial value string to a float."""

        if not isinstance(value_text, str):
            return None

        try:
            value_text = re.sub(r'[\$£€,]', '', value_text)
            multiplier = 1
            if 'billion' in value_text.lower() or 'b' in value_text.lower():
                multiplier = 1_000_000_000
                value_text = re.sub(r'billion|b', '', value_text, flags=re.IGNORECASE)
            elif 'million' in value_text.lower() or 'm' in value_text.lower():
                multiplier = 1_000_000
                value_text = re.sub(r'million|m', '', value_text, flags=re.IGNORECASE)

            numeric_match = re.search(r'\d+\.?\d*', value_text)
            if numeric_match:
                return float(numeric_match.group(0)) * multiplier
            return None
        except (ValueError, TypeError):
            return None

    def _extract_value_from_table(self, soup, keywords):
        """Atomically extracts a value from a table in the soup."""

        for keyword in keywords:
            for table in self._find_all_in_soup(soup, 'table'):
                for row in self._find_all_in_soup(table, 'tr'):
                    cells = self._find_all_in_soup(row, ['td', 'th'])
                    for i, cell in enumerate(cells):
                        if cell.text and keyword.lower() in cell.text.lower():
                            if i + 1 < len(cells) and cells[i + 1].text:
                                return self._parse_financial_value(cells[i + 1].text.strip())
        return None

    def _extract_value_from_text(self, soup, keywords):
        """Atomically extracts a value from text in the soup."""

        text = self._extract_text(soup)
        for keyword in keywords:
            value_match = re.search(r'[\$£€]?\s?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s?(?:million|billion|m|b)?', text, re.IGNORECASE)
            if value_match:
                return self._parse_financial_value(value_match.group(0))
        return None

    def _extract_value(self, soup, keywords):
        """Atomically extracts a financial value from the soup, trying table and text."""

        value = self._extract_value_from_table(soup, keywords)
        if value is not None:
            return value
        return self._extract_value_from_text(soup, keywords)

    def search_company(self, ticker):
        """Search for company by ticker and retrieve CIK number."""

        companies = self._fetch_json("https://www.sec.gov/files/company_tickers.json")
        if companies is None:
            return None, "Error fetching company tickers"

        cik = None
        for _, company in companies.items():
            if company['ticker'].upper() == ticker.upper():
                cik = str(company['cik_str']).zfill(10)
                break

        if not cik:
            return None, f"Company with ticker {ticker} not found"
        return cik, None

    def get_recent_10k_url(self, cik):
        """Get the most recent 10-K filing URL for a company."""

        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        data = self._fetch_json(url)
        if data is None:
            return None, f"Error fetching submission data for CIK {cik}"

        recent_filings = data.get('filings', {}).get('recent', {})
        if not recent_filings:
            return None, "No recent filings found"

        form_types = recent_filings.get('form', [])
        filing_dates = recent_filings.get('filingDate', [])
        accession_numbers = recent_filings.get('accessionNumber', [])

        for i, form_type in enumerate(form_types):
            if form_type == '10-K':
                accession_number = accession_numbers[i].replace('-', '')
                filing_date = filing_dates[i]

                filing_details_url = f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{accession_number}/index.json"
                details_data = self._fetch_json(filing_details_url)
                if details_data is None:
                    return None, f"Error fetching filing details for {filing_details_url}"

                for filing in details_data.get('directory', {}).get('item', []):
                    if filing.get('name', '').endswith('.htm') and not filing.get('name', '').startswith('R'):
                        return f"{self.base_url}/edgar/data/{cik.lstrip('0')}/{accession_number}/{filing['name']}", None
        return None, "No 10-K filing found"

    def extract_company_name(self, soup):
        """Atomically extracts the company name from the BeautifulSoup object."""

        company_name_tag = self._find_in_soup(soup, 'company-name')
        if company_name_tag:
            return company_name_tag.text

        title_tag = self._find_in_soup(soup, 'title')
        if title_tag:
            return title_tag.text.split('|')[0].strip()
        return "Unknown"

    def extract_financial_data(self, doc_url):
        """Extract financial data from 10-K document."""

        response = requests.get(doc_url, headers=self.headers)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        metrics = {
            'company_name': self.extract_company_name(soup),
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

        metrics['equity'] = metrics['total_assets'] - metrics['total_liabilities'] if metrics['total_assets'] and metrics['total_liabilities'] else self._extract_value(soup, ['total equity', 'stockholders equity', 'shareholders equity'])
        metrics['profit_margin'] = round((metrics['net_income'] / metrics['revenue']) * 100, 2) if metrics['revenue'] and metrics['net_income'] else None
        metrics['return_on_assets'] = round((metrics['net_income'] / metrics['total_assets']) * 100, 2) if metrics['total_assets'] and metrics['net_income'] else None
        metrics['return_on_equity'] = round((metrics['net_income'] / metrics['equity']) * 100, 2) if metrics['equity'] and metrics['net_income'] else None
        metrics['debt_to_assets_ratio'] = round(metrics['total_liabilities'] / metrics['total_assets'], 2) if metrics['total_assets'] and metrics['total_liabilities'] else None

        return metrics, None

    def _extract_fiscal_year(self, soup):
        """Extract fiscal year from document."""

        text = self._extract_text(soup)
        fiscal_year_patterns = [
            r'fiscal\s+year\s+end(?:ed|ing)?\s+(?:on)?\s*(\w+\s+\d{1,2},?\s+\d{4})',
            r'for\s+the\s+(?:fiscal\s+)?year\s+end(?:ed|ing)?\s+(?:on)?\s*(\w+\s+\d{1,2},?\s+\d{4})',
            r'(?:as\s+of|ended)\s+(\w+\s+\d{1,2},?\s+\d{4})'
        ]

        for pattern in fiscal_year_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_string = match.group(1).strip()
                parsed_date = self._parse_date(date_string, ['%B %d, %Y'])
                if parsed_date:
                    return parsed_date

        for meta in self._find_all_in_soup(soup, 'meta'):
            if meta.get('name') == 'documentdate' or meta.get('name') == 'period':
                date_string = meta.get('content', '')
                parsed_date = self._parse_date(date_string, ['%Y-%m-%d'])
                if parsed_date:
                    return parsed_date
        return None

    def _extract_filing_date(self, soup):
        """Extract filing date from document."""

        for meta in self._find_all_in_soup(soup, 'meta'):
            if meta.get('name') == 'filing-date':
                return meta.get('content')

        text = self._extract_text(soup)
        filing_date_patterns = [
            r'filed(?:\s+on)?:\s*(\w+\s+\d{1,2},?\s+\d{4})',
            r'date\s+of\s+report[^:]*:\s*(\w+\s+\d{1,2},?\s+\d{4})'
        ]

        for pattern in filing_date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_string = match.group(1).strip()
                parsed_date = self._parse_date(date_string, ['%B %d, %Y'])
                if parsed_date:
                    return parsed_date
        return None

# Caching Functions
def _get_cache_dir():
    """Atomically gets the cache directory, creating it if it doesn't exist."""
    cache_dir = 'cache'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    return cache_dir

def save_to_cache(ticker, data):
    """Atomically saves data to a cache file."""

    cache_file = os.path.join(_get_cache_dir(), f"{ticker.upper()}.json")
    with open(cache_file, 'w') as f:
        json.dump(data, f)

def load_from_cache(ticker):
    """Atomically loads data from a cache file if it exists, otherwise returns None."""

    cache_file = os.path.join(_get_cache_dir(), f"{ticker.upper()}.json")
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return None

# Flask Routes
@app.route('/')
def index():
    """Atomically renders the index page."""
    return flask.render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Atomically analyzes a stock ticker and returns financial data."""

    ticker = flask.request.form.get('ticker', '').strip()
    if not ticker:
        return flask.jsonify({"error": "Please enter a valid ticker symbol"})

    cached_data = load_from_cache(ticker)
    if cached_data:
        return flask.jsonify(cached_data)

    scraper = EdgarScraper()
    cik, error = scraper.search_company(ticker)
    if error:
        return flask.jsonify({"error": error})

    doc_url, error = scraper.get_recent_10k_url(cik)
    if error:
        return flask.jsonify({"error": error})

    metrics, error = scraper.extract_financial_data(doc_url)
    if error:
        return flask.jsonify({"error": error})

    metrics['source_url'] = doc_url
    metrics['ticker'] = ticker.upper()

    save_to_cache(ticker, metrics)
    return flask.jsonify(metrics)

if __name__ == '__main__':
    app.run(debug=True)