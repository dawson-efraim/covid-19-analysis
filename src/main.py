"""
Main entry point for the COVID-19 data analysis project.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from data_loader import COVIDDataLoader
from analyzer import COVIDDataAnalyzer
from visualizer import COVIDDataVisualizer

def main():
    """Main function to run the COVID-19 analysis."""
    print("=== COVID-19 Data Analysis Project ===\n")
    
    # Initialize components
    loader = COVIDDataLoader()
    analyzer = COVIDDataAnalyzer()
    visualizer = COVIDDataVisualizer()
    
    # Create output directories
    Path("output").mkdir(exist_ok=True)
    Path("output/plots").mkdir(exist_ok=True)
    
    try:
        # Step 1: Load data
        print("1. Loading COVID-19 data...")
        # Try to load JHU data first
        df = loader.load_jhu_data()
        
        if df is None or df.empty:
            print("Failed to load JHU data, trying WHO data...")
            df = loader.load_who_data()
        
        if df is None or df.empty:
            print("Failed to load WHO data, trying OWID data...")
            df = loader.load_owid_data()
        
        if df is None or df.empty:
            print("Error: Could not load any COVID-19 data.")
            return 1
        
        print(f"   Loaded data shape: {df.shape}")
        
        # Save raw data
        loader.save_data(df, "raw_covid_data.csv")
        
        # Step 2: Analyze data
        print("\n2. Analyzing data...")
        analyzer.load_data(df)
        
        # Get summary statistics
        stats = analyzer.get_summary_stats()
        print("   Summary Statistics:")
        for key, value in stats.items():
            print(f"     {key}: {value}")
        
        # Step 3: Create visualizations
        print("\n3. Creating visualizations...")
        
        # Time series plot
        fig1 = visualizer.plot_time_series(
            df, 
            title="Global COVID-19 Confirmed Cases Over Time",
            y_label="Number of Cases"
        )
        if fig1:
            visualizer.save_plot(fig1, "output/plots/time_series.png")
        
        # Growth rate plot (if we have time series data)
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            fig2 = visualizer.plot_growth_rate(
                df,
                column_name=numeric_cols[0] if len(numeric_cols) > 0 else None,
                title="Daily Growth Rate of COVID-19 Cases (%)"
            )
            if fig2:
                visualizer.save_plot(fig2, "output/plots/growth_rate.png")
        
        print("   Visualizations saved to output/plots/")
        
        # Step 4: Generate report
        print("\n4. Generating analysis report...")
        report_path = "output/analysis_report.txt"
        with open(report_path, 'w') as f:
            f.write("COVID-19 Data Analysis Report\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns\n\n")
            f.write("Summary Statistics:\n")
            for key, value in stats.items():
                f.write(f"  {key}: {value}\n")
            f.write("\nVisualizations generated:\n")
            f.write("  - output/plots/time_series.png\n")
            f.write("  - output/plots/growth_rate.png\n")
        
        print(f"   Report saved to {report_path}")
        
        print("\n=== Analysis Complete ===")
        print("Check the 'output' directory for results.")
        
        return 0
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())