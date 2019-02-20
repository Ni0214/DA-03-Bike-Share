import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
   # define a function to identify the input city/month/day name is correct or not, request corrct name until input right city name
    def input_identify(request_input_message, error_print,input_list, get_value):
        while True:
            ident=input(request_input_message) #condition1: request_input_message got
            ident=get_value(ident) #confition2: get the value of city/month/day name
            if ident in input_list:
                return ident
            else:
                print(error_print)
    city=input_identify('Please input 1 of the city name in following city list (Chicago,New york city,Washington):',
                        'Error! please enter the correct city name.',
                        ['chicago','new york city','washington'],
                        lambda x:str.lower(x))
    # TO DO: get user input for month (all, january, february, ... , june)
    month=input_identify('Please input month filter? all,january,february,...,june:',
                         'Error! please enter the correct month name.',
                         ["january","february","march","april","may","june","all"],
                         lambda x:str.lower(x)) 
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day=input_identify('Please input dayfilter? all,monday,tuesday,...,sunday:',
                       'Error! please enter the correct month name.',  
                       ["monday","tuesday","wednesday","thursday","friday","saturday","sunday","all"],
                       lambda x:str.lower(x)) 
    
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
    df=pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time']=pd.to_datetime(df['Start Time'])
       
    #extract month and day of week from Start Time to create new columns
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday_name
       
    #filter by month if applicable
    if month!='all':
       # use the index of the months list to get the columns
       months=['january','february','march','apri','may','june']
       month=months.index(month)+1
       
       #filter by month to create the new dataframe
       df=df[df['month']==month]
    #filter by day of week if applicable
    if day!='all':
       #fliter by day of week to create the new data frame
       df=df[df['day_of_week']==day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    #convert the start time column to date time
    #df['Start Time']=pd.to_datetime(df['Start Time'])
    #extract hour from start time column to create an month column
    #df['month']=df['Start Time'].dt.month
    #find the most popular month
    popular_month=df['month'].mode()[0]
    print('Most Popular month:', popular_month)
    # TO DO: display the most common day of week
    #df['day']=df['Start Time'].dt.weekday_name
    popular_day=df['day_of_week'].mode()[0]
    print('Most Popular day:', popular_day)
    # TO DO: display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    popular_hour=df['hour'].mode()[0]
    print('Most Popular hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station=df['Start Station'].mode()[0]
    print('Most Popular start station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station=df['End Station'].mode()[0]
    print('Most Popular end station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    #create a new column to get the information from 'start station' to 'end station'
    df['trip'] = 'from ' + df['Start Station'] + ' to ' +df['End Station']
    popular_both_station=df['trip'].mode()[0]
    print('Most Popular start combination+end station:', popular_both_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time is:', df['Trip Duration'].sum())

    # TO DO: display mean travel time
    print('Mean travel time is:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('User types are\n:', df['User Type'].value_counts())

    # TO DO: Display counts of gender
    #due to washington.csv lack of information for gender and birth year, so:
    if 'Gender' in df:
        print('Gender types are\n:', df['Gender'].value_counts())
    else:
        print(' There is no gender information for this city file')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
       # df['Year']=pd.to_datetime(df['Birth Year']).dt.year
        print('Most earliest birth year:', df['Birth Year'].min())
        print('Most recent birth year:', df['Birth Year'].max())
        print('Most earliest birth year:', df['Birth Year'].mode()[0])
    else:
        print(' There is no birth year information for this city file')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
