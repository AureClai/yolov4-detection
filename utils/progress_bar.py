"""
Original
https://stackoverflow.com/questions/48706237/how-to-choose-the-threshold-of-the-output-of-a-dnn-in-tensorflow

et test ajouté par :
aurelien.clairais@cerema.fr
"""

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

if __name__ == "__main__":
    # Ajout 
    import time
    for i in range(1000):
        printProgressBar(i, 1000, prefix = 'Progression', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r")
        # 60 ticks par seconde
        time.sleep(0.015)