#commit

# Converts visChallenge data to a format more easily manipulated into an influxDB database.

import pandas as pd
import os

bldg = input('bldging id: ').upper()

filepath = "/Users/joseph/Documents/Datalog_backups/LLC_BLDG_" + bldg + "/"
files = os.listdir(filepath)
print(files)

dateID = input('date: ')
timeID = input('time: ')

print('searching for file...')


file = "multi_meter_datalog_LLC_BLDG_"+bldg+"_"+dateID+"_"+timeID+".csv"

print('file found, buildind main data frame...')

main_df = pd.read_csv(filepath+file, sep =',', header=1, low_memory=False, index_col=0,
                      parse_dates=True, infer_datetime_format=True)

print('splitting main dataframe into sources...')

hotIN_df = main_df.copy()
hotIN_df.drop(['RecordNumber','coldInVoltage', 'coldInFlowRate','coldInVolume','hotInVoltage',
               'hotInVolume','hotOutPulseCount','hotOutFlowRate', 'hotOutVolume'], axis=1, inplace=True)

coldIN_df = main_df.copy()
coldIN_df.drop(['RecordNumber','coldInVoltage','coldInVolume','hotInVoltage', 'hotInFlowRate',
               'hotInVolume','hotOutPulseCount','hotOutFlowRate', 'hotOutVolume'],axis=1, inplace=True)

hotRETURN_df = main_df.copy()
hotRETURN_df.drop(['RecordNumber','coldInVoltage', 'coldInFlowRate','coldInVolume','hotInVoltage', 'hotInFlowRate',
               'hotInVolume','hotOutPulseCount', 'hotOutVolume'],axis=1, inplace=True)

print('uploading sources to folder...')

path="/Users/joseph/Desktop/GRA/InfluxSemesterProject/LLC_BLDG_"+bldg+"/"
hotIN_df.to_csv(path + "hotIN_LLC_BLDG_"+bldg+"_OCT-4-NOV-13_Testdata.csv", sep=',', index=True)
coldIN_df.to_csv(path + "coldIN_LLC_BLDG_"+bldg+"_OCT-4-NOV-13_Testdata.csv", sep=',', index=True)
hotRETURN_df.to_csv(path + "hotRETURN_LLC_BLDG_"+bldg+"_OCT-4-NOV-13_Testdata.csv", sep=',', index=True)


print('\ndone')