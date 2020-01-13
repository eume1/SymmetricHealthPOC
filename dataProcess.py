import xml.etree.ElementTree as et
import pandas as pd
from datetime import date
import datetime
import zipfile
import requests
import os
import json
from pandas import ExcelWriter
#from fuzzywuzzy import fuzz
import re


now = datetime.datetime.now()
today = str(date.today()).replace('-','')
#today_zip = today + '.zip'
gudidZip = 'gudidZip.zip'

#gudid_url = 'https://accessgudid.nlm.nih.gov/release_files/download/gudid_daily_update_' + today_zip
gudid_url = 'https://accessgudid.nlm.nih.gov/release_files/download/gudid_full_release_20200101.zip'


#Gudid Extraction

req = requests.get(gudid_url)
file = open(gudidZip, 'wb')
for chunk in req.iter_content(100000):
    file.write(chunk)
file.close()


with zipfile.ZipFile(gudidZip) as zf:
    zf.extractall(gudidZip.split('.')[0])


gudid_items = []

def append(x):
    try:
        gudid_items.append([x[11].text,x[10].text,x[15].text])
    except (IndexError, AttributeError, ValueError):
        return None


def appendto_df(gudidPath):
	tree = et.parse(gudidPath)
	allNodes = tree.getroot()

	for node in allNodes:
		append(node)


wd = str(os.getcwd()) + "\\" + gudidZip.split('.')[0]
count = 0
counter = 0


for subdir, dirs, files in os.walk(wd):
    for filename in files:
        filepath = subdir + os.sep + filename

        if filepath.endswith(".xml"):
            appendto_df(filepath)
            counter += 1

# re.sub(r'\W+', '', str_ )

def processstring(str):
	return re.sub(r'\W+', '', str).lower()
	

gudid_items_df = pd.DataFrame(gudid_items, columns = ['catalogNumber', 'versionModelNumber', 'deviceDescription']).astype(str)

#Basic processing to eliminate non alphanumerals and standardize lock
gudid_items_df['catalogNumber'] = gudid_items_df['catalogNumber']
gudid_items_df['versionModelNumber'] = gudid_items_df['versionModelNumber']


gudid_items_df.to_csv('gudid.csv')

#Mdall data
active_device_identifier_url = ['active_device_identifier' ,'active_device_identifier.json', 'https://health-products.canada.ca/api/medical-devices/deviceidentifier/?state=active&type=json']
active_license_url = ['active_license' ,'active_license.json','https://health-products.canada.ca/api/medical-devices/licence/?state=active&type=json&lang=en']
company_url = ['company', 'company.json','https://health-products.canada.ca/api/medical-devices/company/?type=json']

company_df = pd.read_json(company_url[2], orient='columns').drop_duplicates().astype(str)
active_license_df = pd.read_json(active_license_url[2], orient='columns').drop_duplicates().astype(str)
active_device_identifier_df = pd.read_json(active_device_identifier_url[2], orient='columns').drop_duplicates().astype(str)


dfs = [ [company_df,'company.csv'], [active_license_df, 'active_license.csv'], [active_device_identifier_df, 'active_device_identifier.csv'] ]

count = 0
while count < len(dfs):
    dfs[count][0].to_csv(dfs[count][1])
    count += 1  # This is the same as count = count + 1
	

licence_version_join = pd.merge(gudid_items_df, active_device_identifier_df, left_on='versionModelNumber', right_on='device_identifier', how='inner').astype(str)
catalog_version_join = pd.merge(gudid_items_df, active_device_identifier_df, left_on='catalogNumber', right_on='device_identifier', how='inner').astype(str)

licence_catalog_join = pd.concat([licence_version_join, catalog_version_join], ignore_index=True).drop_duplicates().astype(str)


licence_catalog_join_with_licence = pd.merge(licence_catalog_join, active_license_df, left_on='device_identifier', right_on='original_licence_no', how='left')

#licence_catalog_with_licence_and_company = pd.merge(licence_catalog_join_with_licence, company_df, left_on='company_id', right_on='company_id', how='outer')
licence_catalog_with_licence_and_company = licence_catalog_join_with_licence.merge(company_df, 'outer')

licence_catalog_with_licence_and_company.drop_duplicates().to_json('aligned.json', orient='records')
licence_catalog_with_licence_and_company.drop_duplicates().to_csv('aligned.csv', orient='records')

print('There are ' + str(licence_catalog_join.shape[0]) + ' matched devices in in both GUDID & MDALL')
print('There are ' + str(active_device_identifier_df.shape[0] - licence_catalog_join.shape[0]) + ' in MDALL ONLY')
print('There are ' + str(gudid_items_df.shape[0] - licence_catalog_join.shape[0]) + ' in GUDID ONLY')
