# Energy calculator
The purpose of this tool is to analyse a CAN trace in format asammdf and extract the info of the extracted energy of a BEV vehicle during a drive cycle
# Usage
python energy_extracted_calculator.py <inputFile>.mf4
The trace must be mdf format
-. Options:  --output <filename>.xlsx -> extracts a report containing the data from the trace
             --search <key>           -> returns a list of signal names that contain the key 
             --start  <startTime>     -> choose a timestamp to start the calculation from
             --stop   <stopTime>      -> choose a timestamp to stop che calculation to
             -p or --plot             -> plots the outcome