#!/usr/bin/env python
# -*- coding: utf-8 -*-
from quantTradingAlgorithm.main import SimpleCalculator
import quantTradingAlgorithm.main as QTA
from quantTradingAlgorithm.main import ClassifyBar
import math as m
from pandas_datareader import data
import pandas as pd
import datetime as dt
import filecmp
import os
# from quantTradingAlgorithm.main import RetrieveData
# from quantTradingAlgorithm.main import FormatData
# from quantTradingAlgorithm.main import ConsolidateBar

################################
# Unit Tests (ClassifyBar)
################################

def test_bar_is_not_green():
    bar = ClassifyBar(5.0, 4.0, 6.0, 2.0, 60000)
    result = bar.polarity()

    assert result == False

def test_bar_has_bottoming_tail():
    # check for bottoming tail green bar
    bar = ClassifyBar(4.0, 5.3, 5.35, 3.99, 50000)
    result = bar.bottom_tail()
    assert m.isclose(result, 0.01)

def test_bar_has_bottoming_tail2():
    # check for bottoming tail red bar
    bar = ClassifyBar(7.5, 3.6, 7.9, 3.2, 60000)
    result = bar.bottom_tail()
    assert m.isclose(result, 0.4)

def test_bar_has_no_bottoming_tail():
    # check for bottoming tail 
    bar = ClassifyBar(6.8, 2.2, 6.8, 2.2, 50000)
    result = bar.bottom_tail()
    assert m.isclose(result, 0)

def test_bar_has_topping_tail():
    # check for topping tail
    bar = ClassifyBar(4.0, 5.3, 5.31, 3.5, 50000)
    result = bar.top_tail()
    assert m.isclose(result, 0.01)

def test_bar_has_no_topping_tail():
    # check for topping tail green bar
    bar = ClassifyBar(4.0, 5.3, 5.3, 3.5, 50000)
    result = bar.top_tail()
    assert result == 0

def test_bar_is_doji():
    bar = ClassifyBar(4.0, 4.002, 6.2, 3.5, 50000)
    result = bar.is_doji()
    assert result == True

def test_bar_is_not_doji():
    bar = ClassifyBar(4.0, 5.1, 6.2, 3.5, 50000)
    result = bar.is_doji()
    assert result == False

def test_bar_is_wide_range():
     # definition of wide range based on large difference between open/close, relative to surrounding bars
     # larger than the last 3 bars and at least twice the average sized bar
    bars = []
    bars.append(ClassifyBar(4.0, 5.3, 5.35, 3.99, 50000))
    bars.append(ClassifyBar(5.3, 6.4, 7.6, 3.25, 45000))
    bars.append(ClassifyBar(6.4, 5.7, 6.80, 5.6, 37000))
    bars.append(ClassifyBar(5.6, 5.23, 5.71, 5.10, 54000))
    bars.append(ClassifyBar(5.25, 5.58, 5.71, 5.10, 48000))

    bar = ClassifyBar(5.9, 9.2, 9.2, 5.2, 66000)
    result = bar.is_wide_range(bars)
    assert result == True

def test_bar_has_volume_spike():
    bars = []
    bars.append(ClassifyBar(4.0, 5.3, 5.35, 3.99, 50000))
    bars.append(ClassifyBar(5.3, 6.4, 7.6, 3.25, 45000))
    bars.append(ClassifyBar(6.4, 5.7, 6.80, 5.6, 37000))
    bars.append(ClassifyBar(5.6, 5.23, 5.71, 5.10, 54000))
    bars.append(ClassifyBar(5.25, 5.58, 5.71, 5.10, 48000))

    bar = ClassifyBar(5.9, 9.2, 9.2, 5.2, 100000)
    result = bar.is_volume_spike(bars)    
    assert result == True

def test_bar_is_igniting_move():
    # check for volume spike, wide range, and breaking through pivot (support/resistance) 
    bars = []
    bars.append(ClassifyBar(4.0, 5.3, 5.35, 3.99, 50000))
    bars.append(ClassifyBar(5.3, 6.4, 7.6, 3.25, 45000))
    bars.append(ClassifyBar(6.4, 5.7, 6.80, 5.6, 37000))
    bars.append(ClassifyBar(5.6, 5.23, 5.71, 5.10, 54000))
    bars.append(ClassifyBar(5.25, 5.58, 5.71, 5.10, 48000))

    bar = ClassifyBar(5.9, 9.2, 9.2, 5.2, 100000)
    result = bar.is_igniting_move(bars, 8.5)
    assert result == True

def test_bar_is_not_igniting_move_volume():
    # check for volume spike, wide range, and breaking through pivot (support/resistance) 
    bars = []
    bars.append(ClassifyBar(4.0, 5.3, 5.35, 3.99, 50000))
    bars.append(ClassifyBar(5.3, 6.4, 7.6, 3.25, 45000))
    bars.append(ClassifyBar(6.4, 5.7, 6.80, 5.6, 37000))
    bars.append(ClassifyBar(5.6, 5.23, 5.71, 5.10, 54000))
    bars.append(ClassifyBar(5.25, 5.58, 5.71, 5.10, 48000))

    bar = ClassifyBar(5.9, 9.2, 9.2, 5.2, 54000)
    result = bar.is_igniting_move(bars, 8.50, 3.50)
    assert result == False

def test_bar_is_not_igniting_move_resistance():
    # check for volume spike, wide range, and breaking through pivot (support/resistance) 
    bars = []
    bars.append(ClassifyBar(4.0, 5.3, 5.35, 3.99, 50000))
    bars.append(ClassifyBar(5.3, 6.4, 7.6, 3.25, 45000))
    bars.append(ClassifyBar(6.4, 5.7, 6.80, 5.6, 37000))
    bars.append(ClassifyBar(5.6, 5.23, 5.71, 5.10, 54000))
    bars.append(ClassifyBar(5.25, 5.58, 5.71, 5.10, 48000))

    bar = ClassifyBar(5.9, 9.2, 9.2, 5.2, 54000)
    result = bar.is_igniting_move(bars, 10.00, 3.50)
    assert result == False


def test_bar_is_ending_move():
    # check for volume spike, wide range, and failing at pivot (support/resistance)
    bars = []
    bars.append(ClassifyBar(4.0, 5.3, 5.35, 3.99, 50000))
    bars.append(ClassifyBar(5.3, 6.4, 7.6, 3.25, 45000))
    bars.append(ClassifyBar(6.4, 5.7, 6.80, 5.6, 37000))
    bars.append(ClassifyBar(5.6, 5.23, 5.71, 5.10, 54000))
    bars.append(ClassifyBar(5.25, 5.13, 5.71, 5.10, 48000))
    
    bar = ClassifyBar(5.12, 2.50, 5.22, 2.50, 100000)
    result = bar.is_ending_move(bars, 2.4, 8.5)
    assert result == True

def test_bar_is_ending_move():
    # check for volume spike, wide range, and failing at pivot (support/resistance)
    bars = []
    bars.append(ClassifyBar(4.0, 5.3, 5.35, 3.99, 50000))
    bars.append(ClassifyBar(5.3, 6.4, 7.6, 3.25, 45000))
    bars.append(ClassifyBar(6.4, 5.7, 6.80, 5.6, 37000))
    bars.append(ClassifyBar(5.6, 5.23, 5.71, 5.10, 54000))
    bars.append(ClassifyBar(5.25, 5.13, 5.71, 5.10, 48000))
    
    bar = ClassifyBar(5.12, 2.50, 5.22, 2.50, 100000)
    result = bar.is_ending_move(bars, 2.4, 8.5)
    assert result == True

################################
# Unit Tests (RetrieveData)
################################
def test_read_data_from_yahoo():
    #checks to make sure the dataframe is returned
    start = dt.datetime(2018, 1, 1)
    end = dt.datetime(2020, 6, 2)

    result = QTA.get_data('AAPL', start, end)

    assert (result.empty == False)

def test_input_start_date_is_valid():
    start = dt.datetime(2018, 1, 5)
    end = dt.datetime(2020, 6, 2)
    result = QTA.get_data('AAPL', start, end)

    assert (result.iloc[0].name == dt.datetime(2018, 1, 5))

def test_input_end_date_is_valid():
    start = dt.datetime(2018, 1, 1)
    end = dt.datetime(2020, 6, 2)
    result = QTA.get_data('AAPL', start, end)

    assert (result.iloc[-1].name == dt.datetime(2020, 6, 2))

def test_output_to_csv():
    #Makes a data_frame from tsla, prints it to a csv and compares 
    #to existing one
    start = dt.datetime(2018, 1, 1)
    end = dt.datetime(2020, 6, 2)
    F1 = "tests/AAPL_correct.csv"

    result = QTA.get_data('AAPL', start, end)
    QTA.make_csv(result, 'AAPL')
    F2 = "AAPL.csv"

    assert filecmp.cmp(F1, F2)
    os.remove("AAPL.csv")

def test_df_to_bar_list():

    i = 0
    start = dt.datetime(2019, 1, 2)
    end = dt.datetime(2020, 6, 2)
    result = QTA.get_data('AAPL', start, end)

    bars = QTA.create_bar_list(result)
    for i in range(len(bars)):
        print(bars[i].open)

    assert True

################################
# Unit Tests (FormatData)
################################

# def test_map_dates():
#     assert result == True

# def test_drop_missing_values():
#     assert result == True

# def test_reset_index():
#     assert result == True


################################
# Unit Tests (ConsolidateBar)
################################

# def test_resample_bar_data():
#     assert result == True

# def test_oversample_bar_data():
#     assert result == True

# def test_combine_two_bars():
#     assert result == True

################################
# Unit Tests (ClassifyTrend)
################################
################################
# Unit Tests (ClassifyMovingAverage)
################################
################################
# Unit Tests (ClassifyBullish)
################################
################################
# Unit Tests (ClassifyBearish)
################################
################################
# Unit Tests (ClassifyRetracement)
################################
################################
# Unit Tests (ClassifyMove)
################################
################################
# Unit Tests (FindGap)
################################
################################
# Unit Tests (FindResistance)
################################
################################
# Unit Tests (FindSupport)
################################
################################
# Unit Tests (DefinePattern)
################################
################################
# Unit Tests (FindPattern)
################################
################################
# Unit Tests (ClassifyBullish)
################################
################################

# Simple Calculator Tests (for reference to better understand TDD/BDD)

def test_add_two_numbers():
    calculator = SimpleCalculator()
    result = calculator.add(4, 5)
    assert result == 9

def test_subtract_two_numbers():
    calculator = SimpleCalculator()
    result = calculator.subtract(4, 5)
    assert result == -1

def test_add_three_numbers():
    calculator = SimpleCalculator()
    result = calculator.add(4, 5, 6)
    assert result == 15
   
def test_add_many_numbers():
    calculator = SimpleCalculator()
    numbers = range(100)
    
    result = calculator.add(*numbers)
    assert result == 4950

