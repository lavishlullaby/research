import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

class EarningsTranscriptDownloader:
    def __init__(self):
        self.api_key = os.getenv('API_KEY')
        if not self.api_key:
            raise ValueError("API_KEY not found in environment variables")
        self.base_url = "https://api.api-ninjas.com/v1/earningstranscript"
        
    def get_company_transcript(self, ticker, year, quarter):
        """
        Fetch earnings transcript for a given company, year, and quarter
        """
        try:
            headers = {
                "X-Api-Key": self.api_key
            }
            
            # Print debug information
            print(f"Using API Key: {self.api_key[:5]}...") # Only print first 5 chars for security
            print(f"Headers being sent: {headers}")
            
            api_url = f'{self.base_url}?ticker={ticker}&year={year}&quarter={quarter}'
            print(f"Requesting URL: {api_url}")
            
            response = requests.get(api_url, headers=headers)
            
            # Add more detailed error handling
            if response.status_code != requests.codes.ok:
                print(f"Full response: {response.text}")
                print(f"Response headers: {response.headers}")
                response.raise_for_status()
            
            # Add a small delay to avoid rate limiting
            time.sleep(1)
            
            # Check if the response is empty or invalid
            if not response.text:
                return None
                
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching transcript for {ticker} {year} Q{quarter}: {e}")
            return None
    
    def save_transcript(self, data, ticker, year, quarter):
        """
        Save transcript data to a JSON file
        """
        if not data:
            return False
            
        # Create a directory for transcripts if it doesn't exist
        os.makedirs("transcripts", exist_ok=True)
        
        # Generate filename with year and quarter
        filename = f"transcripts/{ticker}_{year}_Q{quarter}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Transcript saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving transcript: {e}")
            return False

    def download_all_transcripts(self, ticker):
        """
        Download all available transcripts for a company from 2000 to current year
        """
        current_year = datetime.now().year
        current_quarter = (datetime.now().month - 1) // 3 + 1
        
        for year in range(2000, current_year + 1):
            # For the current year, only download up to the current quarter
            max_quarter = 4 if year < current_year else current_quarter
            
            for quarter in range(1, max_quarter + 1):
                print(f"\nFetching transcript for {ticker} {year} Q{quarter}...")
                transcript = self.get_company_transcript(ticker, year, quarter)
                
                if transcript:
                    if self.save_transcript(transcript, ticker, year, quarter):
                        print(f"Successfully downloaded and saved transcript for {year} Q{quarter}")
                    else:
                        print(f"Failed to save transcript for {year} Q{quarter}")
                else:
                    print(f"No transcript available for {year} Q{quarter}")

def main():
    try:
        downloader = EarningsTranscriptDownloader()
        
        while True:
            ticker = input("\nEnter company ticker symbol (or 'quit' to exit): ").upper()
            
            if ticker.lower() == 'quit':
                break
                
            print(f"\nStarting download of all available transcripts for {ticker}...")
            downloader.download_all_transcripts(ticker)
            print(f"\nCompleted downloading transcripts for {ticker}")
                
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 