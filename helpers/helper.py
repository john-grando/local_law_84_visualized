#!/home/grandocu/anaconda3/envs/cpy3/bin
# -*- coding: utf-8 -*-

"""
DATA 608
Final Project
John Grando
functions used to clean and manage data
"""

import os
import pandas as pd
import numpy as np
from pyproj import Proj, transform

def load_pluto(clean_data = None):
    '''
    This function cleans, arranges, and loads data from pluto.  A .csv file is created
    so the user doesn't have to perform the first few steps every time this function
    is called.
    '''
    if not os.path.isfile('Data/pluto_df.csv') or clean_data == True:
        # Processs pluto data
        bk = pd.read_csv('Data/PLUTO17v1.1/BK2017V11.csv')
        bx = pd.read_csv('Data/PLUTO17v1.1/BX2017V11.csv')
        mn = pd.read_csv('Data/PLUTO17v1.1/MN2017V11.csv')
        qn = pd.read_csv('Data/PLUTO17v1.1/QN2017V11.csv')
        si = pd.read_csv('Data/PLUTO17v1.1/SI2017V11.csv')
        ny = pd.concat([bk, bx, mn, qn, si], ignore_index=True)
        
        ## Getting rid of some outliers
        ny = ny[(ny['YearBuilt'] > 1850) & (ny['YearBuilt'] < 2020) & (ny['NumFloors'] != 0)]
        wgs84 = Proj("+proj=longlat +ellps=GRS80 +datum=NAD83 +no_defs")
        nyli = Proj("+proj=lcc +lat_1=40.66666666666666 +lat_2=41.03333333333333 +lat_0=40.16666666666666 +lon_0=-74 +x_0=300000 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs")
        ny['XCoord'] = 0.3048*ny['XCoord']
        ny['YCoord'] = 0.3048*ny['YCoord']
        ny['lon'], ny['lat'] = transform(nyli, wgs84, ny['XCoord'].values, ny['YCoord'].values)
        ny = ny[(ny['lon'] < -60) & (ny['lon'] > -100) & (ny['lat'] < 60) & (ny['lat'] > 20)]
        #return subset of interes and save to csv file for later use
        ny[['BBL', 'Address', 'lon', 'lat']].to_csv("Data/pluto_df.csv", index=False)
    return pd.read_csv("Data/pluto_df.csv")

def load_ll84_2017(clean_data = None):
    '''
    Clean up and select pertinent data from the ll84 file
    '''
    if not os.path.isfile('Data/ll84_2017_df.csv') or clean_data == True:
        df = pd.read_excel('Data/ll84/excel_proc/2017_ll84.xlsx', sheet_name=0)
        df = df[np.isfinite(pd.to_numeric(df["BBL - 10 digits"], errors='coerce'))]
        df["year"] = 2017
        df = pd.concat([pd.to_numeric(df.loc[:,"BBL - 10 digits"]).astype(int), 
                        df.loc[:,"Parent Property Id"], 
                        pd.to_numeric(df.loc[:,"DOF Gross Floor Area"], errors='coerce'), 
                        df.loc[:,"Largest Property Use Type"],  
                        pd.to_numeric(df.loc[:,"Year Built"]), 
                        df.loc[:,"Metered Areas (Energy)"], 
                        df.loc[:,"Metered Areas  (Water)"], 
                        pd.to_numeric(df.iloc[:,28], errors='coerce'), 
                        pd.to_numeric(df.iloc[:,38], errors = 'coerce'),
                        pd.to_numeric(df.iloc[:,39], errors='coerce'), 
                        pd.to_numeric(df.iloc[:,41], errors='coerce'), 
                        pd.to_numeric(df.iloc[:,43], errors= 'coerce'),
                        pd.to_numeric(df.iloc[:,44], errors= 'coerce'),
                        pd.to_numeric(df.iloc[:,45], errors= 'coerce'),
                        pd.to_numeric(df.iloc[:,47], errors= 'coerce'),
                        pd.to_numeric(df.iloc[:,48], errors= 'coerce'),
                        df.loc[:,"year"], 
                        df.loc[:,"Occupancy"], 
                        pd.to_numeric(df.loc[:,"Street Number"], errors='coerce').fillna(0).astype(int), 
                        df.loc[:,"Street Name"]], 
        axis=1).replace("(Not Available.*|Not Applicable.*)", np.nan, regex = True)
        df.columns = ["bbl", "parent_property_id", "gross_floor_area", "first_area_type", "year_built", "metered_area_energy", "metered_area_water", "eui_kbtu_sf", "steam_kbtu", "natural_gas_kbtu", "electricity_kbtu", "total_ghg_mmco2e", "direct_ghg_mmco2e", "indirect_ghg_mmco2e", "water_kgal", "wui_gal_sf", "year", "occupancy", "street_number", "street_name"]
        df.to_csv('Data/ll84_2017_df.csv', index=False)
    return pd.read_csv('Data/ll84_2017_df.csv')

def load_ll84_2016(clean_data = None):
    '''
    Clean up and select pertinent data from the ll84 file
    '''
    if not os.path.isfile('Data/ll84_2016_df.csv') or clean_data == True:
        df = pd.read_excel('Data/ll84/excel_proc/2016_ll84.xlsx', sheet_name=0)
        df = df[np.isfinite(pd.to_numeric(df["NYC Borough, Block and Lot (BBL)"], errors='coerce'))]
        df["year"] = 2016
        df = pd.concat([pd.to_numeric(df.loc[:,"NYC Borough, Block and Lot (BBL)"]).astype(int), 
                        df.loc[:,"Parent Property Id"], 
                        pd.to_numeric(df.iloc[:,49], errors='coerce'), 
                        df.loc[:,"Largest Property Use Type"], 
                        pd.to_numeric(df.loc[:, "Year Built"], errors='coerce'), 
                        df.loc[:, "Metered Areas (Energy)"], 
                        df.loc[:,"Metered Areas  (Water)"], 
                        pd.to_numeric(df.iloc[:,28], errors='coerce'), 
                        pd.to_numeric(df.loc[:, "District Steam Use (kBtu)"], errors='coerce'), 
                        pd.to_numeric(df.loc[:, "Natural Gas Use (kBtu)"], errors='coerce'), 
                        pd.to_numeric(df.iloc[:,44], errors = 'coerce'),
                        pd.to_numeric(df.iloc[:,46], errors = 'coerce'),
                        pd.to_numeric(df.iloc[:,47], errors = 'coerce'),
                        pd.to_numeric(df.iloc[:,48], errors = 'coerce'),
                        pd.to_numeric(df.iloc[:,51], errors = 'coerce'),
                        pd.to_numeric(df.iloc[:,52], errors = 'coerce'),
                        df.loc[:,"year"], 
                        df.loc[:,"Occupancy"], 
                        pd.to_numeric(df.loc[:,"Street Number"], errors='coerce').fillna(0).astype(int), 
                        df.loc[:,"Street Name"]], 
        axis=1).replace("(Not Available.*|Not Applicable.*)", np.nan, regex = True)
        df.columns = ["bbl", "parent_property_id", "gross_floor_area", "first_area_type", "year_built", "metered_area_energy", "metered_area_water", "eui_kbtu_sf", "steam_kbtu", "natural_gas_kbtu", "electricity_kbtu", "total_ghg_mmco2e", "direct_ghg_mmco2e", "indirect_ghg_mmco2e", "water_kgal", "wui_gal_sf", "year", "occupancy", "street_number", "street_name"]
        df.to_csv('Data/ll84_2016_df.csv', index=False)
    return pd.read_csv('Data/ll84_2016_df.csv')

def load_ll84_2015(clean_data = None):
    '''
    Clean up and select pertinent data from the ll84 file
    Note, multiple columns are not available in this set.  Might not be worth using.
    '''
    if not os.path.isfile('Data/ll84_2015_df.csv') or clean_data == True:
        df = pd.read_excel('Data/ll84/excel_proc/2015_ll84.xlsx', sheet_name=0)
        df = df[np.isfinite(df["NYC Borough, Block, and Lot (BBL)"])]
        df["NYC Borough, Block, and Lot (BBL)"] =  df["NYC Borough, Block, and Lot (BBL)"].astype(int).apply(str)
        df["year"] = 2015
        df["Occupancy"] = np.nan
        df["parent_property_id"] = np.nan
        df["second_area_type"] = np.nan
        df["third_area_type"] = np.nan
        df["year_built"] = np.nan
        dff = df[(df["NYC Borough, Block, and Lot (BBL)"].str.len() == 10) & (pd.to_numeric(df["NYC Borough, Block, and Lot (BBL)"], errors='coerce') != np.nan)]
        dff_clean = pd.concat([dff.loc[:, "NYC Borough, Block, and Lot (BBL)"], dff.loc[:,"parent_property_id"], dff.iloc[:,23], dff.iloc[:,24], dff.loc[:,"second_area_type"], dff.loc[:,"third_area_type"], dff.loc[:,"year_built"]], axis=1).replace("(Not Available.*|Not Applicable.*)", np.nan, regex = True)
        print(dff_clean)
    return

def clean_df(df = None):
    if df is not None:
        df["bbl"] =  df["bbl"].astype(int).apply(str)
        print(df.dtypes)
        dff = df[(df["bbl"].str.len() == 10) & (pd.to_numeric(df["bbl"], errors='coerce') != np.nan) & (df["occupancy"] == 100) & (df["metered_area_energy"] == "Whole Building") & (pd.to_numeric(df["year_built"], errors='coerce').fillna(0) > 1850) & (pd.to_numeric(df["year_built"], errors = 'coerce').fillna(0) < 2018) ].copy()
        dff.loc[df["gross_floor_area"] < 0, "gross_floor_area"] = np.nan
        dff.loc[df["eui_kbtu_sf"] < 0, "eui_kbtu_sf"] = np.nan
        dff.loc[df["natural_gas_kbtu"] < 0, "natural_gas_kbtu"] = np.nan
        dff.loc[df["electricity_kbtu"] < 0, "electricity_kbtu"] = np.nan
        dff.loc[df["total_ghg_mmco2e"] < 0, "total_ghg_mmco2e"] = np.nan
        dff.loc[df["indirect_ghg_mmco2e"] < 0, "indirect_ghg_mmco2e"] = np.nan
        dff.loc[df["direct_ghg_mmco2e"] < 0, "direct_ghg_mmco2e"] = np.nan
        dff.loc[df["water_kgal"] < 0, "water_kgal"] = np.nan
        dff.loc[df["wui_gal_sf"] < 0, "wui_gal_sf"] = np.nan
        dff.loc[df["steam_kbtu"] < 0, "steam_kbtu"] = np.nan
        area_type_list = df[["bbl","first_area_type"]].groupby(["first_area_type"]).count().reset_index().sort_values(by=["bbl"], ascending=False)["first_area_type"].tolist()[:15]
        print(area_type_list)
        dff.loc[~df["first_area_type"].isin(area_type_list), "first_area_type"] = "other"
        dff["steam_kbtu_sf"] = dff["steam_kbtu"] / dff["gross_floor_area"]
        dff["natural_gas_kbtu_sf"] = dff["natural_gas_kbtu"] / dff["gross_floor_area"]
        dff["electricity_kbtu_sf"] = dff["electricity_kbtu"] / dff["gross_floor_area"]
        dff["total_ghg_mmco2e_sf"] = dff["total_ghg_mmco2e"] / dff["gross_floor_area"]
        dff["direct_ghg_mmco2e_sf"] = dff["direct_ghg_mmco2e"] / dff["gross_floor_area"]
        dff["indirect_ghg_mmco2e_sf"] = dff["indirect_ghg_mmco2e"] / dff["gross_floor_area"]
    else:
        dff = None
    return dff

def geo_df(df = None):
    if df is not None:
        dff = df[["bbl", "street_number", "street_name", "first_area_type", "lon", "lat", "year", "eui_kbtu_sf", "steam_kbtu_sf", "natural_gas_kbtu_sf", "electricity_kbtu_sf", "total_ghg_mmco2e_sf", "direct_ghg_mmco2e_sf", "indirect_ghg_mmco2e_sf"]]
        dff = pd.melt(dff, id_vars = ["bbl", "street_number", "street_name", "first_area_type", "lon", "lat", "year"], var_name="metered_type", value_name="value").sort_values(["value"])
        dff = dff[(dff["value"] > 0) & (np.isfinite(dff["value"]))]
    else:
        dff = None
    dff.to_csv('Data/csv/ll84_geo_df.csv', index=False)
    return dff

def plot_df(df = None):
    if df is not None:
        dff = df[["bbl", "street_number", "street_name", "first_area_type", "year", "year_built", "gross_floor_area", "eui_kbtu_sf", "steam_kbtu_sf", "natural_gas_kbtu_sf", "electricity_kbtu_sf", "total_ghg_mmco2e_sf", "direct_ghg_mmco2e_sf", "indirect_ghg_mmco2e_sf"]]
        dff = dff[((dff["eui_kbtu_sf"] > 0) | (dff["steam_kbtu_sf"] > 0) | (dff["natural_gas_kbtu_sf"] > 0) | (dff["electricity_kbtu_sf"] > 0)  | (dff["total_ghg_mmco2e_sf"] > 0) | (dff["direct_ghg_mmco2e_sf"] > 0) | (dff["indirect_ghg_mmco2e_sf"] > 0)) &   
                  (np.isfinite(dff["eui_kbtu_sf"])) | (np.isfinite(dff["steam_kbtu_sf"])) | (np.isfinite(dff["natural_gas_kbtu_sf"])) | (np.isfinite(dff["electricity_kbtu_sf"])) | (np.isfinite(dff["total_ghg_mmco2e_sf"])) | (np.isfinite(dff["direct_ghg_mmco2e_sf"])) | (np.isfinite(dff["indirect_ghg_mmco2e_sf"]))]
    else:
        dff = None
    dff.to_csv('Data/csv/ll84_plot_df.csv', index=False)
    return dff

def build_dfs(clean_pluto = False, clean_ll84 = False):
    pluto_df = load_pluto(clean_data = clean_pluto)
    ll84_2016_df = load_ll84_2016(clean_data = clean_ll84)
    ll84_2017_df = load_ll84_2017(clean_data = clean_ll84)
    ll84_df = ll84_2017_df.append(ll84_2016_df, ignore_index = True)
    ll84_df = pd.merge(ll84_df, pluto_df, left_on = "bbl", right_on = "BBL", how = "inner")
    ll84_df = clean_df(ll84_df)
    ll84_df.to_csv('Data/csv/ll84_df.csv', index=False)
    geo_df(ll84_df)
    plot_df(ll84_df)
    return ll84_df

if __name__ == '__main__':
    build_dfs(False, True)