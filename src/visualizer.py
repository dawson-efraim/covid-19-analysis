import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Optional

class COVIDDataVisualizer:
    """Creates visualizations for COVID-19 data."""
    
    def __init__(self, style: str = 'seaborn-v0_8'):
        plt.style.use(style)
        self.fig_size = (12, 8)
    
    def plot_time_series(self, data: pd.DataFrame, title: str = "COVID-19 Cases Over Time", 
                         x_label: str = "Date", y_label: str = "Number of Cases",
                         figsize: tuple = None) -> plt.Figure:
        """Plot time series data."""
        if figsize is None:
            figsize = self.fig_size
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Assuming data has dates as columns and regions as rows
        # We'll plot the sum across regions for each date
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            # Sum across rows (regions) for each date column
            totals = data[numeric_cols].sum()
            ax.plot(totals.index, totals.values, linewidth=2)
            ax.set_title(title, fontsize=16, fontweight='bold')
            ax.set_xlabel(x_label, fontsize=12)
            ax.set_ylabel(y_label, fontsize=12)
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
        
        return fig
    
    def plot_top_countries(self, data: pd.DataFrame, top_n: int = 10, 
                           title: str = None,
                           figsize: tuple = None) -> plt.Figure:
        if title is None:
            title = f"Top {top_n} Countries by Total Cases"
        """Plot a bar chart of top countries by total cases."""
        if figsize is None:
            figsize = self.fig_size
        
        # Calculate totals per region (assuming wide format with dates as columns)
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0 and len(data) > 0:
            totals = data[numeric_cols].sum(axis=1)
            # Get top N countries
            top_data = pd.DataFrame({
                'region': data.index if hasattr(data, 'index') else range(len(data)),
                'total_cases': totals
            }).nlargest(top_n, 'total_cases')
            
            fig, ax = plt.subplots(figsize=figsize)
            bars = ax.bar(range(len(top_data)), top_data['total_cases'])
            ax.set_title(title, fontsize=16, fontweight='bold')
            ax.set_xlabel('Country/Region', fontsize=12)
            ax.set_ylabel('Total Cases', fontsize=12)
            ax.set_xticks(range(len(top_data)))
            ax.set_xticklabels(top_data['region'], rotation=45, ha='right')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height):,}',
                        ha='center', va='bottom')
            
            plt.tight_layout()
            return fig
        return None
    
    def plot_growth_rate(self, data: pd.DataFrame, column_name: str = None,
                         title: str = "Daily Growth Rate (%)",
                         figsize: tuple = None) -> plt.Figure:
        """Plot growth rate over time."""
        if figsize is None:
            figsize = self.fig_size
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # If column_name is not specified, use the first numeric column
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            if column_name is None:
                column_name = numeric_cols[0]
            
            if column_name in data.columns:
                # Calculate day-over-day percentage change
                growth_rate = data[column_name].pct_change() * 100
                ax.plot(data.index if hasattr(data, 'index') else range(len(data)), 
                        growth_rate.values, color='red', linewidth=2)
                ax.set_title(title, fontsize=16, fontweight='bold')
                ax.set_xlabel('Time', fontsize=12)
                ax.set_ylabel('Growth Rate (%)', fontsize=12)
                ax.grid(True, alpha=0.3)
                ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
                plt.xticks(rotation=45)
                plt.tight_layout()
                return fig
        return None
    
    def save_plot(self, fig: plt.Figure, filename: str, dpi: int = 300):
        """Save the figure to a file."""
        fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        print(f"Plot saved as {filename}")