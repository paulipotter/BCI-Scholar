class Contacts:
    def __init__(self):  # int, int, list
        self.contact_buddy = 0
        #this number adds up all the items in the list below
        self.total_seconds = 0

        # each index represents a day and the number at that index is the amount of
        # contacts between those two calves during that day
        self.record_dates = []

    @staticmethod
    def ct(self, day):
        self.total_seconds += 1
        self.record_dates[day-1] += 1

    def print_one(self) -> object:
        return str(self.contact_buddy) + ','  + str(self.total_seconds) + ',' + ",".join(str(item) for item in self.record_dates)