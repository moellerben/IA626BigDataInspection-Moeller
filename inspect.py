# Big Data Inspection - NYC Taxi Trips
# Ben Moeller - Dataset Group 4

import csv
import datetime
from math import floor, radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956 # miles
    return c*r

def update_minmax(cmin, cmax, candidate):
    omin = cmin
    omax = cmax
    if candidate is None:
        return omin, omax
    if cmin is None or cmin > candidate:
        omin = candidate
    if cmax is None or cmax < candidate:
        omax = candidate
    return omin, omax

fn = "trip_data_4.csv"
ofn = "trip_data_4_output.csv"
f = open(fn, 'r')
reader = csv.reader(f)

# Get info about the headers and first row of data
n = 0
for row in reader:
    print(row)
    n += 1
    if n > 5:
        break
'''
['medallion', ' hack_license', ' vendor_id', ' rate_code',
' store_and_fwd_flag', ' pickup_datetime', ' dropoff_datetime',
' passenger_count', ' trip_time_in_secs', ' trip_distance', ' pickup_longitude',
' pickup_latitude', ' dropoff_longitude', ' dropoff_latitude']

['91F6EB84975BBC867E32CB113C7C2CD5', 'AD8751110E6292079EB10EB9481FE1A6',
'CMT', '1', 'N', '2013-04-04 18:47:45', '2013-04-04 19:00:25', '1', '759',
'2.50', '-73.957855', '40.76532', '-73.976273', '40.785648']
'''

'''
    ID  Col Name            Value @ Row 1
----------------------------------------------------------------
    0   medallion           91F6EB84975BBC867E32CB113C7C2CD5
    1   hack_license        AD8751110E6292079EB10EB9481FE1A6
    2   vendor_id           CMT
    3   rate_code           1
    4   store_and_fwd_flag  N
    5   pickup_datetime     2013-04-04 18:47:45
    6   dropoff_datetime    2013-04-04 19:00:25
    7   passenger_count     1
    8   trip_time_in_secs   759
    9   trip_distance       2.50
    10  pickup_longitude    -73.957855
    11  pickup_latitude     40.76532
    12  dropoff_longitude   -73.976273
    13  dropoff_latitude    40.785648
'''

mindt = None
maxdt = None

minlat = None
maxlat = None
minlon = None
maxlon = None

avgpulat = 0
avgpulatc = 0
avgpulon = 0
avgpulonc = 0

avgdolat = 0
avgdolatc = 0
avgdolon = 0
avgdolonc = 0

bin_width = 0.25 # Width of bins
overflow = 15 # Distance at which we stop caring about individual bins
distance_bins = [0]*int((overflow/bin_width)+1) # Odometer distance
haversine_bins = [0]*int((overflow/bin_width)+1) # Haversine distance

minrc = None
maxrc = None

minpc = None
maxpc = None

mintt = None
maxtt = None

pph = {}
for i in range(24):
    pph[str(i).zfill(2)] = {}

n = -1
printevery = 100000
for row in reader:
    n += 1
    if n == 0:
        # Ignore header row since there's no data
        continue
    pudt = datetime.datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S")
    if mindt is None or pudt < mindt:
        mindt = pudt
    dodt = datetime.datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S")
    if maxdt is None or dodt > maxdt:
        maxdt = dodt
    if row[11] != '':
        pulat = float(row[11])
        if pulat is not None and pulat != 0 and -90 < pulat < 90:
            if maxlat is None:
                maxlat = pulat
            else:
                maxlat = max(maxlat, pulat)
            if minlat is None:
                minlat = pulat
            else:
                minlat = min(minlat, pulat)
            avgpulat = (avgpulat*avgpulatc + pulat) / (avgpulatc+1)
            avgpulatc += 1
    if row[10] != '':
        pulon = float(row[10])
        if pulon is not None and pulon != 0 and -180 < pulon < 180:
            if maxlon is None:
                maxlon = pulon
            else:
                maxlon = max(maxlon, pulon)
            if minlon is None:
                minlon = pulon
            else:
                minlon = min(minlon, pulon)
            avgpulon = (avgpulon*avgpulonc + pulon) / (avgpulonc+1)
            avgpulonc += 1
    if row[13] != '':
        dolat = float(row[13])
        if dolat is not None and dolat != 0 and -90 < dolat < 90:
            maxlat = max(maxlat, dolat)
            minlat = min(minlat, dolat)
            avgdolat = (avgdolat*avgdolatc + dolat) / (avgdolatc+1)
            avgdolatc += 1
    if row[12] != '':
        dolon = float(row[12])
        if dolon is not None and dolon != 0 and -180 < dolon < 180:
            maxlon = max(maxlon, dolon)
            minlon = min(minlon, dolon)
            avgdolon = (avgdolon*avgdolonc + dolon) / (avgdolonc+1)
            avgdolonc += 1

    # Trip Distance
    dist_bin = floor(float(row[9]) / bin_width)
    if float(row[9]) > overflow:
        dist_bin = int(overflow / bin_width)
    #print(dist_bin)
    distance_bins[dist_bin] += 1
    # Haversine Distance
    hav_dist = haversine(pulat, pulon, dolat, dolon)
    hav_bin = floor(hav_dist / bin_width)
    if hav_dist > overflow:
        hav_bin = int(overflow / bin_width)
    haversine_bins[hav_bin] += 1

    minrc, maxrc = update_minmax(minrc, maxrc, int(row[3])) # Rate Code
    minpc, maxpc = update_minmax(minpc, maxpc, int(row[7])) # Passenger Count
    mintt, maxtt = update_minmax(mintt, maxtt, int(row[8])) # Trip Time

    # Passengers per hour
    # Get the current hour and date from the pickup datetime
    puhour = pudt.strftime("%H")
    pudate = pudt.strftime("%Y-%m-%d")
    #print(puhour)
    if pudate not in pph[puhour].keys():
        pph[puhour][pudate] = int(row[7])
    else:
        pph[puhour][pudate] += int(row[7])

    if n % printevery == 0:
        print(n)

mindtstr = mindt.strftime("%Y-%m-%d %H:%M:%S")
maxdtstr = maxdt.strftime("%Y-%m-%d %H:%M:%S")

#print(str(n)+" rows in dataset")
#print("Datetime range covered: "+mindtstr+" to "+maxdtstr)
#print("Area covered: "+str(minlat)+", "+str(minlon)+" to "+str(maxlat)+", "+str(maxlon))
#print("Average pickup location: "+str(avgpulat)+", "+str(avgpulon))
#print("Average dropoff location: "+str(avgdolat)+", "+str(avgdolon))
#print(distance_bins)
#print(haversine_bins)
#print(pph)

avg_pph = {}
for hour in pph.keys():
    sum = 0
    count = 0
    for day in pph[hour].keys():
        sum += pph[hour][day]
        count += 1
    avg_pph[hour] = sum/count
#print(avg_pph)

with open(ofn, 'w', newline='') as outcsv:
    writer = csv.writer(outcsv)
    writer.writerow(["Records: ", n])
    writer.writerow(["Datetime Range"])
    writer.writerow([mindtstr, maxdtstr])
    writer.writerow(["Area Range"])
    writer.writerow(["Min Lat", "Min Lon", '', "Max Lat", "Max Lon"])
    writer.writerow([minlat, minlon, '', maxlat, maxlon])
    writer.writerow(["Avg Pickup", '', '', "Avg Dropoff"])
    writer.writerow([avgpulat, avgpulon, '', avgdolat, avgdolon])
    writer.writerow(["Distance Histogram"])
    binlabels = list(range(int(overflow/bin_width)+1))
    binlabels = [bin_width * x for x in binlabels]
    writer.writerow(binlabels)
    writer.writerow(distance_bins)
    writer.writerow(["Haversine Histogram"])
    writer.writerow(binlabels)
    writer.writerow(haversine_bins)
    writer.writerow(["Passengers Per Hour"])
    pph_keys = avg_pph.keys()
    #print(pph_keys)
    writer.writerow(pph_keys)
    pph_values = [avg_pph[x] for x in pph_keys]
    writer.writerow(pph_values)

print("Inspection complete, look at "+ofn+" for results")
