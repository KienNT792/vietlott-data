#!/usr/bin/env python3
"""
Main entry point for Vietlott Power 6/55 data collection and prediction system.
"""

import pandas as pd
from pathlib import Path
from loguru import logger

from src.vietlott.config.products import power655_config
from src.vietlott.crawler.products import ProductPower655
from src.vietlott.model.strategy.frequency import FrequencyStrategy


def main():
    """Main function to run Power 6/55 data collection and analysis."""
    logger.info("Starting Power 6/55 data collection and analysis")
    
    # Initialize Power 6/55 crawler
    power655_crawler = ProductPower655()
    
    # Load existing data or create empty dataframe
    data_file = power655_config.raw_path
    if data_file.exists():
        # Load existing data from JSONL file
        df = pd.read_json(data_file, lines=True)
        logger.info(f"Loaded {len(df)} existing records")
    else:
        logger.info("No existing data found, starting fresh")
        df = pd.DataFrame()
    
    # Run analysis if we have data
    if len(df) > 0:
        # Initialize frequency strategy for prediction
        frequency_strategy = FrequencyStrategy(df)
        
        # Perform backtest
        frequency_strategy.backtest()
        results = frequency_strategy.evaluate()
        
        logger.info(f"Analysis results: {results}")
        
        # Generate prediction for next draw
        latest_date = df['date'].max()
        prediction = frequency_strategy.predict(latest_date)
        logger.info(f"Prediction for next draw: {prediction}")
    
    logger.info("Power 6/55 analysis completed")


if __name__ == "__main__":
    main()
