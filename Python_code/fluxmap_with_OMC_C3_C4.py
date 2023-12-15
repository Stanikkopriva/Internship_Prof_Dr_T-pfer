# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 11:37:36 2023

@author: stani
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 15:19:51 2023

@author: stani

Creating an exponentialised version of the flux data to then import the omc colorgradient
and create a colorbar
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib as mpl
import math
from lxml import etree
import os
from openpyxl.workbook import Workbook
from sklearn.preprocessing import MinMaxScaler
import numpy as np


#Import flux data set and replace index with unamed column (reaction id)
fluxdata_df = pd.read_csv("./Csv_files/C3_C4_Flux_Solution.csv")
fluxdata_df.set_index("Unnamed: 0",inplace=True)
print(fluxdata_df)

#first_column = fluxdata_df.iloc[:,0]
#print(first_column)


#make a dictionary with paths and reaction_ids
match_dict = {"path8" : "[M]_RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p",
           "path8-3":"[M]_RXN_961_p",
           "path119":"[M]_GPH_RXN_p",
           "path95":"[M]_RXN_969_x",
           "path96":"[M]_GLYCINE_AMINOTRANSFERASE_RXN_x",
           "path182":"[M]_SERINE_GLYOXYLATE_AMINOTRANSFERASE_RXN_x",
           "path83":"[M]_SERINE_GLYOXYLATE_AMINOTRANSFERASE_RXN_x",
           "path100":"[M]_GLYOHMETRANS_RXN_m",
           "path100-8":"[M]_GCVMULTI_RXN_m",
           "path81":"[M]_HYDROXYPYRUVATE_REDUCTASE_RXN_NAD_x",
           "path71":"[M]_GLY3KIN_RXN_p",
           "path121":"[M]_RXN0_5224_c",
           "path122":"[M]_PEPCARBOX_RXN_c",
           "path123":"[M]_ASPAMINOTRANS_RXN_c",
           "path153-4":"[B]_ASPAMINOTRANS_RXN_c",
           "path154":"[B]_PEPCARBOXYKIN_RXN_c",
           "path155":"[B]_PEPCARBOXYKIN_RXN_c",
           "path7":"[M]_MALATE_DEH_RXN_c",
           "path204-0":"[M]_MALATE_DEH_RXN_p",
           "path204":"[M]_MALATE_DEHYDROGENASE_NADP_RXN_p",
           "path157":"[B]_1_PERIOD_1_PERIOD_1_PERIOD_39_RXN_m",
           "path158":"[B]_1_PERIOD_1_PERIOD_1_PERIOD_39_RXN_m",
           "path160":"[B]_ALANINE_AMINOTRANSFERASE_RXN_c",
           "path124":"[M]_ALANINE_AMINOTRANSFERASE_RXN_c",
           "path126":"[M]_PYRUVATEORTHOPHOSPHATE_DIKINASE_RXN_p",
           "path39":"[B]_RIBULOSE_BISPHOSPHATE_CARBOXYLASE_RXN_p",
           "path170":"[B]_MALIC_NADP_RXN_p",
           "path171":"[B]_MALIC_NADP_RXN_p",
           "path125":"[M]_Pyr_H_pc",
           "path177":"[B]_ASPAMINOTRANS_RXN_m",
           "path177-3":"[B]_MALATE_DEH_RXN_m",
           "path184":"[B]_GLYOHMETRANS_RXN_m",
           "path183":"[B]_GCVMULTI_RXN_m",
           "path186":"[B]_SERINE_GLYOXYLATE_AMINOTRANSFERASE_RXN_x",
           "path187":"[B]_HYDROXYPYRUVATE_REDUCTASE_RXN_NAD_x",
           "path120":"[M]_CO2_tx",
           "path213-8":"[M]_CO2_pc",
           "path13": "[M]_GLYCERATE_GLYCOLLATE_pc",
           "path13-7":"[M]_GLYCERATE_GLYCOLLATE_pc",
           "path30":"[M]_OAA_MAL_pc",
           "path30-19":"[M]_OAA_MAL_pc",
           "path3":"[M]_GLYCOLLATE_pc",
           "path53":"[M]_Glycerate_xc",
           "path53-9":"[M]_Glycolate_xc",
           "path4":"[MB]_MAL_c",
           "path161":"[MB]_L_ALPHA_ALANINE_c",
           "path197":"[MB]_GLYCERATE_c",
           "path189":"[MB]_GLY_c",
           "path173":"[MB]_PYRUVATE_c",
           "path162":"[MB]_PHOSPHO_ENOL_PYRUVATE_c",
           "path153":"[MB]_L_ASPARTATE_c",
           "path11":"[B]_CO2_mc",
           "path15":"[B]_CO2_pc",
           "path16":"[B]_SER_mc",
           "path17":"[B]_SER_xc",
           "path18":"[B]_Glycerate_xc",
           "path19":"[B]_GLY_mc",
           "path22":"[B]_PYRUVATE_PROTON_mc",
           "path24":"[M]_PPT_pc",
           "path25":"[M]_GLYCERATE_GLYCOLLATE_pc",
           "path29":"[M]_SER_mc",
           "path31":"[M]_SER_xc",
           "path26":"[M]_GLY_xc",
           "path27":"[M]_GLY_mc",
           "path32":"[M]_CO2_mc",
           }


#create a data frame with our dictionary making the columns path and reaction id
fluxdata_match_df = pd.DataFrame(match_dict.items(), columns=["path", "reaction_id"])

#print(fluxdata_match_df)

path_fluxes = []

#for every key value (paths) if value of key is in [Bundlesheath] 
#add a column (fluxes) to empty list path_fluxes and add fluxdata from the 
#dataframe fluxdata_df matching with the dict_values into the created column
#if not in the bundlesheath divide the flux data by the volume ratio to normalise it
    

for i in range(len(list(match_dict.keys()))):
    if "[M]" in list(match_dict.values())[i] or "[MB]" in list(match_dict.values())[i]:
        path_fluxes.append(fluxdata_df.loc[list(match_dict.values())[i] ,"fluxes"])
    else:
        path_fluxes.append(fluxdata_df.loc[list(match_dict.values())[i] ,"fluxes"]*0.8 )

#print(path_fluxes)
#replace values that are -1e-5 <= i <= 1e-5 with 0

threshold = 1e-5

for i in range(len(path_fluxes)):
    if -threshold <= path_fluxes[i] <= threshold:
        # Replace the number within the specified range
        path_fluxes[i] = 0  


#define direction giving function
def eval_sign(i):
    if i >= 0:
        return 1
    else:
        return -1
    
#run through function and assign 1 and -1 to the path fluxes    
direction = [eval_sign(i) for i in path_fluxes]  

#print(path_fluxes)

#increasing values of series, perfrming a min max normalisation

#convert list into series
path_fluxes_series = abs(pd.Series(list(path_fluxes)))
#print(path_fluxes_series[48])

# Example Series
series = path_fluxes_series

# Convert the Series to a DataFrame with a single column
df = pd.DataFrame({'Column1': series})

# Save the original index
original_index = df.index

# Create a MinMaxScaler
scaler = MinMaxScaler()

# Fit and transform the values
scaled_values = scaler.fit_transform(df)

# Create a new DataFrame with scaled values and the original index
df_scaled = pd.DataFrame(scaled_values, columns=['Column1'], index=original_index)

# Specify the factor by which you want to increase the values
increase_factor = 10000

# Scale the values by the increase factor
df_scaled *= increase_factor

# Denormalize the scaled values back to the original range
df_increased = pd.DataFrame(scaler.inverse_transform(df_scaled), columns=['Column1'], index=original_index)

# Extract the increased values as a Series
path_fluxes_series_increased = df_increased['Column1']

#print("Original Series:")
#print(series)
#print("\nSeries with Increased Values while Maintaining Ratio:")
#print(path_fluxes_series_increased)

#######################################

#min max normalisation with increased fluxes
norm_path_fluxes_minmax = (path_fluxes_series_increased-path_fluxes_series_increased.min())/(path_fluxes_series_increased.max()-path_fluxes_series_increased.min())
#print(norm_path_fluxes_minmax[48])

#create a dataframe with reaction_id fluxdata and path and save to excel

#print(fluxdata_match_df)

flux_df = fluxdata_match_df.assign(flux = path_fluxes_series_increased, direction = direction, norm_fluxes = norm_path_fluxes_minmax)
#print(flux_df)
flux_df.to_excel(r'./Excel_files/Flux_C3_C4.xlsx', index=False)
#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #print(flux_df)
 

#get lowest value and highest value in df
selected_column = 'flux'

# Get the lowest value in the specified column

lowest_value_column = flux_df[selected_column].min()

#get lowest value which is not 0

#lowest_non_zero_value = flux_df[flux_df[selected_column] != 0][selected_column].min()

#print(f"Lowest non-zero value in {selected_column}: {lowest_non_zero_value}")
# Get the highest value in the specified column

highest_value_column = flux_df[selected_column].max()

#print(f"Lowest value in {selected_column}: {lowest_value_column}")
#print(f"Highest value in {selected_column}: {highest_value_column}")

#set data_min and data_max

data_max = highest_value_column
data_min = lowest_value_column


#generate omc cmap

from omccolors import omccolors

cmap = "rainbow"

(colormap, min_exp, max_exp) = omccolors.generate_omc(data_min, data_max, cmap)

#creating colorbar

def b_g(cmap=colormap, low=0, high=0, dataframe = flux_df):
    a = pd.Series(list(dataframe["norm_fluxes"]))
    rng = a.max() - a.min()
    norm = colors.Normalize(a.min() - (rng * low),
                        a.max() + (rng * high))
    normed = norm(a.values)
    c = [colors.rgb2hex(x) for x in plt.cm.get_cmap(cmap)(normed)]

    ###- Trying to get that sweet colorbar
    fig, ax = plt.subplots(figsize=(.5, 6))
    fig.subplots_adjust(bottom=0.5)

    cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                norm=norm,
                                orientation='vertical')
    cb1.set_label('Flux Values')
    fig.savefig("./SVG_files/OMC_Colorbar_C3_C4.svg", format='svg', bbox_inches = 'tight')

    grad = [color for color in c]
    return grad


#run function to create color gradiant figure
flux_df["colors"] = b_g(dataframe=flux_df)

#SQ normalisation
#print(list(path_fluxes_series_increased))
#print(path_fluxes)
path_fluxes = list(path_fluxes)
norm_path_fluxes = [(0.5 + 0.2 * math.sqrt(abs(i))) * 0.5 for i in path_fluxes]
#print(norm_path_fluxes)

#create dataframe for visualisation
flux_df = flux_df.assign(SQ_flux_values = norm_path_fluxes)
#flux_df.to_excel(r'C:/Users/stani/OneDrive/Dokumente/Uni stuff/Etagen praktikum/Python/Flux_path_excel/flux_path_SQ.xlsx', index=False)

#with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
 #   print(match_df)
    
    
#Parse the skeleton model SVG file
def parser(filename = "./SVG_files/Skeleton_model_finished_template.svg", path = "path33", fill = "#ff0000", width = 1, direction = 1):
    tree = etree.parse(open(filename, 'r'))
    if direction == 1:
        for element in tree.iter():
            if element.tag.split("}")[1] == "path":
                if element.get("id") == path:
                    element.set("style", f"clip-rule:evenodd;fill:none;fill-rule:evenodd;stroke:{fill};stroke-width:{round(width,2)};stroke-linecap: butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray: none;stroke-opacity:1;image-rendering:optimizeQuality;shape-rendering:geometricPrecision;text-rendering:geometricPrecision;marker-end:url(#marker67);")
            else:
                pass
    else:
        for element in tree.iter():
            if element.tag.split("}")[1] == "path":
                if element.get("id") == path:
                    element.set("style", f"clip-rule:evenodd;fill:none;fill-rule:evenodd;stroke:{fill};stroke-width:{round(width,2)};stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1;image-rendering:optimizeQuality;shape-rendering:geometricPrecision;text-rendering:geometricPrecision;marker-start:url(#marker67);")
            else:
                pass

    tree.write(filename)

#Map Flux Data to the SVG file
for i in range(len(flux_df["norm_fluxes"])):
    parser(path = list(flux_df["path"])[i], fill = list(flux_df["colors"])[i], width= list(flux_df["SQ_flux_values"])[i], direction = list(flux_df["direction"])[i])


