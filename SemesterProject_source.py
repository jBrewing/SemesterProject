# ---------------------------------------------------------------------------
# SemesterProject_source.py
#
# Author(s):  Joseph Brewer / Jaxon White
# Creation Date: 11/14/2018
#
# Development Environment:
#   Pycharm
#   Python 3.7
#
# This script is a general visualization tool used in conjunction with
# the ongoing water-related-energy study, under the CUASHI research
# umbrella, focusing on the Living & Learning Community at Utah State.
# Based on input, it queries an InfluxDB database, where
# water consumption data is stored.  Based on user input,
# the script performs a variety of tasks, including:
#   - comparison of water-related energy use between buildings
#   - outputs a variety of visualizations for water-related energy use
#   - performs some basic statistical analysis on water-related energy use.
#
# ----------------------------------------------------------------------------

import pandas as pd
from influxdb import InfluxDBClient
import matplotlib.pyplot as plt
import numpy as np
#from SemesterWork import Resample

print('Receiving inputs...')
# Input parameters.
# Available dates - 2018/10/10 - 2018/11/10
#       Dates - Do not remove 'T' or 'Z' - required influxDB syntax.
#       bldgID - Do not remove " " or ' ' - required influxDB syntax
beginDate = "'2018-10-10T05:00:00Z'"
endDate = "'2018-10-10T17:00:00Z'"
bldgID = "'F'"


print('Connecting to database...')
# Create client object with InfluxDBClient library
# Set database.
client = InfluxDBClient(host='influxdbubuntu.bluezone.usu.edu', port=8086)
client.switch_database('LLC_FlowData')


print('Assembling query...')
# Build query by concatenating inputs into query.  InfluxDB query language has several
# requirements.  Fields/Tags must be bracketed with " " and the field/tag values must be
# bracketed with ' '.
# Query returns a 'ResultSet" type.  Have to convert to pandas dataframe.
query = """SELECT "flowrate", "source" FROM "flow" WHERE "buildingID" ="""+bldgID+""" AND time >= """+beginDate+""" AND time <= """+endDate+""""""
#"source" = """+source+""" AND

print('Retrieving data...')
# Convert returned ResultSet to Pandas dataframe with list
# and get_points. Set dataframe index as datetime.
main = client.query(query)

main_Ls = list(main.get_points(measurement='flow'))
main_Df = pd.DataFrame(main_Ls)
main_Df.sort_values(by=['source'], inplace=True)
main_Df['time'] = pd.to_datetime(main_Df['time'])
main_Df.set_index('time', inplace=True)

print('Data retrieved...')

print('Splitting Data frame...')
cold_Df = main_Df[main_Df['source'] == 'coldIN'].copy()
cold_Df.sort_index(inplace=True)
cold_Df.drop(['source'], axis ='columns', inplace=True)

hot_Df = main_Df[main_Df['source'] == 'hotIN'].copy()
hot_Df.sort_index(inplace=True)
hot_Df.drop(['source'], axis ='columns', inplace=True)

print('Resampling data...')
# Resample tool
# Input resample rule:
#   Options are: Daily, #D.
#                Weekly, #W,
#                Hourly, #H,
#                Minute, #T.
resampleRule = '15T'

hotFinalAvg = hot_Df.resample(rule=resampleRule, base=0).mean()
#hotFinalMax = hot_Df.resample(rule=resampleRule, base=0).max()
#hotFinalMin = hot_Df.resample(rule=resampleRule, base=0).min()

coldFinal = cold_Df.resample(rule = resampleRule , base=0).mean()
#coldFinalMax = cold_Df.resample(rule=resampleRule, base=0).max()
#coldFinalMin = cold_Df.resample(rule=resampleRule, base=0).min()


# Plot results - raw data, resampled data, resampled with stats.
print('Plotting results...')

# Initialize figures and subplots
gridsize=(3,2)
fig=plt.figure(figsize=(12,8))
axHot1 = plt.subplot2grid(gridsize, (0,0))
plt.xticks(fontsize=8)
axHot2 = plt.subplot2grid(gridsize, (1,0))
plt.xticks(fontsize=8)
axHot3 = plt.subplot2grid(gridsize, (2,0))
plt.xticks(fontsize=8)
axCold1 = plt.subplot2grid(gridsize, (0,1))
plt.xticks(fontsize=8)
axCold2 = plt.subplot2grid(gridsize, (1,1))
plt.xticks(fontsize=8)
axCold3 = plt.subplot2grid(gridsize, (2,1))
plt.xticks(fontsize=8)

# Plot raw data
axHot1.plot(hot_Df, color='red', label='1-Sec HOT Data')
axHot1.set_xlim(beginDate, endDate)

axCold1.plot(cold_Df, color='blue', label='1-Sec COLD Data')
axCold1.set_xlim(beginDate, endDate)

# Plot resampled data
axHot2.plot(hot_Df, color='grey', alpha=0.5, linewidth=0.5)
axHot2.plot(hotFinalAvg, color='red', label=resampleRule+' resample')
#axHot2.plot(hotFinalMax, color='lightsalmon', label=resampleRule+' max.')
#axHot2.plot(hotFinalMin, color='maroon',label=resampleRule+' min.')
axHot2.set_xlim(beginDate, endDate)

axCold2.plot(cold_Df, color='grey', alpha=0.5, linewidth=0.5)
axCold2.plot(coldFinal, color='blue', label=resampleRule+' resample')
#axCold2.plot(coldFinalMax, color='cyan',label=resampleRule+' max.')
#axCold2.plot(coldFinalMin, color='navy',label=resampleRule+' min.')
axCold2.set_xlim(beginDate, endDate)

# Plot histograms
dataHot = hotFinalAvg['flowrate']
binwidthHot = (dataHot.max()-dataHot.min())/15
axHot3.hist(dataHot, bins=np.arange(min(dataHot), max(dataHot), binwidthHot), color='red')

dataCold = coldFinal['flowrate']
binwidthCold = (dataCold.max()-dataCold.min())/15
axCold3.hist(dataCold, bins=np.arange(min(dataCold), max(dataHot), binwidthCold), color='blue')

# Plot Formatting
fig.suptitle('Water Use Data Vis/Analysis for Building: '+bldgID+' FOR: '+beginDate+'-'+endDate, fontsize=14, weight='bold')
plt.tight_layout(pad=5, w_pad=2, h_pad=1.75)


# Hot
axHot1.legend(loc='upper left')
axHot1.set_ylabel('GPM')
axHot1.grid(True)
axHot1.set_title('Raw hot water flowrate', fontsize=10, weight ='bold')

hotLegend = axHot2.legend(loc='upper left')
for label in hotLegend.get_texts():
    label.set_fontsize(6)
axHot2.set_ylabel('GPM')
axHot2.set_title('Resampled hot water flowrate', fontsize=10, weight='bold')
axHot2.grid(True)

axHot3.set_xlabel('Gallons per Minute')
axHot3.set_ylabel('Freq.')
axHot3.set_title('Resampled GPM distribution', fontsize=10, weight='bold')

# Cold
axCold1.legend(loc='upper left')
axCold1.set_ylabel('GPM')
axCold1.grid(True)
axCold1.set_title('Raw cold water flowrate', fontsize=10, weight ='bold')

coldLegend = axCold2.legend(loc='upper left')
for label in coldLegend.get_texts():
    label.set_fontsize(6)
axCold2.set_ylabel('GPM')
axCold2.set_title('Resampled cold water flowrate', fontsize=10, weight='bold')
axCold2.grid(True)

axCold3.set_xlabel('Gallons per Minute')
axCold3.set_ylabel('Freq.')
axCold3.set_title('Resampled GPM distribution', fontsize=10, weight='bold')









plt.show()

print('done')

