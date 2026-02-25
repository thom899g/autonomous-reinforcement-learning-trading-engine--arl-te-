"""
Configuration module for ARL_TE.
Centralized configuration with validation and environment variable handling.
Architecture Choice: Centralized config prevents scattered magic numbers and enables easy hot-reloading.
"""
import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from dotenv import load_dotenv
import logging

# Load environment variables first
load_dotenv()

@dataclass
class ExchangeConfig:
    """Exchange-specific configuration with validation"""
    name: str
    api_key: Optional[str] = None
    secret: Optional[str] = None
    sandbox: bool = True  # Default to sandbox for safety
    rate_limit: int = 1000
    timeout: int = 30000
    
    def __post_init__(self):
        """Validate configuration on initialization"""
        if not self.name:
            raise ValueError("Exchange name cannot be empty")
        if not self.sandbox and (not self.api_key or not self.secret):
            logging.warning(f"Live trading enabled for {self.name} but API credentials missing")

@dataclass
class RLConfig:
    """Reinforcement Learning hyperparameters"""
    learning_rate: float = 0.001
    discount_factor: float = 0.99
    exploration_rate: float = 0.1
    batch_size: int = 32
    memory_size: int = 10000
    update_frequency: int = 100
    
    def validate(self) -> List[str]:
        """Validate RL parameters"""
        warnings = []
        if not 0 < self.learning_rate < 1:
            warnings.append(f"Learning rate {self.learning_rate} outside recommended range (0,1)")
        if not 0 <= self.exploration_rate <= 1:
            warnings.append(f"Exploration rate {self.exploration_rate} must be in [0,1]")
        return warnings

@dataclass
class RiskConfig:
    """Risk management configuration"""
    max_position_size: float = 0.1  # 10% of portfolio per trade
    max_daily_loss: float = 0.02  # 2% max daily loss
    stop_loss_pct: float = 0.02  # 2% stop loss
    take_profit_pct: float = 0.05  # 5% take profit
    max_leverage: float = 3.0
    correlation_threshold: float = 0.7
    
    def calculate_position_size(self, portfolio_value: float, volatility: float) -> float:
        """Calculate position size based on volatility-adjusted risk"""
        if volatility <= 0:
            return 0
        risk_adjusted_size = self.max_position_size / volatility
        return min(risk_adjusted_size * portfolio_value, 
                  portfolio_value * self.max_position_size)

class ARLTEConfig