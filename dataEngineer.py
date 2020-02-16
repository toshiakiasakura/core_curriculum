import pandas as pd
import numpy as np


termN = ["term%d"%i for i in range(1,7)]
item = "施設名"
rank = "順位"

def getSubLists(file_):
    ''' get lists of submission 
    '''
    useCols = [1,2,3,4]
    colN = ["index1","item1","index2","item2"]
    index = 5

    x1 = pd.ExcelFile(file_) 
    shName = x1.sheet_names[0]
    df = pd.read_excel(file_,sheet_name=shName,usecols=useCols)
    df.columns = colN
    df = df.iloc[index:]
    df = df.dropna(axis=0,how="any",subset=[colN[0]])

    df1 = df.loc[:,colN[0:2]]
    cond1 = df1[colN[0]].isnull() == False
    df1 = df1.loc[cond1]

    df2 = df.loc[:,colN[2:4]] 
    cond2 = df2[colN[2]].isnull() == False
    df2 = df2.loc[cond2]

    dfSub = np.vstack((df1.values[1:] ,df2.values[1:]))
    dfSub = pd.DataFrame(dfSub,columns=[rank,item])
    dfSub.index = dfSub[rank]
    del dfSub[rank]
    return(dfSub)

def getCandidates(file_):
    '''get candidates list of hospitals. 
    '''
    useCols = [6,7,8,9,10,11]
    index =5

    x1 = pd.ExcelFile(file_)
    shName = x1.sheet_names[0]
    df = pd.read_excel(file_,sheet_name=shName,usecols=useCols)
    df.columns = termN
    df = df.iloc[index:].reset_index(drop=True)
    return(df)

def checkDuplicate(df_):
    vals = df_[item].dropna()
    u,c  = np.unique(vals,return_counts=True)
    if (c > 1 ).sum():
        msg = "重複しているデータがあります."
        print(msg)
        dupLis = u[c>1]
        for d in dupLis:
            cond = df_[item] == d
            display(df_.loc[cond])
    else:
        msg = "重複はありません."
        pinrt(msg)

def checkCandidate(df_,dfCand):
    '''
    Arg: 
        df_ : created in "getSubList".
    '''
    df_ = df_.copy()
    flag = False
    notIn = []
    for k,v in df_.T.items():
        if v[item] == v[item]:
            exist = False
            for t in termN:
                if v[item] in dfCand[t].values:
                    df_.loc[k,"term"] = t
                    exist = True
                    break
            if not exist :
                msg = "注意: 次の名前は候補にありません．"
                print(msg)
                print(k,v[item])
                print()
        else:
            notIn.append(k)
            flag = True
    if flag:
        msg = "注意: 希望順位のリストは全て埋まっていません．以下は埋まっていない希望順位です．"
        print(msg)
        print(notIn)

    return(df_)

def reconstRank(df_,nan=" "):
    '''
    Args:
        df_ : created in "checkCandidate".
    Return:
        dataframe : reconstructed ranks.
    '''

    grp = df_.groupby(by="term")

    dfSum = pd.DataFrame()
    for t in termN:
        df = grp.get_group(t)

        itemNew = "%s_%s"%(t,item)
        rankNew = "%s_%s"%(t,rank)

        df.loc[:,rankNew] = df.index.values
        dfM =df.rename(columns = {item:itemNew})
        dfM = dfM[[itemNew,rankNew]].reset_index(drop=True)
        dfSum = pd.concat((dfSum,dfM),axis=1)
        dfSum = dfSum.replace({np.nan:nan})
    return(dfSum)


