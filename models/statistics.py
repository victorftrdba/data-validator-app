"""Statistics data model."""

from dataclasses import dataclass


@dataclass
class Statistics:
    """Data validation statistics."""
    
    rows: int
    total_value: float
    average_value: float
    
    def to_dict(self) -> dict:
        """Convert statistics to dictionary."""
        return {
            'rows': self.rows,
            'total_val': self.total_value,
            'avg_val': self.average_value
        }

