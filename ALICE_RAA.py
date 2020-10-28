import ALICE_RAA_Tools as at
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np

listCentralities = [(0,5), (30,40), (40,50), (70,80)]
centralities = at.create_dictionary(listCentralities)

# read events
event_lines = at.count_lines('event_information.csv')
print("Number of events: '" + str(event_lines) + "'!")

df_events = pd.read_csv("event_information.csv", header=None, names=['eventMult', 'eventCent'])

print(df_events.head())

for key in centralities:
    df_events[key] = False

print(df_events.head())

dicEventsCent = {}
for row in df_events.iterrows():
    keys = at.find_centralities(centralities, row[1]['eventCent'])
    if keys:
        for cent in keys:
            df_events.loc[row[0], cent] = True
            if cent in dicEventsCent:
                dicEventsCent[cent] += 1
            else:
                dicEventsCent[cent] = 1

print(dicEventsCent)

hNTPC_0_100, fBins = at.create_event_histos(df_events['eventMult'])
hNTPC_30_40, fBins = at.create_event_histos(df_events[df_events['30-40'] == True]['eventMult'])

plt.errorbar(fBins[:-1], hNTPC_0_100, yerr=1, fmt='g+', label='0-100%')
plt.errorbar(fBins[:-1], hNTPC_30_40, yerr=1, fmt='b.', label='30-40%')

plt.yscale('log')
plt.xlabel('Number TPC tracks')
plt.ylabel('Counts/N')
plt.legend(loc='upper right')
plt.show()


plt.hist2d(df_events['eventMult'],df_events['eventCent'], bins=(200,100), range=[[0, 2000], [0, 100]], cmap=plt.cm.jet, norm=mpl.colors.LogNorm())
plt.colorbar()
plt.xlabel('Number TPC tracks')
plt.ylabel('Centrality')
plt.show()

#eingabe = input('Ihre Eingabe')

# read tracks
track_lines = at.count_lines('track_information.csv')
print("Number of tracks: '" + str(track_lines) + "'!")

dicMomCent = {}
for key in centralities:
    dicMomCent[key] = []

df_tracks = pd.read_pickle("./track_info.pkl", 'bz2').to_numpy()
print("loaded")

for line in df_tracks:
    keys = at.find_centralities(centralities, line[1])
    if keys:
        for key in keys:
            dicMomCent[key].append(line[0])


fBinsPt = at.get_bins()
fBinWidth = at.get_bin_width(fBinsPt)
x_bin_width = np.asarray(fBinWidth)/2

dic_nColl = {'0-5': 1686.87, '0-10': 1502.7, '5-10': 1319.89, '10-20': 923.89,
             '20-30': 558.68, '30-40': 321.20, '40-50': 171.67, '50-60': 85.13,
             '60-70': 38.51, '70-80': 15.78, '80-90': 6.32}

print(dic_nColl)

hist_0_5, _ = np.histogram(dicMomCent['0-5'], fBinsPt)
hist_0_5 = hist_0_5 / fBinWidth
hist_0_5 = hist_0_5 / dicEventsCent['0-5']

hist_70_80, _ = np.histogram(dicMomCent['70-80'], fBinsPt)
hist_70_80 = hist_70_80 / fBinWidth
hist_70_80 = hist_70_80 / dicEventsCent['70-80']

hist_0_5_err = np.sqrt(hist_0_5)/dicEventsCent['0-5']
hist_70_80_err = np.sqrt(hist_70_80)/dicEventsCent['70-80']

plt.errorbar(fBinsPt[:-1],hist_0_5, xerr=x_bin_width, yerr=hist_0_5_err, fmt='r+', label='0-5%')
plt.errorbar(fBinsPt[:-1],hist_70_80, xerr=x_bin_width, yerr=hist_70_80_err, fmt='r+', label='70-80%')

plt.yscale('log')
plt.show()    
    
pp = np.genfromtxt('pp_reference.dat')
print(pp)
arr = np.asarray(pp)
#pp, _ = np.histogram(pp, fBinsPt)

hist_0_5 = hist_0_5 / dic_nColl['0-5']
hist_0_5 = hist_0_5 / arr
#hist_0_5_err = hist_0_5_err / dic_nColl['0-5']

hist_70_80 = hist_70_80 / dic_nColl['70-80']
hist_70_80 = hist_70_80 / arr
#hist_70_80_err = hist_70_80_err / dic_nColl['70-80']

plt.errorbar(fBinsPt[:-1], hist_0_5, xerr=x_bin_width, yerr=hist_0_5_err, fmt='r+', label='R_AA')
plt.errorbar(fBinsPt[:-1], hist_70_80, xerr=x_bin_width, yerr=hist_70_80_err, fmt='b+', label='R_AA')
plt.show()   
#event = pd.read_csv("./prepareData/event_info.csv", chunksize=20000)


