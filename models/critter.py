class Critter():
    def __init__(self, name, species, location, size, value, start_time, end_time, alt_start_time, alt_end_time, start_month, end_month, alt_start_month, alt_end_month, image_url):
        self.name = name
        self.species = species
        self.location = location
        self.size = size
        self.value = value
        self.start_time = start_time
        self.end_time = end_time
        self.alt_start_time = alt_start_time
        self.alt_end_time = alt_end_time
        self.start_month = start_month
        self.end_month = end_month
        self.alt_start_month = alt_start_month
        self.alt_end_month = alt_end_month
        self.image_url = image_url

    def get_critter_time_period(self):
        print(self.start_month)
