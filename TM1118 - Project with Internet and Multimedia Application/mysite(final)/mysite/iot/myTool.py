from asyncio import events
import numbers
from re import sub
from .models import Event
from event.models import Event as Classdata
from datetime import datetime,timedelta
from django.db.models import Avg, Max, Min
from django.core import serializers
from django.db.models.functions import TruncHour, TruncMinute
from itertools import chain
import pytz

timezone_str = "+08:00"
#Get all distinct time, venue and node

def getTimeInRange(start,end):
    Events = Event.objects.filter(date_created__range=[start, end]).annotate(time=TruncHour('date_created')).values('time')
    TimeDict = {}
    for event in Events: 
        time = str(event['time'].strftime("%Y-%m-%d %H:%M:%S"))
        if str(event['time'].strftime("%Y-%m-%d %H:%M:%S")) in TimeDict:
            TimeDict[str(event['time'].strftime("%Y-%m-%d %H:%M:%S"))] += 1
        else:
            TimeDict[str(event['time'].strftime("%Y-%m-%d %H:%M:%S"))] = 1
    Timelist =list(TimeDict.keys())
    Timelist.sort()
    return Timelist

def getAllVenue():
    #return all venue in [a,b,c,d,e,f,.......]
    classdatas = Classdata.objects.all().values()
    locationDict = {}
    
   
    for eventloc in classdatas:
        venue = str(eventloc['venue'])
        
        if venue in locationDict:
            locationDict[venue] += 1
        else:
            locationDict[venue] = 1
    return list(locationDict.keys())

def getAllDistinceNode(start,end):
    Events = Event.objects.filter(date_created__range=[start, end])
    EventNodeDict = {}
    for tempevent in Events:
        if Event.node_id in EventNodeDict:
            EventNodeDict[tempevent.node_id] += 1
        else:
            EventNodeDict[tempevent.node_id] = 1
    return EventNodeDict.keys()

#Use in dataAnalysis by node or time slot

def getDataByIdInHourWithRange(start,end,nodes):
    data = {}
    subdataInID = {}
    
    TimeDict = {}

    for node in nodes:
        Events = Event.objects.filter(date_created__range=[start, end],node_id = node).annotate(time=TruncHour('date_created')).values('time','node_id','node_loc').annotate(avg_temp = Avg('temp'),avg_hum = Avg('hum'),avg_light = Avg('light'),avg_snd = Avg('snd'))
        
        sublist = []
        for event in Events: 
            temp = {}
            temp['time'] = str(event['time'].strftime("%Y-%m-%d %H:%M:%S"))
            temptime = str(event['time'].strftime("%Y-%m-%d %H:%M:%S"))
            temp['node_id'] = node
            temp['loc'] = str(event['node_loc'])
            temp['avg_temp'] = str(event['avg_temp'])
            temp['avg_hum'] = str(event['avg_hum'])
            temp['avg_light'] = str(event['avg_light'])
            temp['avg_snd'] = str(event['avg_snd'])
            sublist.append(temp)

           
            if temptime in TimeDict:
                TimeDict[temptime].append(temp)
            else:
                TimeDict[temptime]= [temp]
  
        subdataInID.update({node: sublist})
    nodeslist = list(nodes)
    nodeslist.sort()
    Timelist =list(TimeDict.keys())
    Timelist.sort()
    data.update({"NodeData":subdataInID})
    data.update({"NodeSet":nodeslist})
    data.update({"NodeDate": Timelist})
    data.update({"NodeDateInTime": TimeDict})
    return data

def getDataByIdInMinutesWithRange(start,end,nodes):
    data = {}
    subdataInID = {}
    
    TimeDict = {}

    for node in nodes:
        Events = Event.objects.filter(date_created__range=[start, end],node_id = node).annotate(time=TruncMinute('date_created')).values('time','node_id','node_loc').annotate(avg_temp = Avg('temp'),avg_hum = Avg('hum'),avg_light = Avg('light'),avg_snd = Avg('snd'))
        
        sublist = []
        for event in Events: 
            temp = {}
            temp['time'] = str(event['time'].strftime("%Y-%m-%d %H:%M:%S"))
            temptime = str(event['time'].strftime("%Y-%m-%d %H:%M:%S"))
            temp['node_id'] = node
            temp['loc'] = str(event['node_loc'])
            temp['avg_temp'] = str(event['avg_temp'])
            temp['avg_hum'] = str(event['avg_hum'])
            temp['avg_light'] = str(event['avg_light'])
            temp['avg_snd'] = str(event['avg_snd'])
            sublist.append(temp)

           
            if temptime in TimeDict:
                TimeDict[temptime].append(temp)
            else:
                TimeDict[temptime]= [temp]
  
        subdataInID.update({node: sublist})
    nodeslist = list(nodes)
    nodeslist.sort()
    Timelist =list(TimeDict.keys())
    Timelist.sort()
    data.update({"NodeData":subdataInID})
    data.update({"NodeSet":nodeslist})
    data.update({"NodeDate": Timelist})
    data.update({"NodeDateInTime": TimeDict})
    return data

#Use in comparing the room have event and no event
def getExcludedTimeByIncludedTime(venues):
    data = {}
    for venue1 in venues:
        classdatas = Classdata.objects.filter(venue = venue1).values()
        sublist = []
        for i in range(len(classdatas)):
               
                temp = ['','']
            
                if i == 0:
                    temp[0] = "2022-07-12T07:00:00.000"+timezone_str
                else:
                    temp[0] = datetime.combine(classdatas[i-1]['date'],classdatas[i-1]['end_time']).isoformat()+timezone_str

                if i == len(classdatas)-1:
                    temp[1] = "2022-07-19T00:00:00.000"+timezone_str
                else:
                    temp[1]= datetime.combine(classdatas[i]['date'],classdatas[i]['start_time']).isoformat()+timezone_str
                sublist.append(temp)

        data.update({venue1:sublist})
    return data

def getClassDataInAllTimeRange(venues):
    #return the date range of all selected venues in {"venues":[[date1,date2],[date3,date4],....]}
    data = {}
    for venue1 in venues:
        classdatas = Classdata.objects.filter(venue = venue1).values()
        sublist = []
        for classdata in classdatas: 
                temp = ['','']
               
                temp[0] = datetime.combine(classdata['date'],classdata['start_time']).isoformat()+timezone_str

                temp[1]= datetime.combine(classdata['date'],classdata['end_time']).isoformat()+timezone_str
                sublist.append(temp)
        data.update({venue1:sublist})
    return data

def getCombineDataWithinDateRange(datasInVenue,venue):
    #data = [[a,b],[b,c],[c,d]...] date range array
    #combine all result in date (time) range
    #return = [All suitable record]
    result = []
    for data in datasInVenue:
        Events = Event.objects.filter(date_created__range=[data[0],data[1]]).filter(node_loc = venue.upper(), date_created__gt = "2022-07-13T15:00:00"+timezone_str).values()
        
        result += list(Events)
   
    return processUnionResultAndGetAverage(result,venue)



def processUnionResultAndGetAverage(result,venue):
    #Support getCombineDataWithinDateRange getCombineDataWithoutDateRange
    if len(result) > 0 :
        totalResultSet = {"node_id":str(result[len(result)-1]["node_id"]),"node_loc":str(venue),"number":0,"temp":0,"hum":0,"light":0,"snd":0,"state":"success"}
        for event in result:
            totalResultSet["number"]+=1
            totalResultSet["temp"]+=event["temp"]
            totalResultSet["hum"]+=event["hum"]
            totalResultSet["light"]+=event["light"]
            totalResultSet["snd"]+=event["snd"]
        
        totalResultSet["temp"]= str(totalResultSet["temp"]/totalResultSet["number"])
        totalResultSet["hum"]= str(totalResultSet["hum"]/totalResultSet["number"])
        totalResultSet["light"]= str(totalResultSet["light"]/totalResultSet["number"])
        totalResultSet["snd"]= str(totalResultSet["snd"]/totalResultSet["number"])
    else:
        totalResultSet ={"state":"fail"}

    return totalResultSet

def processVenueTimeRangeData(indata,outdata):
    #Get data in getClassDataInAllTimeRange and combine it with 
    #getCombineDataWithinDateRange and  getCombineDataWithoutDateRange
    #To get two data in same venue in (average)
    keys = list(indata.keys())
    result= {}
    #print(getCombineDataWithoutDateRange(data[keys[0]],keys[0]))
    
    for key in keys:
        temp = {}
        
        tempinclude = getCombineDataWithinDateRange(indata[key],key)
        tempexclude = getCombineDataWithinDateRange(outdata[key],key)
        if tempinclude['state']=="success" and tempexclude['state']=='success':
            temp.update({'inrange':tempinclude,'outrange':tempexclude})
            result.update({key:temp})
        
    return result

def secondAnalysis():
    venues = getAllVenue()
    insidedata = getClassDataInAllTimeRange(venues)
    outsidedata = getExcludedTimeByIncludedTime(venues)
    data = processVenueTimeRangeData(insidedata,outsidedata)
    return data

#print(getExcludedTimeByIncludedTime(["W311a"]))
#d2=getClassDataInAllTimeRange(["W311a"])
#data=Event.objects.filter(date_created__range=['2022-07-14T08:00:00+08:00', '2022-07-14T12:00:00+08:00'], node_loc = "W311A").values()
#print(d2)
#print(data)