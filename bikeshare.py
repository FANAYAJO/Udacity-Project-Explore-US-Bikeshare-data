"""
    File name: test.py
    Author: Fanayajo Oluwasegun
    Date created: 3/16/2021
    Date last modified: 4/18/2021
    Python Version: 3.8
"""

import time
import numpy as np
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city = input('INPUT THE CITY (city available are Chicago, New york city and Washington):  ').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input("CHOOSE BETWEEN chicago, new york city OR washington: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input('ENTER MONTH(e.g January, February etc) or \'all\' to not filter by month: ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'all']:
        month = input('ENTER MONTH january, february, ... , june : ').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('ENTER DAY(e.g monday, friday etc) or \'all\' to not filter by day: ').lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']:
        day = input('Enter day e,g monday, tuesday etc.....')

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load intended file into data frame
    df = pd.read_csv(CITY_DATA[city])
    # pd.set_option("display.max_columns", 6)

    # convert columns od Start Time and End Time into date format yyyy-mm-dd
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month from Start Time into new column called month
    df['month'] = df['Start Time'].dt.month
    # extract day from Start Time into new column called month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # create a day mapper that maps day to corresponding day int(1st day start on sunday)
    day_mapper = {
        'sunday': 1,
        'monday': 2,
        'tuesday': 3,
        'wednesday': 4,
        'thursday': 5,
        'friday': 6,
        'saturday': 7
    }

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day_mapper[day]]

    return df


def map_day_to_text(day):
    """
    Method to help map each day in int to a corresponding day in string
    :param
     day(int): input the int day of week
    :return:
     string:  correct day of week in string(Week starts on sunday)
    """
    day_mapper = {
        1: 'Sunday',
        2: 'Monday',
        3: 'Tuesday',
        4: 'Wednesday',
        5: 'Thursday',
        6: 'Friday',
        7: 'Saturday'
    }
    return day_mapper[day]


def map_month_to_text(month):
    """
    Method to help map each month in int to a corresponding month in string
    :param
     day(int): input the int mont
    :return:
     string:  correct month in string(Month always ends at june)
    """
    month_mapper = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June'
    }
    return month_mapper[month]


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: ", map_month_to_text(df['month'].mode()[0]))

    # display the most common day of week
    print("The most common day is: ", map_day_to_text(df['day_of_week'].mode()[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common hour is: ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common start station is: ", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most common end station is: ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("The most frequent combination of start station and end station trip")
    most_common_start_and_end_stations = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print(most_common_start_and_end_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum() / 3600.0
    print("total travel time in hours is: ", round(total_duration))

    # display mean travel time
    mean_duration = df['Trip Duration'].mean() / 3600.0
    print("mean travel time in hours is: ", round(mean_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    # Display counts of gender
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    else:
        print("No gender data available")

        # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year_of_birth = int(df['Birth Year'].min())
        most_recent_year_of_birth = int(df['Birth Year'].max())
        most_common_year_of_birth = int(df['Birth Year'].value_counts().idxmax())
        print("The earliest year of birth is:", earliest_year_of_birth,
              ", most recent one is:", most_recent_year_of_birth,
              "and the most common one is: ", most_common_year_of_birth)
    else:
        print("No birth year data available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """Displays the data due filteration.
    5 rows will added in each press"""
    print('Tap any key to see row data or type no to skip....')
    x = 0
    display_data = input().lower()
    while display_data != 'no':
        if x + 5 > len(df.index):
            print("No more data for display....")
            break
        else:
            print(df.iloc[x: x + 5].to_json(orient='index', indent=5))
            display_data = input("Tap any key to display next 5 rows or \'no\' to stop....  ")
            x += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter \'Yes\' to restart or any key to cancel.... \n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
