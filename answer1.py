import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february' , 'march', 'april' , 'may' ,'june']
days = ['sunday', 'monday' , 'tuesday', 'wednesday' , 'thursday' ,'friday', 'saturday']
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
    while True:
        city = input('Enter the city name\n').lower()
        if city in CITY_DATA.keys():
            print('the name of the city you entered is: ',city)
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nWhich month(ex: All, January):\nor Press Enter to make no month filter\n').lower()
        if month in months:
            print('month to filter ',month)
            break
        elif month == 'all':
            print('NO month filter')
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nWhich day to filter(ex: All, Sunday, Monday):\n or Press Enter to make no day filter\n').lower()
        if day in days:
            print('you selected' ,day , ' to filter ')
            break
        elif day == 'all':
            print('NO day filter')
            break

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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
#     CREATE NEW COLUMNS TO COMPARE FILTERING WITH
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    #filter by month if applicable
    if month != "all":
        month = months.index(month) +1 
        df = df[df['month']==month]
    if day!="all":
        df = df[df['day_of_week']==day.title()]
#     print(month)
#     print(df)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("\nThe most common month is ", df['Start Time'].dt.month.mode()[0])

    # display the most common day of week
    print("\nThe most common day is ", df['Start Time'].dt.weekday_name.mode()[0])

    # display the most common start hour
    print("\nThe most common start hour is ", df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("\nThe most common start station is ", df['Start Station'].mode()[0])
    
    # display most commonly used end station
    print("\nThe most common end station is ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print(df.groupby(['Start Station','End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Diff Time'] = df['End Time'] - df['Start Time']
    print("Total time travel %s" %df['Diff Time'].sum())

    # display mean travel time
    print("Mean travel time = %s minutes"%(df['Diff Time'].sum().total_seconds() / df['Diff Time'].count() /60 ))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df , city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    
    user_counts = df['User Type'].value_counts()
    print("User types count: %s" %user_counts)
    
    if city!= "washington":
        # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print("gender count: %s" %gender_counts)
        # Display earliest, most recent, and most common year of birth
        early_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].value_counts().idxmax()
        print("\nEarly Birth Year is %s \n Recent Birth Year is %s \n Common Birth Year is %s" %(early_birth_year,recent_birth_year ,               common_birth_year))
          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    if view_data == "yes":
        start_loc = 0
        view_display = "yes"
        print("exit")
        while (view_display =="yes" ):
            print(df.iloc[ start_loc : start_loc+5])
            start_loc += 5
            view_display = input("Do you wish to continue?: ").lower()
    else:
        pass
    
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
