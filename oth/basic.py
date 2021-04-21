"""
All the supporting functions for the graph to work
"""


# import torch

class Eye:

    def __init__(self, *size, format:str = 'rgb'):
        """
        size: 3 channels or four channels
        format: 'rgb', 'hsv', ...
        """
        print('size:', size)
        print('format:', format)
        """
        Image -> edges, black_n_white, other color spaces, ...
        then feature importance analysis to get the weights to assign
        to each one
        """



if __name__ == "__main__":
    # eye = Eye(16,45,78,45)
    # eye2 = Eye(1,2,3, format='hsv')
    pass
