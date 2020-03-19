
import math

import pandas as pd
import numpy as np

df = pd.read_csv("07_publication_data.csv", sep=",", header=None,
                 names=["cell_id", "dendrite_id", "spine_id", "session_no",
                        "intensity", "lambda1", "lambda2", "dist",
                        "cofmas_x", "cofmas_y", "11", "12", "13"])


print(df.head())


# make a unique id

i = math.ceil(np.log10(np.max(df["cell_id"])))+1
j = math.ceil(np.log10(np.max(df["dendrite_id"])))+1
k = math.ceil(np.log10(np.max(df["spine_id"])))+1


df["uid"] = 10**(i+j+k)*df["cell_id"] + \
            10**(j+k)*df["dendrite_id"] + \
            10**(k)*df["spine_id"]


#

spines_session_1 = df[df["session_no"]==1]["uid"]
spines_session_2 = df[df["session_no"]==2]["uid"]

new_spines =  np.setdiff1d(spines_session_2,
                           spines_session_1)

srv_spines = new_spines
# print(new_spines)
# print(len(new_spines))


session, srvprb = [], []

for s_no in range(3, np.max(df["session_no"])+1):
    
    srv_until_sno =df[(df["session_no"]==s_no) & (df['uid'].isin(new_spines))]

    srv_spines = srv_until_sno["uid"]

    srvprb.append(len(srv_spines)/len(new_spines))
    session.append(s_no-2)


print(session, srvprb)



session, srvprb = [], []

for s_no in [4, 6]:
    
    srv_until_sno =df[(df["session_no"]==s_no) & (df['uid'].isin(new_spines))]

    srv_spines = srv_until_sno["uid"]

    srvprb.append(len(srv_spines)/len(new_spines))
    session.append(s_no-2)


print(session, srvprb)
