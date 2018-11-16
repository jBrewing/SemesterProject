#commit
# Slow as crap, but worth holding on to for project comparison.




import pandas as pd
from influxdb import InfluxDBClient
from progressbar import Percentage, RotatingMarker, ETA,FileTransferSpeed, ProgressBar, Bar

widgets = ['Test: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
           ' ', ETA(), ' ', FileTransferSpeed()]




bldg = input('bldg ID: ').upper()
source = input("'hotIN', 'coldIN', or 'hotRETURN': ")

print('locating file...\n')

path="/Users/joseph/Desktop/GRA/InfluxSemesterProject/LLC_BLDG_"+bldg+"/"
file = source + "_LLC_BLDG_"+bldg+"_OCT-4-NOV-13_Testdata.csv"

print('Connecting to InfluxDB...\n')

client = InfluxDBClient(host='influxdbubuntu.bluezone.usu.edu', port=8086)
client.switch_database('LLC_FlowData')


#path="/Users/joseph/Desktop/GRA/InfluxSemesterProject/"
#file = "test.csv"

print('Reading CSV file...\n')

csvReader = pd.read_csv(path+file, sep=',')

print(csvReader.shape)
print(csvReader.columns)

data = len(csvReader)
pbar = ProgressBar(widgets=widgets, maxval=data).start()

print('Loading data to influxDB\n')


for row_index, row in csvReader.iterrows():
    tag1 = source
    tag2 = bldg
    fieldValue = row[2]
    json_body = [
        {
            "measurement": "flow",
            "tags": {
                "buildingID": tag2,
                "source" : source
            },
            "fields":{
                "flow":fieldValue
            }
        }
    ]
    client.write_points(json_body)




print('done\n')




