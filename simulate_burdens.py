import simlib_evo_v2 as sl
import pandas as pd
from ast import literal_eval
from statistics import mean

df = pd.read_csv("library_full_df.csv")


def calc_burden(construct, input_conditions):
    parts = ["part0", "part1", "part2", "part3", "part4", "part5"]
    burden = 0
    for i, name in enumerate(parts):
        if sl.part_catalogue[construct[name]] == "TF":
            burden = burden + mean(literal_eval(construct[input_conditions])[i])
    return burden


burden_minus_minus = []
burden_minus_plus = []
burden_plus_minus = []
burden_plus_plus = []


for i in range(len(df)):
    burden_minus_minus.append(calc_burden(df.iloc[i], "-/-"))
    burden_minus_plus.append(calc_burden(df.iloc[i], "-/+"))
    burden_plus_minus.append(calc_burden(df.iloc[i], "+/-"))
    burden_plus_plus.append(calc_burden(df.iloc[i], "+/+"))


df["burden -/-"] = burden_minus_minus
df["burden -/+"] = burden_minus_plus
df["burden +/-"] = burden_plus_minus
df["burden +/+"] = burden_plus_plus

df.to_csv("library_full_df_with_burdens.csv")

print("done")