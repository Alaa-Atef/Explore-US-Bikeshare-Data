import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago','new york city','washington']
input_months = ['january', 'february', 'march', 'april', 'may', 'june','all']
input_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Please choose a city from: chicago, new york city, washington')
    city = input()

    while not(city.lower() in cities ):
        print('Enter the city again, please choose a city from: chicago, new york city, washington')
        city = input()
    # get user input for month (all, january, february, ... , june)
    print('Please choose a month from: january, february, march, april, may, june, or select "all" ')
    month = input()

    while not(month.lower() in input_months ):
        print('Enter the month again, please choose a month from: january, february, march, april, may, june, or select "all"')
        month = input()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('Please choose a day from: monday, tuesday, wednesday, thursday, friday, saturday, sunday, or select "all" ')
    day = input()

    while not(day.lower() in input_days ):
        print('Enter the day again, please choose a day from: monday, tuesday, wednesday, thursday, friday, saturday, sunday, or select "all" ')
        day = input()

    print('-'*40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most common month:', most_common_month)

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end = df.groupby(['Start Station','End Station']).size().idxmax()
    print("Most frequent combination of start station and end station trip", popular_start_end )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print("Total travel time:", total_travel_time)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time:",mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    if city == 'washington':
        print("There is no gender or birth year data for washington")
    else:
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print(gender)

        # Display earliest, most recent, and most common year of birth
        earliest_year = min(df['Birth Year'])
        print("The earliest year of birth:",earliest_year)

        most_recent = max(df['Birth Year'])
        print("The most recent year of birth:", most_recent)

        most_common = df['Birth Year'].mode()[0]
        print("The most common year of birth:", most_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        answer = input("\nWould you like to see 5 new lines of the raw data ? Enter yes or no.\n")
        answer_itirator = 0

        while answer.lower() == 'yes':
            print(df.iloc[answer_itirator:answer_itirator + 5])
            answer_itirator += 5
            answer = input("\nWould you like to see 5 new lines of the raw data ? Enter yes or no.\n")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
