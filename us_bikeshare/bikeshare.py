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
    
    while True:
          city = input("Which city would you like to filter by? new york city, chicago or washington?\n")
          city=city.lower() # conv to lower case 
          
          if city not in ("new york city", "chicago", "washington"):
            print("Sorry, I didn't catch that. Try again.")
            continue
          else:
            break
        
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
              month = input("Which month would you like to filter by? January, February, March, April, May, June or type 'all' if you do not have any preference?\n")
              month = month.lower() 
              #print("This is the monthhhh ====   "+ month)  
              if month not in ("january", "february", "march", "april", "may", "june", "all"):
                print("Sorry, I didn't catch that. Try again.")
                continue
              else:
                break


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
          day = input("Are you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you do not have any preference.\n")
          day=day.lower() # convert to lower case
          if day not in ("sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "all"):
            print("Sorry, I didn't catch that. Try again.")
            continue
          else:
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

    df = pd.read_csv("{}.csv".format(city.replace(" ","_")))

    # Convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df["month"].mode()[0]
    print("Most Common Month:", common_month)


    # TO DO: display the most common day of week
    common_day = df["day_of_week"].mode()[0]
    print("Most Common Day of Week:", common_day)


    # TO DO: display the most common start hour
    df['hour'] = df["Start Time"].dt.hour
    common_hour = df['hour'].mode()[0]
    print("Most Common Start Hour:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df["Start Station"].value_counts().idxmax()
    print("Most Commonly used Start Station:", common_start_station)

    # TO DO: display most commonly used end station
    commonly_end_station = df["End Station"].value_counts().idxmax()
    print("Most Commonly used End Station:", commonly_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    combination_station = df.groupby(["Start Station", "End Station"]).count()
    print('Most Commonly used combination of start station and end station:', combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print("Total travel time:", total_travel_time/86400, "Days")

    # TO DO: display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print("Mean travel time:", mean_travel_time/60, "Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df["User Type"].value_counts()
    print("User Types:", user_types)
    
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df["Gender"].value_counts()
        print("Gender Types:", gender_types)


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = df["Birth Year"].min()
        print("Earliest Year of Birth:", earliest_year)
        most_recent_year = df['Birth Year'].max()
        print("Most Recent Year of Birth:", most_recent_year)
        most_common_year = df['Birth Year'].mode()[0]
        print("Most Common Year of Birth:", most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Displays raw data to the user upon their request.
    Prints:
        The raw data, five lines at a time, until the user specifies
        to stop, or until the end of the dataframe is reached.
    """
    show_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').lower()
    i = 0
    while show_data.startswith('y'):
        if i + 5 < df.shape[0]:
            print(df.iloc[i:i+5])
            i = i + 5
        else:
            print(df.iloc[i:])
            break

        show_data = input('\nDo you want to see more raw data? Enter yes or no.\n').lower()
                          

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
