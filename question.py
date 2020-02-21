import numpy as np
import pandas as pd
import json

def priRegion(r,indent=" "*4):
    print("\n\n%s##################################"%indent)
    print("%s########  診療科 : %s   ########" %(indent,r))
    print("%s##################################\n"%indent)

def showItems(df_,key,dfKey,regions,indent=" "*4):
    print("########### 質問項目 : %s    ############## "%key)
    df = df_.copy()
    for r in regions:
        cond = r == df[dfKey[1]]
        priRegion(r)

        dfSort = df.loc[cond].sort_values(by=dfKey[2])
        hosp = dfKey[2]

        #print("%s### 病院・グループ名 : %s  ####" %(indent,key))
        for k,v in dfSort.T.items():
            print("\n%s### %s ###  :   \n-->%s"%(indent*2,v[hosp],v[key]))


def showBusinnes(df_,region,dfKey):
    df = df_.copy()
    cond = region == df[dfKey[1]]
    dfSort = df.loc[cond].sort_values(by=dfKey[2])
    dfSort["count"] = 1 

    table = dfSort.pivot_table(values="count",index=dfKey[2],columns=dfKey[5],aggfunc = np.mean).replace({np.nan:""})
    display(table)


def showSpecificItems(df,key,dfKey,indent=" "*4):
    #print("%s### 病院・グループ名 : %s  ####" %(indent,key))
    display(df.loc[:,[dfKey[2],key]])

def showSpecificAll(df,key,regions,dfKey):
    for r in regions:
        cond = r == df[dfKey[1]]
        priRegion(r)
        showSpecificItems(df.loc[cond],key,dfKey)

def sumRegional(df,regions,dfKey):
    for r in regions:
        cond = r == df[dfKey[1]]
        priRegion(r)
        sumOneHospInfo(df,dfKey)


def sumOneHospInfo(df,dfKey):
    inds = df.index
    for i in inds:
        dic = df.T[i].to_dict()
        del dic[dfKey[0]]
        del dic[dfKey[1]]
        print(json.dumps(dic,indent=4,ensure_ascii=False))
