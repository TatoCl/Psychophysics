import pandas as pd
from scipy.stats import norm
from statistics import mean
from os import listdir
from statsmodels.stats.anova import AnovaRM

#d' function
def dPrime(hitRate, FArate):
    stat = norm.ppf(hitRate) - norm.ppf(FArate)
    return stat

#criterion function
def criterion(hitRate, FArate):
    stat = -.5*(norm.ppf(hitRate) + norm.ppf(FArate))
    return stat


dataPath = "data_group/"
fileList = listdir(dataPath)

meanSDTs = pd.DataFrame({"participant" : [], "dPrime" : [], "criterion" : []})
counter = 0
for dataFile in fileList:
    #New ID for each participant
    counter += 1
    pNum = "P-" + str(counter)
    rawData = pd.read_csv(dataPath + dataFile)

    expData = pd.DataFrame(rawData, columns = ["type","shape","condition","key_resp_5.keys", "key_resp_5.rt"])
    expData = expData.rename(columns = {"key_resp_5.rt" : "RT", "key_resp_5.keys" : "response"})

    accuracy = pd.DataFrame({"condition" : ["salient rectangle", "nonsalient rectangle", "salient circle", "nonsalient circle"], "hits" : [0,0,0,0], "misses" : [0,0,0,0], "CRs" : [0,0,0,0], "FAs" : [0,0,0,0]})

    for index, row in expData.iterrows():
        if row["condition"] == "nonsalient" and row["shape"] == "rectangle":
            rowInd = 1
            #Hit
            if row["type"] == "st" and row["response"] == "right":
                accuracy.loc[rowInd,"hits"] += 1
            #Miss
            elif row["type"] == "st" and row["response"] == "left":
                accuracy.loc[rowInd,"misses"] += 1
            #Correct rejection
            elif row["type"] == "nonst" and row["response"] == "left":
                accuracy.loc[rowInd,"CRs"] += 1 #False alarm
            elif row["type"] == "nonst" and row["response"] == "right":
                accuracy.loc[rowInd,"FAs"] += 1

        elif row["condition"] == "salient" and row["shape"] == "rectangle":
            rowInd = 0
            #Hit
            if row["type"] == "st" and row["response"] == "right":
                accuracy.loc[rowInd,"hits"] += 1
            #Miss
            elif row["type"] == "st" and row["response"] == "left":
                accuracy.loc[rowInd,"misses"] += 1
            #Correct rejection
            elif row["type"] == "nonst" and row["response"] == "left":
                accuracy.loc[rowInd,"CRs"] += 1 #False alarm
            elif row["type"] == "nonst" and row["response"] == "right":
                accuracy.loc[rowInd,"FAs"] += 1

        elif row["condition"] == "nonsalient" and row["shape"] == "circle":
            rowInd = 3
            #Hit: go trial where participant responds
            if row["type"] == "st" and row["response"] == "right":
                #loc is index with string, but only works for database
                accuracy.loc[rowInd,"hits"] += 1
            #Miss
            elif row["type"] == "st" and row["response"] == "left":
                accuracy.loc[rowInd,"misses"] += 1
            #Correct rejection
            elif row["type"] == "nonst" and row["response"] == "left":
                accuracy.loc[rowInd,"CRs"] += 1 #False alarm
            elif row["type"] == "nonst" and row["response"] == "right":
                accuracy.loc[rowInd,"FAs"] += 1

        elif row["condition"] == "salient" and row["shape"] == "circle":
            rowInd = 2
            #Hit
            if row["type"] == "st" and row["response"] == "right":
                accuracy.loc[rowInd,"hits"] += 1
            #Miss
            elif row["type"] == "st" and row["response"] == "left":
                accuracy.loc[rowInd,"misses"] += 1
            #Correct rejection
            elif row["type"] == "nonst" and row["response"] == "left":
                accuracy.loc[rowInd,"CRs"] += 1 #False alarm
            elif row["type"] == "nonst" and row["response"] == "right":
                accuracy.loc[rowInd,"FAs"] += 1

    hitRatenonsalientr = accuracy.loc[1]["hits"]/10
    FAratenonsalientr = accuracy.loc[1]["FAs"]/10
    hitRatesalientr = accuracy.loc[0]["hits"]/10
    FAratesalientr = (accuracy.loc[0]["FAs"])/10

    hitRatenonsalientc = accuracy.loc[3]["hits"]/10
    FAratenonsalientc = accuracy.loc[3]["FAs"]/10
    hitRatesalientc = accuracy.loc[2]["hits"]/10
    FAratesalientc = (accuracy.loc[2]["FAs"])/10

    missRatenonsalientr = accuracy.loc[1]["misses"]/10
    rejectionRatenonsalientr = accuracy.loc[1]["CRs"]/10
    missRatesalientr = accuracy.loc[0]["misses"]/10
    rejectionRatesalientr = (accuracy.loc[0]["CRs"])/10

    missRatenonsalientc = accuracy.loc[3]["misses"]/10
    rejectionRatenonsalientc = accuracy.loc[3]["CRs"]/10
    missRatesalientc = accuracy.loc[2]["misses"]/10
    rejectionRatesalientc = (accuracy.loc[2]["CRs"])/10


    dnonsalientr = dPrime(hitRatenonsalientr,FAratenonsalientr)
    criterionnonsalientr = criterion(hitRatenonsalientr,FAratenonsalientr)
    dsalientr= dPrime(hitRatesalientr,FAratesalientr)
    criterionsalientr= criterion(hitRatesalientr,FAratesalientr)

    dnonsalientc = dPrime(hitRatenonsalientc,FAratenonsalientc)
    criterionnonsalientc = criterion(hitRatenonsalientc,FAratenonsalientc)
    dsalientc= dPrime(hitRatesalientc,FAratesalientc)
    criterionsalientc= criterion(hitRatesalientc,FAratesalientc)


    pNumList = [pNum, pNum,pNum,pNum]
    stimuliList = ["salient", "nonsalient","salient","nonsalient"]
    shapeList = ["rectangle", "rectangle", "circle", "circle"]

    hitList=[]
    hitList.append(hitRatesalientr)
    hitList.append(hitRatenonsalientr)
    hitList.append(hitRatesalientc)
    hitList.append(hitRatenonsalientc)

    FAList=[]
    FAList.append(FAratesalientr)
    FAList.append(FAratenonsalientr)
    FAList.append(FAratesalientc)
    FAList.append(FAratenonsalientc)

    missList=[]
    missList.append(missRatesalientr)
    missList.append(missRatenonsalientr)
    missList.append(missRatesalientc)
    missList.append(missRatenonsalientc)

    rejectionList=[]
    rejectionList.append(rejectionRatesalientr)
    rejectionList.append(rejectionRatenonsalientr)
    rejectionList.append(rejectionRatesalientc)
    rejectionList.append(rejectionRatenonsalientc)

    dList =[]
    dList.append(dsalientr)
    dList.append(dnonsalientr)
    dList.append(dsalientc)
    dList.append(dnonsalientc)


    cList=[]
    cList.append(criterionsalientr)
    cList.append(criterionnonsalientr)
    cList.append(criterionsalientc)
    cList.append(criterionnonsalientc)


    newLines = pd.DataFrame({"participant" : pNumList, "stimulus_type" : stimuliList, "shape": shapeList,
                            "hits": hitList, "correct rejections": rejectionList, "false alarms": FAList, "misses": missList, "dPrime" :dList , "criterion": cList})

    meanSDTs = meanSDTs.append(newLines, ignore_index=True) #don't want index duplicates

#remove participant 1 because it was affecting results
meanSDTs = meanSDTs.drop([0,1,2,3])

print(meanSDTs)

#repeated measures anova
model = AnovaRM(data = meanSDTs, depvar = "dPrime", subject = "participant", within = ["stimulus_type","shape"]).fit()
print(model)

#repeated measures anova
model = AnovaRM(data = meanSDTs, depvar = "criterion", subject = "participant", within = ["stimulus_type","shape"]).fit()
print(model)
