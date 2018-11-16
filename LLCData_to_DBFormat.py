#commit

# Converts visChallenge data to a format more easily manipulated into an influxDB database.

import pandas as pd

bldg = input('bldging id: ').upper()
#day = input('day: ')

print('searching for file...')

filepath = "/Users/joseph/Documents/VisChallengeData/Vis_LLC_BLDG_" + bldg + "/"
file = "LLC_BLDG_"+bldg+"_OCT-4-NOV-13_VisChallenge.csv"

print('file found, buildind main data frame...')

main_df = pd.read_csv(filepath+file, sep =',', header=0)

print('splitting main dataframe into sources...')

hotIN_df = main_df.copy()
hotIN_df.drop(['coldInFlowRate', 'hotOutPulseCount'], axis=1, inplace=True)

coldIN_df = main_df.copy()
coldIN_df.drop(['hotInFlowRate', 'hotOutPulseCount'],axis=1, inplace=True)

hotRETURN_df = main_df.copy()
hotRETURN_df.drop(['hotInFlowRate', 'coldInFlowRate'],axis=1, inplace=True)

print('uploading sources to folder...')

path="/Users/joseph/Desktop/GRA/InfluxSemesterProject/LLC_BLDG_"+bldg+"/"
hotIN_df.to_csv(path + "hotIN_LLC_BLDG_"+bldg+"_OCT-4-NOV-13_Testdata.csv", sep=',', index=False)
coldIN_df.to_csv(path + "coldIN_LLC_BLDG_"+bldg+"_OCT-4-NOV-13_Testdata.csv", sep=',', index=False)
hotRETURN_df.to_csv(path + "hotRETURN_LLC_BLDG_"+bldg+"_OCT-4-NOV-13_Testdata.csv", sep=',', index=False)


print('\ndone')