import pandas as pd
import os
import json
import sys


description = ''
licenseName = ''

path_to_json = str(os.getcwd()) + "\\" + 'licence_catalog_with_licence_and_company.json'
data_df = pd.read_json(path_to_json).drop_duplicates()

if (sys.argv[1] == 'catalog_no'):
	output = data_df.loc[ (data_df['catalogNumber'] == sys.argv[2]) ]
	description = output['deviceDescription'].head(1)
	licenseName = output['licence_name'].head(1)
elif (sys.argv[1] == 'version_no'):
	output = data_df.loc[(data_df['versionModelNumber'] == sys.argv[2])]
	description = output['deviceDescription'].head(1)
	licenseName = output['licence_name'].head(1)


print('Catalog #: ' + sys.argv[2])
print('')
print('Gudid Description: ' + str(description).replace('Name: deviceDescription, dtype: object',''))
print('MDALL Description: ' + str(licenseName).replace('Name: licence_name, dtype: object','') )


