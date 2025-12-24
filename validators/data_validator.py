"""Data validator for processing and validating Parquet files."""

import pandas as pd

from models import Statistics
from utils import get_logger

logger = get_logger(__name__)


class DataValidator:
    """Validator for processing and generating statistics from Parquet data."""
    
    def __init__(self, value_column: str = 'valor_usd'):
        """
        Initialize data validator.
        
        Args:
            value_column: Name of the column containing values to calculate statistics
        """
        self.value_column = value_column
    
    def validate_and_generate_stats(self, df: pd.DataFrame) -> Statistics:
        """
        Validate DataFrame and generate statistics.
        
        Args:
            df: DataFrame to validate and process
            
        Returns:
            Statistics object with validation results
            
        Raises:
            ValueError: If required column is missing or DataFrame is empty
        """
        if df.empty:
            raise ValueError("DataFrame is empty")
        
        if self.value_column not in df.columns:
            raise ValueError(f"Required column '{self.value_column}' not found in DataFrame")
        
        logger.info(f"Validating DataFrame with {len(df)} rows")
        
        # Calculate statistics
        total_value = float(df[self.value_column].sum())
        average_value = float(df[self.value_column].mean())
        
        statistics = Statistics(
            rows=len(df),
            total_value=total_value,
            average_value=average_value
        )
        
        logger.info(
            f"Generated statistics: {statistics.rows} rows, "
            f"total=${statistics.total_value:.2f}, "
            f"avg=${statistics.average_value:.2f}"
        )
        
        return statistics

