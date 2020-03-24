import pickle

class L(object):

    def __init__(self):
        self.dfs = []

    def pload(self,fname):

        with open("data/"+fname+".p", "rb") as pfile:
            df = pickle.load(pfile)
        self.dfs.append(df)
        
        return df
