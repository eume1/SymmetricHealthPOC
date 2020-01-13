# SymmetricHealthPOC

To run:
Step 1: git clone https://github.com/eume1/SymmetricHealthPOC.git


Step 2: cd SymmetricHealthPOC/process


Step 3: python dataProcess.py


Step 3 will pull down the various code bases from the web and perform joins. It will also emit CSV & JSONs of processed data. Once Step 3 is complete, you can now query the data. To query based on catalog number, run:

python dataRetrival.py catalog_no {catalog_number}


e.x.
python dataRetrival.py catalog_no 1710

python dataRetrival.py catalog_no {catalog_number}


e.x.
To query based on version number, run:

python dataRetrival.py version_no {version_no}

python dataRetrival.py version_no 999-028-999
