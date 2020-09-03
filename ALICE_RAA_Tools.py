import numpy as np

def create_dictionary(li):
    dictionary = {}
    for i in li:
        if (type(i[0]) != int or type(i[1]) != int ):
            raise ValueError("Die Liste darf nur ganze Zahlen beinhalten!")
        dictionary[str(i[0]) + "-" + str(i[1])] = i
    for i in dictionary:
        print("processing centrality range: " + str(i) + "% - (" + str(dictionary[i][0]) + "/" + str(dictionary[i][1]) + ")")
    return dictionary

def create_event_histos(input):
    return np.histogram(input, bins=200, range=(0,2000))

def count_lines(file):
    with open(file, 'r') as f:
        nLines=0
        for line in f:
            nLines += 1
    return nLines

def find_centralities(dic, value):
    ret = []
    for key in dic:
        if (dic[key][0] <= value and dic[key][1] > value):
            ret.append(key)
    return ret

def get_bin_width(bins):
    fBinWidth=[]
    nBins = len(bins)-1
    for i in range(0,nBins):
        fBinWidth.append((bins[i+1]-bins[i]))
    return fBinWidth

def get_bins():
    fBinsPt = [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
           0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1, 1.1,
           1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.2, 2.4, 2.6,
           2.8, 3, 3.2, 3.4, 3.6, 3.8, 4, 4.5, 5, 5.5, 6, 6.5, 7, 8,
           9, 10,11, 12, 13, 14, 15]
    return fBinsPt

def fehlerberechnung(h1, h1err, nc1, h2, h2err, nc2):
    return np.sqrt((np.divide(h1err*nc2,h2*nc1))**2 + (np.divide(h1*nc2*h2err,h2*h2*nc1))**2)

#def fill_hist(hist, bins, value):
#    return hist + np.histogram(value, bins)[0]