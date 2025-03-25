# Research

# Earnings Transcript Downloader

A simple Python application to download earnings transcripts for companies.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file:
   - Copy `.env.example` to `.env`
   - Add your API key from [API Ninjas](https://api-ninjas.com/) to the `.env` file
   - Keep your `.env` file private and never commit it to version control

3. Configure the API endpoint:
   - Open `earnings_transcript_downloader.py`
   - Replace `YOUR_API_BASE_URL` with your actual API base URL
   - Update the API endpoint and parameters in the `get_company_transcripts` method according to your API documentation

## Usage

Run the application:
```bash
python earnings_transcript_downloader.py
```

- Enter a company name when prompted
- The application will download the earnings transcripts and save them in JSON format in the `transcripts` directory
- Enter 'quit' to exit the application

## Output

Transcripts are saved in the `transcripts` directory with filenames in the format:
`company_name_YYYYMMDD_HHMMSS.json`
