import sqlite3

conn = sqlite3.connect("..\..\critterpedia.db")
c = conn.cursor()

c.execute(f"""SELECT *
            FROM fish""") # Execute the SQL check

fish_list = list(c.fetchall())

class Critter:
    def __init__(self, critter_name, species, location, size, value, start_time, end_time, start_time_second, end_time_second, start_month, end_month, start_month_second, end_month_second, image_url):
        self.critter_name = critter_name
        self.species = species
        self.location = location
        self.size = size
        self.value = value
        self.start_time = start_time
        self.end_time = end_time
        self.start_time_second = start_time_second
        self.end_time_second = end_time_second
        self.start_month = start_month
        self.end_month = end_month
        self.start_month_second = start_month_second
        self.end_month_second = end_month_second
        self.image_url = image_url

# split time from (start - end) to get start and end
def get_time_start_end(time_to_split: str) -> list:
    start_and_end_times = time_to_split.split("-")
    start_time = start_and_end_times[0].strip()
    end_time = start_and_end_times[1].strip()
    formatted_times = [start_time, end_time]
    return(formatted_times)

# turn time (2 p.m.) into 24 hour format 14:00
def convert_to_24h(time_list: list) -> list:
    formatted_times = []
    for time in time_list:
        # split the number and period
        time = time.split(" ")
        number = int(time[0])
        period = time[1]
        if number < 12 and period == "p.m.":
            number = number + 12
        if number == 12 and period == "a.m.":
            number = 0
        if number < 10:
            number = "0" + str(number)
        number = str(number) + ":00"
        formatted_times.append(number)
    return formatted_times

def get_month_start_end(month_string: str) -> list:
    both_dates = month_string.split("-")
    start_date = both_dates[0]
    end_date = both_dates[1]
    return_list = [start_date, end_date]
    return return_list

# convert each fish into a critter
for fish in fish_list:
    # get the time periods
    fish_time = fish[5]
    if fish_time == "All day":
        fish_time = "12 a.m. - 12 a.m."
    # fix case for 2 time periods
    split_time = fish_time.split(",") # check for 2 time periods
    temp_list = []
    for time_period in split_time:
        time_list = get_time_start_end(time_period)
        time_list = convert_to_24h(time_list)
        for time in time_list:
            temp_list.append(time)

    # get the month periods
    fish_dates = fish[6]
    start_date_second = "null"
    end_date_second = "null"

    if "round" in fish_dates:
        start_date = "All Year"
        end_date = "All Year"
    else:
        # get the northern hemisphere months
        fish_dates = fish_dates.split("/")[0].strip().replace(" (Northern)", "")
        # check if only one month
        if "-" not in fish_dates: # start and end month are the same
            start_date = fish_dates
            end_date = fish_dates
        # check if only one period
        elif "," not in fish_dates:
            both_dates = get_month_start_end(fish_dates)
            start_date = both_dates[0]
            end_date = both_dates[1]
        else:
            both_periods = fish_dates.split(", ")
            both_dates_first = get_month_start_end(both_periods[0])
            both_dates_second = get_month_start_end(both_periods[1])
            start_date = both_dates_first[0]
            end_date = both_dates_first[1]
            start_date_second = both_dates_second[0]
            end_date_second = both_dates_second[1]

    # convert the fish properties ready to fit critter class
    fish_name = fish[0]
    fisih_species = fish[1]
    fish_location = fish[2]
    fish_size = fish[3]
    fish_value = fish[4]
    fish_start_time_period_1 = temp_list[0]
    fish_end_time_period_1 = temp_list[1]
    if len(temp_list) == 4:
        fish_start_time_period_2 = temp_list[2]
        fish_end_time_period_2 = temp_list[3]
    else:
        fish_start_time_period_2 = None
        fish_end_time_period_2 = None
    fish_start_month = start_date
    fish_end_month = end_date
    fish_start_month_period_2 = start_date_second
    fish_end_month_period_2 = end_date_second
    fish_image_url = fish[7]

    # convert fish into critter
    critter = Critter(
        fish_name,
        fish_size,
        fish_location,
        fish_size,
        fish_value,
        fish_start_time_period_1,
        fish_end_time_period_1,
        fish_start_time_period_2,
        fish_end_time_period_2,
        fish_start_month,
        fish_end_month,
        fish_start_month_period_2,
        fish_end_month_period_2,
        fish_image_url)

    print(critter.start_month_second)
