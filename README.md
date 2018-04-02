A10-PoC-Automation

This script accompanies the A10 Proof of Concept Test Plan. The script will will input from the data from the A10_PoC_Data.xlsm spreasheet to generate an inital configuration for the A10 ADC running v4.x code. 

The configuration is meant to be a starting point for evaluating the A10 ADC load-balancing feature.

To generate the configuration, complete all sheets in the excel workbook. Each column for the variables has a comment to provide an example and summary of the data required. The PoC test plan also provides detailed information for each data requirement. 

Usage:

1. Ensure the A10_PoC_Data.xlsm (or A10_PoC_Data.xls) are completed with all rows updated.
2. Run the configuration generator script by running: python3 ACOS_PoC.py
   (Note: configuration will be written to the console windows, just echo output to file if preferred.)
   
