import json
import pandas
import csv
import sys, os

class CSVtoJson:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
    
    # Read file CSV and  to json type 
    def convertCSVtoJson(self):
        df = pandas.read_csv(self.input_file)
        jsonStr = ""
        cols = list(df)
        for index, row in df.iterrows():
            id = str(row[0]).rsplit('-', 1)[-1]
            id = id.split('.')[0]
            jsonStr += "{\"create\": { \"_id\": " + id + "}\n"
            jsonStr += "{"
            for col in cols:
                if(isinstance(row[col], str)):
                    jsonStr += "\"" + col + "\": \"" + str(row[col]).replace("\"", "\\\"") + "\","
                else:
                    jsonStr += "\"" + col + "\": " + str(row[col]).replace("\"", "\\\"") + ","
                
            # remove last comma in jsonStr
            jsonStr = jsonStr[:-1]
            jsonStr += "}\n"
        return jsonStr
    
    # Write json data to file .json
    def writeToFileJson(self, jsonStr):
        directory = os.path.join(os.path.dirname(__file__), '../json_file2/')
        with open(os.path.join(directory, self.output_file), "w") as text_file:
            text_file.write(jsonStr)

# convert CSV file to Json File
# command: python xlsxToJson.py input_file.xls output_file.json
if __name__ == "__main__":
    m = CSVtoJson(sys.argv[1], sys.argv[2])
    data_file = m.convertCSVtoJson()
    m.writeToFileJson(data_file)