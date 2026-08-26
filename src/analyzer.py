import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

class COVIDDataAnalyzer:
    """Performs analysis on COVID-19 data."""
    
    def __init__(self):
        self.data = None
    
    def load_data(self, df: pd.DataFrame):
        """Load a DataFrame for analysis."""
        self.data = df.copy()
    
    def get_summary_stats(self) -> Dict:
        """Calculate basic summary statistics."""
        if self.data is None:
            return {}
        
        # For time series data, calculate latest values
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            latest_data = self.data[numeric_cols].iloc[-1] if len(self.data) > 0 else pd.Series()
            return {
                'total_cases': latest_data.sum() if len(latest_data) > 0 else 0,
                'max_daily_increase': self.data[numeric_cols].diff().sum().max() if len(self.data) > 1 else 0,
                'days_tracked': len(self.data)
            }
        return {}
    
    def calculate_growth_rate(self, column_name: str) -> pd.Series:
        """Calculate day-over-day growth rate for a column."""
        if self.data is None or column_name not in self.data.columns:
            return pd.Series()
        
        # Calculate percentage change
        growth_rate = self.data[column_name].pct_change() * 100
        return growth_rate
    
    def get_top_countries(self, n: int = 10) -> pd.DataFrame:
        """Get top N countries by latest total cases."""
        if self.data is None:
            return pd.DataFrame()
        
        # Assuming columns are dates and we want to sum across dates for each country/region
        # This is a simplified version - actual implementation would depend on data structure
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            # Sum across time to get total per region (if data is in wide format)
            totals = self.data[numeric_cols].sum()
            top_n = totals.nlargest(n)
            return pd.DataFrame({'region': top_n.index, 'total_cases': top_n.values})
        return pd.DataFrame()