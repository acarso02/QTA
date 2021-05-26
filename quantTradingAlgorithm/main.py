# -*- coding: utf-8 -*-
from pandas_datareader import data
import pandas as pd
import datetime as dt


class ClassifyBar:
    __near = 0.005         #Definition of "close enough" used in is_doji method
    
    def __init__(self, open, close, high, low, volume, date = dt.datetime(2018, 5, 3)):
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.date = date
        self.range = self.get_range()

    def polarity(self):
        """
        Checks the polarity of the bar
        returns: true if green or doji
        """
        if self.open <= self.close:
            return True
        
        return False

    def top_tail(self):
        """
        Checks the size of the top tail 
        :returns: size of top tail, 0 if none (float)
        """
        if(self.open > self.close):
            return self.high - self.open
        else:
            return self.high - self.close

    def bottom_tail(self):
        """
        Checks the size of the bottom tail
        :returns: size of the bottom tail, 0 if none (float)
        """
        if(self.open < self.close):
            return self.open - self.low
        else:
            return self.close - self.low

    def is_doji(self):
        """
        Checks if the open and close prices are the same 
        :returns: True if prices are within range of eachother, false if not
        """
        if  abs(self.open - self.close) < ClassifyBar.__near:
            return True

        return False
    
    def get_range(self):
        """
        :returns: Range from OPEN to CLOSE
        """
        return abs(self.open - self.close)

    def is_wide_range(self, recent_bars = []):
        """
        Checks if the current bar is of wide range
        :params: recent_bars: list of n bars preceding the current bar
        :returns: True if the current bar is larger than the last 3 bars and 
                   two times the mean, false otherwise
        """
        mean = float(0.0)

        for bar in recent_bars:
            mean = mean + bar.get_range()
        mean = mean / len(recent_bars)

        if (self.get_range() >= recent_bars[len(recent_bars)- 1].get_range()
        and self.get_range() >= recent_bars[len(recent_bars) - 2].get_range()
        and self.get_range() >= recent_bars[len(recent_bars) - 3].get_range()
        and self.get_range() >= 2.0 * mean):
                return True

        return False 

    def is_volume_spike(self, recent_bars = []):
        """
        Checks if the current bar is a volume spike 
        :params: recent_bars: list of n bars preceding the current bar
        :returns: True if volume is twice the average of the n bars preceding
                   it, false if not
        """
        mean = float(0.0)

        for bar in recent_bars:
            mean = mean + bar.volume
        mean = mean / len(recent_bars)

        if self.volume >= mean * 2:
            return True

        return False

    def is_igniting_move(self, recent_bars = [], support = 0, resistance = 0):
        """
        Checks if the current bar is an igniting move 
        :params: recent_bars: list of n bars preceding the current bar
        :params: SRLevel: support or resistance level
        :returns: True if criteria met, false if not
        """
        if (self.is_wide_range(recent_bars)
        and self.is_volume_spike(recent_bars)):
            if self.polarity and self.close > resistance:
                return True
            elif self.polarity == False and self.close < support:
                return True
        
        return False


    def is_ending_move(self, recent_bars = [], support = 0, resistance = 0):
        """
        Checks if the current bar is an ending move 
        :params: recent_bars: list of n bars preceding the current bar
        :params: support: support price level
        :params: resistance: resistance price level        
        :returns: True if criteria met, false if not
        """
        if (self.is_wide_range(recent_bars)
        and self.is_volume_spike(recent_bars)):
            if self.polarity and self.close < resistance:
                return True
            elif self.polarity == False and self.close > support:
                return True
        
        return False

def get_data(symbol = 'AAPL', start = dt.datetime(2015, 1, 1), 
    end = dt.datetime(2018, 2, 8)):

    data_frame = data.DataReader(symbol, 'yahoo', start, end)

    return data_frame

def make_csv(data_frame, name):
    data_frame.to_csv(name + '.csv')

def create_bar_list(data_frame):
    """
    Converts a data frame to a list of bars
    :params: data_frame: pandas data frame of stock data
    :returns: List of bars
    """
    output = []
    i = 0
    for i in range(len(data_frame)):
        output.append(ClassifyBar(data_frame.iat[i,2], 
        data_frame.iat[i,3], data_frame.iat[i,0], 
        data_frame.iat[i,1], data_frame.iat[i,4], 
        data_frame.iloc[i].name))
    
    return output
    
# class FormatData:
#     def init():
#         pass

# class ConsolidateBar:
#     def init():
#         pass


# Test Class for Simple Calculator functions to understand TDD/BDD
class SimpleCalculator:
    def add(self,*args):
        return sum(args)
        pass

    def subtract(self,a,b,c=0):
        return a-b-c
        pass