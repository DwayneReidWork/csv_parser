def importCSV(filename, delimiter=','):
    with open(filename, 'r') as file:
        dataframe={}
        # Read the header line, split by delimiter
        headers = file.readline().replace("\n", '').split(delimiter)
        for line in file:
            # Parse each individual line
            linedata = line.replace("\n", '').split(delimiter)
            row = {}
            # Sync row data to header category
            # If theres a category but no matching data in the row insert 'null'
            for i in range(len(headers)):
                if i in range(len(linedata)):
                    row[headers[i]] = linedata[i]
                else:
                    row[headers[i]] = "null"    
            dataframe[linedata[0]] = [row]
        file.close()
        return dataframe


data = importCSV('data.csv')
for x in data:
    print(data[x])
