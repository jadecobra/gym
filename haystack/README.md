# Stock Analyzer App

A Python web application that scrapes 10-K data from the SEC's EDGAR database to analyze financial metrics for publicly traded companies.

## Features

- Enter any stock ticker symbol to retrieve financial data from the latest 10-K filing
- Automatic CIK lookup using SEC's API
- Comprehensive financial metrics extraction:
  - Income Statement: Revenue, Net Income, Operating Income
  - Balance Sheet: Total Assets, Total Liabilities, Equity, Cash, Long-term Debt
  - Financial Ratios: Profit Margin, Return on Assets, Return on Equity, Debt to Assets Ratio
- Caching system to reduce redundant requests
- Modern responsive UI with Bootstrap

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/stock-analyzer-app.git
   cd stock-analyzer-app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install flask requests beautifulsoup4 pandas
   ```

4. Update the User-Agent in `EdgarScraper.__init__` with your email address (SEC requirement):
   ```python
   self.headers = {
       "User-Agent": "Stock Analyzer App your.email@example.com"  # Replace with your email
   }
   ```

5. Create a templates directory and add the provided HTML template:
   ```
   mkdir templates
   # Copy the index.html file to the templates directory
   ```

## Usage

1. Start the application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`

3. Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOG) and click "Analyze 10-K Data"

4. The application will:
   - Look up the company's CIK number
   - Find the most recent 10-K filing
   - Extract and analyze the financial data
   - Display the results in a user-friendly format

## How It Works

### SEC EDGAR Data Retrieval

The application uses the SEC's public APIs to:
1. Convert ticker symbols to CIK numbers
2. Find the most recent 10-K filing for the company
3. Download the filing HTML document

### Financial Data Extraction

The app uses BeautifulSoup to parse the 10-K document and extract financial data using:
- Pattern matching for financial terms
- Table structure analysis
- Text extraction from relevant sections

The extraction process is designed to be robust across different 10-K filing formats.

### Calculated Metrics

The app calculates several financial ratios: