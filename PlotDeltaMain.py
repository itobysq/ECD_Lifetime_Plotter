#This program automatically plots the data from a given directory
#It plots the delta over time, here is how it works
# 1. Determine the prefix of the unique devices
# 2. For each of the unique prefixes, divide up the files to the respective prefix
# 3. Sort the data by date and combine it into an array
import os, glob, datetime

os.chdir("C:\\Users\\toby\\Dropbox\\NSF_SBIR_Grant\\AgingData\\AgingCPU\\Aug20")


def FindPrefixes():
    fns = glob.glob('*NicePD*')
    devnames = []
    for fn in fns:
        start = 0
        #start = fn.find('_')
        end = fn.rfind('_')
        devname = fn[start:end]
        devnames.append(devname)
    newList = list(set(devnames))
    return newList

def SortPhotodiodeData(uniques):
    fns = glob.glob('*PD*')
    # Initialilze the Materials and filename matricies
    Materials = []
    matrix = [[] for x in xrange(len(uniques))] 
    # Bin the unique data
    for fn in fns:
        nindex = 0
        for name in uniques:
            if fn.find(name) !=-1:
                if fn.count('_')==name.count('_')+1:
                    matrix[nindex].append(fn)
            nindex = nindex+1
    endex = 0
    # Stash it into the Materials Dictionary
    
    for name in uniques:
        matrix[endex].sort(key=lambda x: os.stat(os.path.join(os.getcwd(), x)).st_mtime)
        Materials.append({name:matrix[endex]})
        endex = endex+1
    return Materials

def DictToArray(Materials):
    tardir = os.getcwd()
    print tardir
    f=''
    rawdata = [] 
    # First, go through all of the the sample, filepath dictionaries
    for dick in Materials:
        matdata = [[],[]]
        name = dick.keys()
        files = dick.values()
        # access the files for each sample
        for i in range(len(files[0])):
            f = files[0][i]
            fullf = tardir+'\\'+f
            with open(fullf, "rb") as f:
                
        # calculate the delta, the try statement allows this program to be 
        # used with transition files or with PD files
                first = f.readline()
                second = f.readline()
            fsplit=[x for x in first.split()]
            ssplit = [x for x in second.split()]
            date = str(fsplit[0]) + ' ' + str(fsplit[1])
            try: 
                delta=float(fsplit[2])-float(ssplit[2])
            except IndexError:
                print fullf
                delta = float(ssplit[0])
            matdata[0].append(date)
            matdata[1].append(delta)
        # format the data to a sample, time vs. delta key-value pair
        rawdata.append({name[0]:matdata})
    return rawdata

# The objective of this short script is to convert the date values into time (in hours)
#1. access the date values
def ToHours(rawdata):
    tohours = []
    for dick in rawdata:
        plotdata = dick.values()
        ckey = dick.keys()
        timedata = plotdata[0][0]
        orgin = timedata[0]
        FMT = '%Y-%m-%d %H:%M:%S'
        ltimel = []
        for timed in timedata:
            norgin = datetime.datetime.strptime(orgin, FMT)
            ntime = datetime.datetime.strptime(timed, FMT)
            duration = abs(ntime - norgin)
            ltime = duration.total_seconds()/3600
            ltimel.append(ltime)
        # insert the new delta time and zip the dictionary back up
        plotdata[0][0]=ltimel
        tohours.append({ckey[0]:plotdata})
    return tohours
def BigDictToArray(Materials):
    tardir = os.getcwd()
    f=''
    rawdata = []
    for dick in Materials:
        matdata = [[],[]]
        name = dick.keys()
        files = dick.values()
        for i in range(len(files[0])):
            f = files[0][i]
            fullf = tardir+'\\'+f
            tlimit = datetime.timedelta(minutes = 10)
            FMT = '%Y-%m-%d %H:%M:%S'
            with open(fullf, "rb") as f:
                first = f.readline()
                for line in f: 
                    fsplit=[x for x in first.split()]
                    ssplit = [x for x in line.split()]
                    fdate = str(fsplit[0]) + ' ' + str(fsplit[1])
                    sdate = str(ssplit[0]) + ' ' + str(ssplit[1])
                    ffmt= datetime.datetime.strptime(fdate, FMT)
                    sfmt = datetime.datetime.strptime(sdate, FMT)
                    duration = abs(ffmt - sfmt) 
                    delta=float(fsplit[2])-float(ssplit[2])
                    date = str(fsplit[0]) + ' ' + str(fsplit[1])
                    if duration < tlimit:
                        delta=float(fsplit[2])-float(ssplit[2])
                        matdata[0].append(date)
                        matdata[1].append(delta)
                    first = line
        rawdata.append({name[0]:matdata})
    return rawdata

def ExtendMaterialFilePath(Materials):
    Materials2 = []
    for matx in range(len(Materials)):
        Materials2.append({Materials[matx].keys()[0]:os.getcwd()+'\\'+str(Materials[matx].values()[0][0])})
    return Materials2
#This function makes a simple plot of just one set of data 
def SimplePlot(pindex):
    import matplotlib.pyplot as plt
    plotdata = tohours[pindex].values()
    plt.plot(plotdata[0][0][0],plotdata[0][0][1],'ro')
    plt.xlim(xmax = 300)
    plt.xlabel('Hours')
    plt.ylabel('PDresponse')
    plt.title(str(tohours[pindex].keys()))
    plt.show()
    
#This function plots all of the data
def AllPlots():
    from numpy import linspace
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    themax = 0.0
    colors = cm.rainbow(linspace(0, 1, len(tohours)))
    for dindex, c in zip(range(len(tohours)),colors):
        plotdata = tohours[dindex].values()
        plt.scatter(plotdata[0][0][0],plotdata[0][0][1],color =c,label=str(tohours[dindex].keys()))
        #plt.plot(plotdata[0][0][0],plotdata[0][0][1],color =c,label=str(tohours[dindex].keys()))
        cmax = abs(plotdata[0][0][1][1])
        if cmax > themax:
            themax = cmax
    ylims = 1.5*themax
    plt.grid('on')
    #plt.xlim(xmin = -0.1)
    #plt.xlim(xmax = 300)
    plt.ylim(ymax = ylims)
    plt.ylim(ymin = -ylims)
    plt.legend(loc='best')
    plt.xlabel('Hours')
    plt.ylabel('PDresponse')
    plt.title('here are the plots')
    plt.show()

    #rename the devices 
def rename(dir, pattern, titlePattern):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
        os.rename(pathAndFilename, 
                  os.path.join(dir, titlePattern % title + ext))
        
#os.chdir('H:\\AllNovAging\\PlotItAll\\Nov52')
#[os.rename(f, f.replace('PD', 'PDh'))
#for f in os.listdir('.') if not f.startswith('.')]
#print 'all done'   

uniques = FindPrefixes()
Materials = SortPhotodiodeData(uniques)
Materials2 = ExtendMaterialFilePath(Materials)
flist = Materials[0].values()
fpath = os.getcwd() + '\\' + flist[0][0]
statinfo = os.stat(fpath)
if statinfo > 1000:
    rawdata = BigDictToArray(Materials)  
else:
    rawdata = DictToArray(Materials)     
#rawdata = DictToArray(Materials)
tohours = ToHours(rawdata)
for x in range(len(uniques)):
    SimplePlot(x)
AllPlots()
