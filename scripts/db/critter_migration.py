import sqlite3

conn = sqlite3.connect("..\..\critterpedia.db")
c = conn.cursor()

c.execute(f"""SELECT *
            FROM fish""") # Execute the SQL check

fish_list = list(c.fetchall())

class Critter:
    def __init__(self, critter_name, species, location, size, value, start_time, end_time, start_time_second, end_time_second, start_month, end_month, image_url):
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
        # print(time)
        # split the number and period
        time = time.split(" ")
        # print(f"time: {time}")
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

# convert each fish into a critter
for fish in fish_list:
    # get the time periods
    fish_time = fish[5]
    if fish_time == "All day":
        fish_time = "12 a.m. - 12 a.m."
    # fix case for 2 time periods
    split_time = fish_time.split(",") # check for 2 time periods
    print(split_time)
    temp_list = []
    for time_period in split_time:
        time_list = get_time_start_end(time_period)
        time_list = convert_to_24h(time_list)
        for time in time_list:
            temp_list.append(time)
    print(temp_list)


    print(fish[0])
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
    fish_start_month = "null"
    fish_end_month = "null"
    fish_start_month = "null"
    fish_end_month = "null"
    fish_image_url = fish[7]

    critter = Critter(fish_name,
        fish_size,
        fish_location, fish_size, fish_value, fish_start_time_period_1, fish_end_time_period_1, fish_start_time_period_2, fish_end_time_period_2, fish_start_month, fish_end_month, fish_image_url)
