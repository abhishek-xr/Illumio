# Illumio
> Designed to process network flow logs and tag each log entry based on predefined port and protocol mappings.
> The program reads log files and a lookup table in plain text (ASCII) format.
> Outputs the tagged log entries along with summary files that count the occurrences of each tag and port/protocol combination.

# Assumptions made for the program:
The program only supports the default log format, specifically formatted to follow the AWS Flow Log Record format as outlined below and only supports Version 2: 
``` [Version, AccountID, InterfaceID, SrcAddr, DstAddr, SrcPort, DstPort, Protocol, Packets, Bytes,StartTime, EndTime, Action, LogStatus, Tag] ```

* We are converting the plain txt files to a new output.csv lookup table to match ports/protocols to the tag for ease of use in the program *

# Requirements met:
The program is optimized to handle log files up to 10 MB in size.
The lookup table can contain up to 10,000 mappings.
Protocol names in the lookup table and logs are case-insensitive. The program automatically converts protocol names to lowercase during processing
Multiple tags can be mapped to the same port and protocol combination.
  
# Installation & Execution:
1. Make sure you have Python 3.x installed on your machine.
2. Clone this repo to your machine.
3. Run the following command within src :
		``` python log_tagger.py ```
	This should generate 3 output files:
		output.csv : Contains the tagged log entries
		output_tag_counts.csv : Contains the count of each tag 
		out_port_protocol_counts.csv : Contains the count for each port/protocol combination in dstport

# Running Tests
1. Navigate to the tests directory
    ``` cd ../tests ```
2. Run the following command : 
	``` python test_log_tagger.py ```
>The current test cases are:
    	Verifying that an empty lookup table is returned if the lookup file is not found
    	Ensures that the program raises a FileNotFoundError if the log file does not exist.
    	Validates that the program correctly processes a valid log file and generates output with the correct number of lines

# Cleanup (just in case)
Run this command in case you wish to clean up the generated output files: 
   ``` rm output.csv output_tag_counts.csv output_port_protocol_counts.csv ```
