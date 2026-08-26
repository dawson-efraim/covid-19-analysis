import pandas as pd
import requests
from pathlib import Path

class COVIDDataLoader:
    """Handles loading and preprocessing of COVID-19 data."""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def load_jhu_data(self, url=None):
        """Load Johns Hopkins University COVID-19 data."""
        if url is None:
            url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
        
        try:
            df = pd.read_csv(url)
            return df
        except Exception as e:
            print(f"Error loading JHU data: {e}")
            return None
    
    def load_who_data(self, url=None):
        """Load World Health Organization COVID-19 data."""
        if url is None:
            url = "https://covid19.who.int/WHO-COVID-19-global-table-data.csv"
        
        try:
            df = pd.read_csv(url)
            return df
        except Exception as e:
            print(f"Error loading WHO data: {e}")
            return None
    
    def load_owid_data(self, url=None):
        """Load Our World in Data COVID-19 data."""
        if url is None:
            url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        
        try:
            df = pd.read_csv(url)
            return df
        except Exception as e:
            print(f"Error loading OWID data: {e}")
            return None
    
    def save_data(self, df, filename):
        """Save DataFrame to CSV in the data directory."""
        filepath = self.data_dir / filename
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")