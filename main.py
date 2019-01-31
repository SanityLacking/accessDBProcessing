
import numpy as np
import time
import matplotlib
import math
import datetime
import csv
from dbConnect import * 
import sys

cursor = dbOpen("3LA_Dredge_Points.accdb")
#if cursor is a string the connect failed
tables = listTables(cursor)
datetimeFormat = '%I:%M:%S %p %d/%m/%Y'
reports = []
reportStart={}

MAXDIST = 40  #max distance item can move
MAXTIME = 86400  # max time between reports


def emitReport(reportStart,row):
   # print("report created")
    results={
    "id":len(reports),
    "distanceMoved":math.hypot(reportStart.Easting - row.Easting, reportStart.Northing - row.Northing),
    "StartEast":reportStart.Easting,
    "StartNorth":reportStart.Northing,
    "EndEast":row.Easting, 
    "EndNorth":row.Northing,
    "timeStart":datetime.datetime.combine(reportStart.Date.date(),reportStart.Time.time()),
    "timeEnd":datetime.datetime.combine(row.Date.date(),row.Time.time()),
    "timeElapsed":timeCompare(datetime.datetime.combine(reportStart.Date.date(),reportStart.Time.time()),datetime.datetime.combine(row.Date.date(),row.Time.time()))
    }
    output = results
    #output = {"results":results,"start": reportStart, "end": row}    
    return output


def timeCompare(time1, time2):    #take two times and compare them and return the difference in seconds
    diff = time1 - time2
    output =  abs(diff.total_seconds())
    return output

#get the data using numpy
#np.loadtxt(open("test.csv", "rb"), delimiter=",", skiprows=1)

#loop through the data

#define results array


#input  = np.array(execute(cursor, "select * from [Table1]"))
input  = (executeCursor(cursor, "select * from [Raw Logging Data]"))
count = 0
latestRow ={}
for row in input:
    #print(row)
    latestRow = row
    count=count+1
    sys.stdout.write("currently processing {} rows \r".format(count))
    sys.stdout.flush()
    #if count >=10000:break
    #check all the fields are filled in
    if not row.Easting or not row.Northing or not row.Time or not row.Date:
        continue

    if not reportStart: #if empty, fill
        reportStart = row
        #print("fill")
        #print(reportStart)
        continue
        
    dist = math.hypot(reportStart.Easting - row.Easting, reportStart.Northing - row.Northing)
    if dist >= MAXDIST:
        #end report
        reports.append(emitReport(reportStart,row))
        reportStart={}
        continue
    elif timeCompare(datetime.datetime.combine(reportStart.Date.date(),reportStart.Time.time()),datetime.datetime.combine(row.Date.date(),row.Time.time())) >= MAXTIME: #first lets do it irrespective of day, and then one which will only have one report per day
        #end Report
        reports.append(emitReport(reportStart,row))
        reportStart={}
        continue
    else:    
        continue
    #define report period start

if reportStart: # if list has ended and a report hasn't been completed, grab the last element of the list and complete the report
    print("Final report")
    reports.append(emitReport(reportStart,latestRow))
    reportStart={}
print("{} lines processed, {} reports created".format(count,len(reports)))

#print("generated Reports:")
#for row in reports:
    #print(row)
# if Euclidean distance between reporting start and current point is equal to or greater then 10m, end report
# if time period is greater then 24hrs, end report.
# todo: generate a graph of the distance moved over time. 

keys = reports[0].keys()
now = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
name = 'results_{}.csv'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
with open("results_{}.csv".format(MAXDIST),'w') as csvfile:
    writer = csv.DictWriter(csvfile,keys)
    writer.writeheader()
    writer.writerows(reports)

print("finished")