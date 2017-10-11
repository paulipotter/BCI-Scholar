class Calf:
    def __init__(self, total_study_days):
        self.sickCount = 0		# this is count of seconds a cow has touched a sick cow
        self.healthyCount = 0 	# this is count of seconds a cow has touched a healthy cow
        self.sick = [] 			# this gives health status of a cow on a given day
        i = 0
        index = 101
       	# contact properties:
        self.buddy=[i for i in range(101,171)] # this gives list of cows that are present        
        self.total_seconds = 0 	# total seconds of contact with any buddy cow
        self.seconds_by_day = [ 0 for _ in range(total_study_days)]


    #def print_one(self) -> object:
    #    return str(self.buddy) + ','  + str(self.total_seconds) + ',' + ",".join(str(item) for item in self.seconds_by_day)