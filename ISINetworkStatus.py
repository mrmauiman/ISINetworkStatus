import json
import requests
import csv

# If this variable is not None then it is the url of a json request
url = None
# This is the local json file path
json_file_path = "data.json"

# This variable will hold the json data
data = None
# This variable will hold the min and max for every switch and port
tracker = {}

# Create the CSV file
csv_file = open("output.csv", 'w', newline='')
csv_writer = csv.writer(csv_file)
# Create headers for csv
csv_writer.writerow(["Switch", "Port", "Value", "Min", "Max"])

# Get the json
if url != None:
    # Get json from web address
    response = requests.get(url)
    data = json.loads(response.text)
else:
    # Get json from test file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

# Loop through totalCount amount of times
for i in range(int(data["totalCount"])):
    curr_obj = data["imdata"][i]
    # curr_obj is the current switch and port reading
    attributes = curr_obj["ethpmDOMCurrentStats"]["attributes"]
    # attributes is the current attributes

    dn = attributes["dn"]
    # dn contains the switch and port

    value = attributes["value"]
    # value contains the current value

    # Extract the switch and port
    switch = dn[dn.find("node"):dn.find("/sys")]
    port = dn[dn.find("[")+1: dn.find("]")]

    # Set the max and min
    if switch not in tracker:
        tracker[switch] = {}
        tracker[switch][port] = {}
        tracker[switch][port]["max"] = value
        tracker[switch][port]["min"] = value

    elif port not in tracker[switch]:
        tracker[switch][port] = {}
        tracker[switch][port]["max"] = value
        tracker[switch][port]["min"] = value

    else:
        tracker[switch][port]["max"] = max(tracker[switch][port]["max"], value)
        tracker[switch][port]["min"] = min(tracker[switch][port]["min"], value)

    # Output
    # Output to command line
    print("S:", switch, "P:", port, "Value:", value, "Min:", tracker[switch][port]["min"], "Max:", tracker[switch][port]["max"])
    # Output to CSV
    csv_writer.writerow([switch, port, value, tracker[switch][port]["min"], tracker[switch][port]["max"]])

# Close the csv file
csv_file.close()    
