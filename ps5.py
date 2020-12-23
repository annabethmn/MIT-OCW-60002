# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import numpy as np
import matplotlib.pyplot as plt
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')
            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return np.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = np.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for deg in degs:
        coeff = np.polyfit(x, y, deg) #generates numpy array with coefficients of best fit polynomial
        models.append(coeff)
    return models


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    #calculate sum of (actual y values - predicted y values)^2
    num = sum((y - estimated)**2)
    #calculate sum of (actual y values - mean)^2
    denom = sum((y - np.mean(y))**2)
    r_squared = 1 - (num/denom)
    return r_squared

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for i in range(len(models)): 
        model = models[i]
        plt.figure(i+1) #ensure that each model is plotted on a different figure
        y_exp = []
        #calculate degree of polynomial 
        degree = len(model) - 1
        for x_val in x: 
            y_val = np.polyval(model, x_val) #evaluate model at x 
            y_exp.append(y_val)
        plt.plot(x, y_exp, 'r') #plot polynomial as a solid red line 
        plt.scatter(x, y, c='b') #scatterplot of actual sample on same figure
        plt.xlabel("Years")
        plt.ylabel("Degrees Celsius")
        r2 = r_squared(y, y_exp)
        title_string = "Change in average annual temperatures over time\n" + "R2: " + str(r2) + "\nDegree: "+ str(degree)
        #include SE/slope for degree 1 polynomials
        if degree == 1:
            se = se_over_slope (x, y, y_exp, model)
            title_string += "\nSE/Slope: " + str(se)
        plt.title(title_string)



        
def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    avg_temps = []
    for year in years:
        national_avg = 0.0 #average yearly temp over all cities
        for city in multi_cities: 
            local_yearly_temp = np.mean(climate.get_yearly_temp(city, year)) #average temp in given city
            national_avg += local_yearly_temp
        national_avg /= len(multi_cities)
        avg_temps.append(national_avg)
    return np.array(avg_temps)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving_averages = []
    for i in range(len(y)):
        if i < (window_length-1): #avoid negative indexing
            moving_average = sum(y[0:i+1]) / (i+1) #compute average of y vals from 0 to i
        else: 
            moving_average = sum(y[(i-window_length+1):i+1]) / window_length #compute average of y vals within window length of i
        moving_averages.append(moving_average)
    return np.array(moving_averages)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    num_array = (y-estimated)**2 #argument of numerator for RMSE function
    return np.sqrt(sum(num_array)/len(num_array))

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    stdev_temps = []
    for year in years:
        national_daily_temps = [] #list of lists of daily temps for each city
        for city in multi_cities: 
            local_daily_temps = climate.get_yearly_temp(city, year) #list of temps of every day in the year
            national_daily_temps.append(local_daily_temps)
    #average the arrays of city temperatures
        national_daily_avg = sum(national_daily_temps) / len(multi_cities)
        national_yearly_stdev = np.std(national_daily_avg)
        stdev_temps.append(national_yearly_stdev)
    return np.array(stdev_temps)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for i in range(len(models)): 
        model = models[i]
        print(model)
        plt.figure(i+1) #ensure that each model is plotted on a different figure
        y_exp = []
        #calculate degree of polynomial 
        degree = len(model) - 1
        for x_val in x: 
            y_val = np.polyval(model, x_val)
            y_exp.append(y_val)
        plt.plot(x, y_exp, 'r') #plot polynomial as a solid red line 
        plt.scatter(x, y, c='b') #scatterplot of actual sample on same figure
        plt.xlabel("Years")
        plt.ylabel("Degrees Celsius")
        RMSE = rmse(y, y_exp)
        title_string = "Change in average annual temperatures over time\n" + "RMSE: " + str(RMSE) + "\nDegree: "+ str(degree)
        plt.title(title_string)
        

if __name__ == '__main__':
    
    # Part A.4
    temp_records = Climate("data.csv")
    years = np.array(TRAINING_INTERVAL)
    avg_temps = [] #average yearly temp in NYC for each year in training interval
    daily_temps = [] #temp from January of each year in NYC
    for year in years:
        yearly_temps = temp_records.get_yearly_temp("NEW YORK", year)
        jan_10_temp = temp_records.get_daily_temp("NEW YORK", 1, 10, year)
        yearly_avg = np.mean(yearly_temps)
        avg_temps.append(yearly_avg)
        daily_temps.append(jan_10_temp)
    avg_temps = np.array(avg_temps) 
    daily_temps = np.array(daily_temps)
    lin_reg_avg = generate_models(years, avg_temps, [1])
    evaluate_models_on_training(years, avg_temps, lin_reg_avg)
    lin_reg_rand = generate_models(years, daily_temps, [1])
    evaluate_models_on_training(years, daily_temps, lin_reg_rand) 
    
    # Part B
    avg_national_temps = gen_cities_avg(temp_records, CITIES, years)
    lin_reg_natl = generate_models(years, avg_national_temps, [1])
    evaluate_models_on_training(years, avg_national_temps, lin_reg_natl)

    # Part C
    national_moving_avg = moving_average(avg_national_temps, 5)
    moving_average_model = generate_models(years, national_moving_avg, [1])
    evaluate_models_on_training(years, national_moving_avg, moving_average_model)
    
    # Part D.2
    #generate models of varying degrees
    moving_average_models = generate_models(years, national_moving_avg,[1,2,20])
    evaluate_models_on_training(years, national_moving_avg, moving_average_models)
    #test data is 2010-2015
    test_years = np.array(TESTING_INTERVAL)
    avg_national_temps_test = gen_cities_avg(temp_records, CITIES, test_years)
    national_moving_avg_test = moving_average(avg_national_temps_test, 5)
    evaluate_models_on_testing(test_years, national_moving_avg_test, moving_average_models)
    
    # Part E
    national_stdevs = gen_std_devs(temp_records, CITIES, years)
    moving_avg_stdev = moving_average(national_stdevs, 5)
    stdev_model = generate_models(years, moving_avg_stdev, [1])
    evaluate_models_on_training(years, moving_avg_stdev, stdev_model)
    
