import logging

def getLogger(name="",write_to_file=False):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a formatter to define the log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a stream handler to print logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    if write_to_file:
        # Create a file handler to write logs to a file
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(formatter)
        # Add the handlers to the logger
        logger.addHandler(file_handler)

    logger.addHandler(console_handler)

    return logger
