# IA626 Big Data Inspection
Created by Ben Moeller

Dataset: Group 4

1. What datetime range does your data cover? How many rows are there total?
   - Group 4 contains 15,100,462 rows
   - Datetime range covers from midnight on April 1, 2013 to 2:19am on May 1, 2013.
2. What are the field names? Give descriptions for each field.
   - medallion: Unique alphanumeric ID of each taxi medallion, which licenses taxi operators to work in NYC
   - hack_license: Unique alphanumeric ID of each taxi driver's hack license
   - vendor_id: Unique ID of the vendor
   - rate_code: Numerical code indicating the rate being charged
   - store_and_fwd_flag: Whether the ride was immediately sent to the server, or if the information was stored locally and then forwarded later (due to poor connection)
   - pickup_datetime: The date and time the passengers were picked up and the meter started
   - dropoff_datetime: The date and time the passengers were dropped off and the meter stopped
   - passenger_count: The number of passengers being transported
   - trip_time_in_secs: The duration of the trip, measured in seconds
   - trip_distance: The distance recorded by the taxi's odometer during the trip, reported (presumably) in miles
   - pickup_longitude: The longitude read by the GPS where the passengers were picked up
   - pickup_latitude: The latitude read by the GPS where the passengers were picked up
   - dropoff_longitude: The longitude read by the GPS where the passengers were dropped off
   - dropoff_latitude: The latitude read by the GPS where the passengers were dropped off
3. Give some sample data for each field.

| medallion | hack_license | vendor_id | rate_code | store_and_fwd_flag | pickup_datetime | dropoff_datetime | passenger_count | trip_time_in_secs | trip_distance | pickup_longitude | pickup_latitude | dropoff_longitude | dropoff_latitude |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 91F6EB84975BBC867E32CB113C7C2CD5 | AD8751110E6292079EB10EB9481FE1A6 | CMT | 1 | N | 2013-04-04 18:47:45 | 2013-04-04 19:00:25 | 1 | 759 | 2.50 | -73.957855 | 40.76532 | -73.976273 | 40.785648 |
| E3FB99712D99954D259002EBAF4AD015 | 506DBCE23867EACF170EFEBDA3143E2A | VTS | 1 | `NULL` | 2013-04-13 09:27:00 | 2013-04-13 09:35:00 | 1 | 480 | 1.28 | -73.977631 | 40.725807 | -73.999023 | 40.734047 |
| 78303FC5414D9061274F6DB06EC81689 | 5AC719AA22EA1B468A3FB4556153D6F4 | VTS | 1 | `NULL` | 2013-04-13 08:14:00 | 2013-04-13 08:24:00 | 6 | 600 | 3.18 | -74.006187 | 40.739758 | -74.014252 | 40.709637 |
| 483E1823636571D425A74CA6B5FA7909 | A8286CE34C7095E6F09BB7A4BA566F69 | VTS | 1 | `NULL` | 2013-04-13 03:40:00 | 2013-04-13 03:52:00 | 1 | 720 | 3.70 | -73.991913 | 40.725792 | -73.984901 | 40.767586 |
| 1D14BCEB15273526346FD543517404D8 | 9F959826431402B410E0B8FA23160AFE | VTS | 1 | `NULL` | 2013-04-13 12:30:00 | 2013-04-13 12:34:00 | 5 | 240 | .42 | -73.989128 | 40.740372 | -73.98513 | 40.742271 |
| 27328100F8702AD2DA7BB48912886CFF | 030C2C1ED4F1CEA429F4DA3DAE4F8B62 | VTS | 1 | `NULL` | 2013-04-13 09:09:00 | 2013-04-13 09:19:00 | 5 | 600 | 2.60 | -73.937439 | 40.824074 | -73.96627 | 40.80394 |
| 89E7FA35C19DB9FA73C7635177216E0C | 2E81DD615637E20C7F50DD58E2FB9BB3 | VTS | 1 | `NULL` | 2013-04-13 13:21:00 | 2013-04-13 13:28:00 | 1 | 420 | .96 | -73.997253 | 40.722458 | -73.989777 | 40.734608 |

4. What MySQL data types/len would you need to store each of the fields?
   - medallion: `char(32)`
   - hack_license: `char(32)`
   - vendor_id: `char(3)`
   - rate_code: `int(4)`
   - store_and_fwd_flag: `char(1)`
   - pickup_datetime: `datetime`
   - dropoff_datetime: `datetime`
   - passenger_count: `int(4)`
   - trip_time_in_secs: `int(16)`
   - trip_distance: `decimal(4,2)`
   - pickup_longitude: `decimal(8,6)`
   - pickup_latitude: `decimal(8,6)`
   - dropoff_longitude: `decimal(8,6)`
   - dropoff_latitude: `decimal(8,6)`
5. What is the geographic range of your data?
   - Constrained to global limits:
     - Minimum corner: -74.069908, -159.435000
     - Maximum corner: 74.035930, 100.987900
     ![Global Limits Map](/img/globallimits.png)
   - I kept trying to find a constraint where it would be reasonably limited to the NYC area, but I kept ending up with maximum and minimum lat/lons that were less than a mile from the corners of my boundaries despite them being 350mi away from NYC
6. What is the average trip distance?
   - Odometer distance: 2.862899
   ![Odometer Distance Histogram](/img/odohist.png)
   - Haversine distance: 11.55658
   ![Haversine Distance Histogram](/img/havhist.png)
   - The average haversine distance is way larger than the odometer distance, which should not be the case. The haversine distance measures a straight line between two points on the Earth's surface without cutting through the ground. For shorter distances, this isn't too much different than just a straight line shot from start to finish, or "as the crow flies." Taxis, on the other hand, must follow city roads and cannot (usually) cut diagonally across blocks. This is also known as the "Manhattan distance," due to the grid-like road layout in Manhattan. This means that typically, the Manhattan distance between two points should be longer than the Haversine. Going diagonally across a block would count for `2*block_length` on the odometer (counting both the edge on the X and Y axes), but only about `1.4*block_length` as far as haversine is concerned (since it can follow the hypotenuse of a right triangle with 45\* angles). The main culprit here is the obnoxiously far away lat/lon coordinates, which despite being rare, are so erroneous that they throw off the average by a significant margin.
   - To resolve this, I estimated the inter-quartile range (IQR) of both the odometer and haversine distances from the histograms. First I divided the number of data points by 4, giving me which data point (when sorted) represents the first quartile. This number is used to initialize a counter. Then, for each bin, if the number of records in a given bin is less than the value of the counter, that number is decremented from the counter. Once the value of the counter is less than the number of records in the current bin, we know that the value of the quartile must exist within the current bin. I then calculate how far through the current bin the quartile is by dividing the counter by the number of records in the bin, then interpolating the value of a record that far through the bin (assuming a linear distribution of records throughout the bin). While this method may not provide an exact value of the quartiles, it should be close enough, and is significantly faster to calculate than sorting all 15 million rows.
   - Using these quartiles, the IQR can be calculated by subtracting Q3 from Q1. A common outlier threshold is given as `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]`. After the quartiles were calculated, the script was run a second time to re-calculate the average distances with outliers removed.

     | | Odometer | Haversine |
     | --- | --- | --- |
     | Lower Outlier Threshold | -2.1092 | -0.9025 |
     | 1st Quartile | 1.0693 | 0.7777 |
     | 3rd Quartile | 3.1883 | 2.4579 |
     | Upper Outlier Threshold | 6.3668 | 4.1381 |
   - Average Odometer distance (outliers removed): 1.9697
     - 1,433,519 outliers removed (9.49% of records)
   - Average Haversine distance (outliers removed): 1.5221
     - 1,267,172 outliers removed (8.39% of records)
   - This makes a lot more sense, as the average odometer distance is slightly larger than the average haversine distance. The actual ratio of odometer to haversine distance is 1.2941, which is pretty close to the theoretical ratio of 1.4142 (or the square root of 2). This is especially true when our original averages had a ratio of 0.2477.
7. What are the distinct values for each field?
   - Vendor ID:

   | Vendor ID | Count |
   | --- | --- |
   | CMT  | 7,582,519 |
   | VTS | 7,517,943 |
   - Rate Codes:

   | Rate Code | Count |
   | --- | --- |
   | 0 | 1,145 |
   | 1 | 14,768,822 |
   | 2 | 254,687 |
   | 3 | 21,937 |
   | 4 | 14,566 |
   | 5 | 39,118 |
   | 6 | 164 |
   | 7 | 1 |
   | 8 | 2 |
   | 9 | 1 |
   | 65 | 2 |
   | 77 | 1 |
   | 206 | 1 |
   | 208 | 1 |
   | 210 | 14 |
   - Store and Forward Flags

   | Flag | Count |
   | --- | --- |
   | `NULL` | 7,518,657 |
   | N | 7,451,835 |
   | Y | 129,970 |
   - Passenger Counts

   | Passenger Count | Count |
   | --- | --- |
   | 0 | 229|
   | 1 | 10,707,067 |
   | 2 | 1,985,741 |
   | 3 | 609,849 |
   | 4 | 298,146 |
   | 5 | 890,115 |
   | 6 | 609,313 |
   | 8 | 1 |
   | 9 | 1 |
8. For other numeric types besides lat and lon, what are the min and max values?

   | Field | Min | Max |
   | --- | --- | --- |
   | Mileage | 0 | 100 |
   | Haversine Distance | 0 | 11,911.91 |
   | Trip Time (s) | 0 | 10,800 |
   | Passengers | 0 | 9 |
   | Rate Code | 0 | 210 |
9. Create a chart which shows the average number of passengers each hour of the day.
   ![Number of Passengers Per Hour](/img/perhour.png)
10. Create a new CSV file which has only one out of every thousand rows.
    - Done, 14,994 rows in new CSV (excluding header)
11. Repeat step 9 with the reduced dataset and compare the two charts.
    ![Number of Passengers Per Hour, Small Dataset](/img/perhoursmall.png)
    - Aside from the scale being used, these two charts appear nearly identical. There are some minor differences, such as the 4pm hour taking slightly more people in the reduced dataset than in the full dataset, however the general trend is maintained in both charts. This is likely due to the fact that the reduced dataset was obtained by taking regular samples throughout the entire dataset, which appears to be somewhat sorted by date and time.
