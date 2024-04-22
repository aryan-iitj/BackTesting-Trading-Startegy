from abc import ABC

class tradingAlgo(ABC):
    """
    Abstract base class defining trading algorithm methods
    """
    
    def __init__(self):
        """
        Initialize algorithms by specifying hyperparameters
        """
        pass
    
    def handle_data(self, data):
        """
        Called every time a bar of data is pushed from the backtesting
        or live trading API
        """
        pass