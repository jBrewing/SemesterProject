#__________________________________________________
#
# flowToInfluxDB.py
#
# Author: Joseph Brewer
# Developed for: CEE6110 - Hydroinformatics Semester Project
#
# Description:  This script is a backup should our software developer
# not finish the final product on time.  This script inputs LLC flow data
# to a CSV reader, connects to an InfluxDB database on a remote Ubuntu-linux
# machine, and uploads flow data to a database within the influxDB instance.
#
# Requirements: Ubuntu machine on and running
#
#Last edited: Friday, 11/18/18
#__________________________________________________



import pandas as pd
from influxdb import DataFrameClient

bldg = input("bldg ID: ").upper()
source = input("'hotIN', 'coldIN', or 'hotRETURN': ")

print('\nlocating file...')


# Used for testing connection.
#path="/Users/joseph/Desktop/GRA/InfluxSemesterProject/"
#file = "test.csv"

path="/Users/joseph/Desktop/GRA/InfluxSemesterProject/LLC_BLDG_"+bldg+"/"
file = source + "_LLC_BLDG_"+bldg+"_OCT-4-NOV-13_Testdata.csv"

print('\nfile located, building dataframe...')

csvReader = pd.read_csv(path+file, sep=',', index_col=0, parse_dates=True, infer_datetime_format=True)

print('\ndataframe complete, connecting to influxDB...')

client = DataFrameClient(host='influxdbubuntu.bluezone.usu.edu', port=8086)
client.switch_database('LLC_FlowData')

print('\nconnection established, uploading to influxdb...')

client.write_points(csvReader, 'flow', {'buildingID':bldg, 'source':source}, batch_size=100, protocol='line')

print('\n\nDONE!')


