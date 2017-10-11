from __future__ import print_function
import pymysql
from Calf import *
import csv
import sys
calf_list = {}
day = 0

def create_dict(total_study_days):
    # create new dict with INT as key and an object->(healthycount, sickcount, sick)
    # test Paula
    test=Calf(total_study_days)
    calf_tag = 101
    print('Creating Dictionary...')

    #loop thru all 70 calves
    while calf_tag <= 170:
        #inner loop created contact instances, one per calf (excluding itself)
        calf_list[calf_tag] = {
        "sick_count":test.sickCount,
        "healthy_count":test.healthyCount,
        "sick":[ 0 for _ in range(total_study_days)]}
        calf_tag+=1

    # Create buddy properties
    calf_tag = 101
    while calf_tag <= 170:
        for i in range(101,171):
            calf_list[calf_tag][i]={"total_seconds":test.total_seconds,"seconds_by_day":[ 0 for _ in range(total_study_days)]}
        calf_tag+=1

    #print(calf_list)
    return calf_list


# uses mysql to pull data and temporarily store it into an array as [calftag1, x, y, calftag2, x, y]
def pull_data(index):
    # pull data with mysql
    # sensitive information has been taken off
    db = pymysql.connect(host='mysql.cis.ksu.edu', user='', passwd='', db='')
    cursor = db.cursor()

    try:
        # this is going to pull all calftags that were .3 meters from each other for 1 second
        # store data in an array

        query = """
            SELECT a.calftag, b.calftag
            FROM rawrtls a, rawrtls b
            WHERE a.calftag < b.calftag
                AND ((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y)) <= .09
                AND a.ts BETWEEN {commence} AND {adjourn}
                AND a.ts = b.ts;
        """.format(commence=index, adjourn=index + 3600)

        #"AND a.ts between "+ str(index) + " and " + str(index + 30)+" "

        print("Query results:",cursor.execute(query))
        contacts = []
        for i, row in enumerate(cursor.fetchall()):
            #print('im looping')
            contacts.append(row)
    except:
        print(sys.exc_info())
        print('Error.')
        db.rollback()
        exit()

    db.close()
    return contacts


# imports the CSV file that states when the calves were shedding. this is added to each CALF object's sick list.

def health_status(calf_list):

    with open('shedding_times1.csv') as csv_file:
        print('Reading CSV...')

        read_csv = csv.reader(csv_file, delimiter=',')

        read_csv.next()

        for row in read_csv:
            temp_list = []
            for i in range(1, 25):
                temp_list.append(row[i] == '1')
            calf_list[int(row[0])]['sick'] = []
            calf_list[int(row[0])]['sick'].extend(temp_list)
            #print('list', calf_list[int(row[0])]['sick'])
            #print('len', len(calf_list[int(row[0])]['sick']))
        #
        # for i in range(1, 25):
        #         calf_list[read_csv.line_num+99]["sick"].insert(i-1, row[i] == '1')
        #   #  print (read_csv.line_num+99)
        #     print(len(calf_list[(read_csv.line_num)+99]["sick"]))
        #


        print('Finished reading CSV...')
        #print(calf_list[101]["sick"])
        #print(calf_list[102]["sick"])
    return calf_list


#calf_contacts is the list of tuples obtained from the pull_data() function and day indicates which day we are in the loop right now
def add_counts(calf_contact, day):
    #key : calf_a
        #   "sick_count"
        #   "healthy_count"
        #   "sick"
        #    key: calf_b
            #   "total_seconds"
            #   "seconds_by_day"
    #print(calf_contact)
    #print("adding counts")
    for calf_a, calf_b in calf_contact:
        elapsed_seconds = 0
        d = day
        calf_a, calf_b = int(calf_a), int(calf_b)
        #print(calf_a, calf_b, day)

        if calf_a and calf_b < 171:
            #print("less than 170")
            #print("sick count", calf_list[calf_b]["sick_count"] )
            calf_list[calf_b]["sick_count" if calf_list[calf_a]["sick"][day] else 'healthy_count'] += 1
            calf_list[calf_a]["sick_count" if calf_list[calf_b]["sick"][day] else 'healthy_count'] += 1
            #print("healthy count", calf_list[calf_a]["healthy_count"])

            """"
            calf_list[calf_a][calf_b]["total_seconds"] += 1  # increase the buddy 'total seconds' by 1
            calf_list[calf_b][calf_a]["total_seconds"] += 1  # increase the buddy 'total seconds' by 1
            print("total seconds", calf_list[calf_b][calf_a]["total_seconds"])
            """

            calf_list[calf_a][calf_b]["seconds_by_day"][day] += 1
            calf_list[calf_b][calf_a]["seconds_by_day"][day] += 1
            #print("seconds by day ", calf_list[calf_b][calf_a]["seconds_by_day"])

            tempDay = d
            totalSecondsAB = 0
            totalSecondsBA = 0
            while tempDay >= 0:
                totalSecondsAB += calf_list[calf_a][calf_b]["seconds_by_day"][tempDay]
                totalSecondsBA+= calf_list[calf_b][calf_a]["seconds_by_day"][tempDay]
                tempDay -= 1
            #print("temp total seconds", totalSecondsAB, totalSecondsBA)
            calf_list[calf_a][calf_b]["total_seconds"] = totalSecondsAB
            calf_list[calf_b][calf_a]["total_seconds"] = totalSecondsBA
        else:
            continue
        #print("total seconds", calf_list[calf_a][calf_b]["total_seconds"], calf_list[calf_b][calf_a]["total_seconds"])

        # if day > 0:
        #
        #     while d > 0:
        #         s = calf_list[calf_b][calf_a]["seconds_by_day"][d]
        #         elapsed_seconds += s
        #         d -=1
        #     calf_list[calf_a][calf_b]["seconds_by_day"][day] = calf_list[calf_a][calf_b]["total_seconds"] - elapsed_seconds
        #     calf_list[calf_b][calf_a]["seconds_by_day"][day] = calf_list[calf_a][calf_b]["total_seconds"] - elapsed_seconds
        #     print("seconds by day ",calf_list[calf_b][calf_a]["seconds_by_day"])
        #
        # else:
        #     calf_list[calf_a][calf_b]["seconds_by_day"][day] = calf_list[calf_a][calf_b]["total_seconds"]
        #     calf_list[calf_b][calf_a]["seconds_by_day"][day] = calf_list[calf_a][calf_b]["total_seconds"]

    # print("right out of for loop, adding counts", str(calf_list[142][153]["seconds_by_day"]))
    # print("total seconds ", calf_list[142][153]["total_seconds"])


def export_data(total_study_days):
    csv_columns=["calf_id","study_day"]
    for i in range(101,171):
        csv_columns.append(str(i))
        csv_columns.append((str(i) + "_sick_status"))
    # print(type(calf_list))
    # print(calf_list[101][102]["seconds_by_day"])

    with open("new_result.csv","w") as f:
        #write=csv.DictWriter(f, fieldnames = csv_columns)
        testwriter = csv.writer(f, delimiter=',')
        testwriter.writerow(csv_columns)
        #write.writeheader()
        for i in range(1, total_study_days):  # days
            #for j in range(101, 110):  # cows <rows>
            for cow in calf_list.keys():
                output = []
                output.append(str(cow))          # cow id
                output.append(i)            # study day

                # output.append(calf_list[cow]["healthy_count"])  #cow health count
                # #print(calf_list[cow]["healthy_count"])
                # output.append(calf_list[cow]["sick_count"])     #cow sick count with all sick cows
                # go over the buddy cows.
                # print(type(calf_list))
                # print(calf_list[101])
                for buddy_cow in range(101, 171):  # columns
                    output.append(calf_list[cow][buddy_cow]["seconds_by_day"][i - 1])  # gives total seconds of contact with a given cow
                    output.append(calf_list[buddy_cow]["sick"][i - 1])  # this gives you the health status of cows
                testwriter.writerow(output)
    with open("main_counts.csv", "w") as wr:
        morewriter = csv.writer(wr, delimiter = ',')
        morewriter.writerow(["Calf ID", "healthy count", "sick count", "total count with 108"])
        for calf in calf_list.keys():
            out = []
            out.append(str(calf))
            out.append(calf_list[calf]["healthy_count"])
            out.append(calf_list[calf]["sick_count"])
            out.append(sum(calf_list[calf][108]["seconds_by_day"]))

            morewriter.writerow(out)


    print("end of export")
