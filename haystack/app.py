import flask
import requests
import re
import json
import os
import datetime
import xbrl
import time

app = flask.Flask(__name__)

# Configure rate limiting: 5 requests per second, 10 requests per 10 seconds, and 1000 requests per day
# Using a dictionary to store request timestamps.  Key is the URL, value is a list of timestamps.
request_log = {}
rate_limits = {
    'second': 5,
    'ten_seconds': 10,
    'day': 1000
}
#Window size for rate limiting
window_sizes = {
    'second': 1,
    'ten_seconds': 10,
    'day': 24 * 60 * 60
}

def check_rate_limit(url):
    """
    Checks if the request for the given URL exceeds the defined rate limits.

    Args:
        url (str): The URL being requested.

    Returns:
        bool: True if the rate limit is exceeded, False otherwise.
    """
    now = time.time()
    if url not in request_log:
        request_log[url] = []

    for interval_name, limit in rate_limits.items():
        window_size = window_sizes[interval_name]
        # Remove requests that are outside the current window
        request_log[url] = [ts for ts in request_log[url] if now - ts <= window_size]
        # Check if the number of requests exceeds the limit
        if len(request_log[url]) >= limit:
            return True  # Rate limit exceeded

    request_log[url].append(now)  # Log the current request
    return False  # Rate limit not exceeded


class EdgarScraper:
    BASE_URL = "https://www.sec.gov/Archives"
    HEADERS = {"User-Agent": "Stock Analyzer App email@example.com"}

    def __init__(self):
        self.base_url = EdgarScraper.BASE_URL
        self.headers = EdgarScraper.HEADERS

    def _fetch_json(self, url):
        """Atomically fetches JSON data from a URL and returns the parsed JSON or None."""
        try:
            # Apply rate limiting before making the request
            if check_rate_limit(url):
                print(f"Rate limit exceeded for {url}")
                return None  # Or raise an exception, or retry after a delay

            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
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
                pass
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
                    if filing.get('name', '').endswith('.xml'):  # Look for the XBRL file
                        return f"{self.base_url}/edgar/data/{cik.lstrip('0')}/{accession_number}/{filing['name']}", None
        return None, "No 10-K XBRL filing found"

    def extract_company_name(self, soup):
        """Atomically extracts the company name from the BeautifulSoup object."""
        company_name_tag = self._find_in_soup(soup, 'company-name')
        if company_name_tag:
            return company_name_tag.text

        title_tag = self._find_in_soup(soup, 'title')
        if title_tag:
            return title_tag.text.split('|')[0].strip()
        return "Unknown"

    def extract_financial_data(self, xbrl_url):
        """Extract financial data from 10-K XBRL document."""
        try:
            # Apply rate limiting
            if check_rate_limit(xbrl_url):
                return None, "Rate limit exceeded"

            # Fetch the XBRL data
            response = requests.get(xbrl_url, headers=self.headers)
            response.raise_for_status()  # Ensure we got a valid response

            # Parse the XBRL document
            xbrl_doc = xbrl.parse(response.content)

            # Get the GAAP context
            gapp_context = None

            # Create a dictionary to hold the extracted data
            metrics = {
                'company_name': self._get_xbrl_value(xbrl_doc, 'dei:EntityRegistrantName', gapp_context) or "Unknown",
                'revenue': self._get_xbrl_value(xbrl_doc, 'us-gaap:RevenueFromContractsWithCustomersExcludingAssessedTax', gapp_context) or self._get_xbrl_value(xbrl_doc, 'us-gaap:SalesRevenueNet', gapp_context),
                'net_income': self._get_xbrl_value(xbrl_doc, 'us-gaap:NetIncomeLoss', gapp_context),
                'total_assets': self._get_xbrl_value(xbrl_doc, 'us-gaap:Assets', gapp_context),
                'total_liabilities': self._get_xbrl_value(xbrl_doc, 'us-gaap:Liabilities', gapp_context),
                'cash_and_equivalents': self._get_xbrl_value(xbrl_doc, 'us-gaap:CashAndCashEquivalentsAtCarryingValue', gapp_context),
                'long_term_debt': self._get_xbrl_value(xbrl_doc, 'us-gaap:LongTermDebt', gapp_context),
                'operating_income': self._get_xbrl_value(xbrl_doc, 'us-gaap:OperatingIncomeLoss', gapp_context),
                'shares_outstanding': self._get_xbrl_value(xbrl_doc, 'dei:EntityCommonStockSharesOutstanding', gapp_context),
                'fiscal_year_end': self._get_xbrl_value(xbrl_doc, 'dei:DocumentPeriodEndDate', gapp_context),
                'filing_date': self._get_xbrl_value(xbrl_doc, 'dei:DocumentFilingDate', gapp_context)
            }

            # Calculate additional metrics
            metrics['equity'] = metrics['total_assets'] - metrics['total_liabilities'] if metrics['total_assets'] and metrics['total_liabilities'] else None
            metrics['profit_margin'] = round((metrics['net_income'] / metrics['revenue']) * 100, 2) if metrics['revenue'] and metrics['net_income'] else None
            metrics['return_on_assets'] = round((metrics['net_income'] / metrics['total_assets']) * 100, 2) if metrics['total_assets'] and metrics['net_income'] else None
            metrics['return_on_equity'] = round((metrics['net_income'] / metrics['equity']) * 100, 2) if metrics['equity'] and metrics['net_income'] else None
            metrics['debt_to_assets_ratio'] = round(metrics['total_liabilities'] / metrics['total_assets'], 2) if metrics['total_assets'] and metrics['total_liabilities'] else None
            metrics['dividends_per_share'] = self._get_xbrl_value(xbrl_doc, 'us-gaap:CommonStockDividendsPerShare', gapp_context)
            metrics['fcf'] = self._get_xbrl_value(xbrl_doc, 'us-gaap:FreeCashFlow', gapp_context)  # Corrected tag
            # Per-share metrics
            shares_outstanding = metrics.get('shares_outstanding')
            if shares_outstanding:
                for key in ['net_income', 'equity', 'total_assets', 'revenue', 'cash_and_equivalents', 'total_liabilities',
                            'long_term_debt']:
                    if metrics.get(key) is not None:
                        metrics[f'{key}_per_share'] = round(metrics[key] / shares_outstanding, 2)
                if metrics.get('fcf') is not None:
                    metrics['fcf_per_share'] = round(metrics['fcf'] / shares_outstanding, 2)
            # net tangible assets per share
            tangible_assets = metrics.get('total_assets') - self._get_xbrl_value(xbrl_doc, 'us-gaap:IntangibleAssetsNet', gapp_context) if metrics.get(
                'total_assets') is not None else None
            if tangible_assets is not None and shares_outstanding is not None:
                metrics['net_tangible_assets_per_share'] = round(
                    (tangible_assets - metrics.get('total_liabilities', 0)) / shares_outstanding,
                    2) if metrics.get('total_liabilities') is not None else None
            else:
                metrics['net_tangible_assets_per_share'] = None
            return metrics, None

        except Exception as e:
            return None, f"Error extracting financial data: {str(e)}"

    def _get_xbrl_value(self, xbrl_doc, tag_name, context_id):
        """
        Helper method to safely extract a value from an XBRL document, given a tag name and context.
        Returns the first non-null value found.
        """
        elements = xbrl_doc.find_all(tag_name)  # Find all elements with the tag_name
        if not elements:
            return None

        for element in elements:
            # Check if the context matches.  If context_id is None, we'll accept any context.
            if context_id is None or element.context_id == context_id:
                text_content = element.text_content()
                try:
                    return self._parse_financial_value(text_content)
                except ValueError:
                    return None  # Handle non-numeric content
        return None

    def _extract_fiscal_year(self, soup):
        """Extract fiscal year from document - Not needed with XBRL"""
        return None

    def _extract_filing_date(self, soup):
        """Extract filing date from document -  Not needed with XBRL"""
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

    xbrl_url, error = scraper.get_recent_10k_url(cik)  # Changed to get XBRL URL
    if error:
        return flask.jsonify({"error": error})

    metrics, error = scraper.extract_financial_data(xbrl_url)  # Pass XBRL URL
    if error:
        return flask.jsonify({"error": error})

    metrics['source_url'] = xbrl_url  # changed to xbrl_url
    metrics['ticker'] = ticker.upper()

    save_to_cache(ticker, metrics)
    return flask.jsonify(metrics)

if __name__ == '__main__':
    app.run(debug=True)
