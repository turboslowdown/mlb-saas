import warnings

def suppress_warnings():
    """
    Suppresses common non-critical warnings from libraries like pybaseball
    to keep ETL logs and outputs clean.
    """
    # Catches warnings about deprecated features that are still in use
    warnings.simplefilter("ignore", category=FutureWarning)
    
    # Catches general user warnings, often from underlying libraries in pybaseball
    warnings.simplefilter("ignore", category=UserWarning)