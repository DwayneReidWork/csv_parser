def main():
    while True:
        user_input = input("\nPlease make a selection.\n1. View CSV Contents\n2. Search for user by ID.\n3. Add row to file.\n4. Update row.\n5. Delete Row.\n\nType 'exit' to quit.\n\n")

        if user_input.lower() == 'exit':
            break
        if not user_input.isdigit():
            print("Invalid input. Please enter a number.")
            continue
        option = int(user_input)
        if option < 1 or option > 5:
            print("Invalid input. Please enter a number 1-5. ")
            continue

        user_options(option)
        

def user_options(choice):
    data = importCSV('data.csv')
    match(choice):
        case 1:
            printData('data.csv')
            return
        case 2:
            search_pid = input("Please enter the ID of the element to search for: ")
            search(data, search_pid)
            return
        case 3:
            addRow(data, 'data.csv')
            return
        case 4:
            update_pid = input("Please enter the ID of the element to update: ")
            update(data, update_pid)
            return
        case 5:
            delete_pid = input("Please enter the ID of the element to delete: ")
            delete(data, delete_pid)
            return
        case _:
            return "Invalid Selection"
        

    printData('data.csv')

def importCSV(filename, pk='pid', delimiter=','):
    with open(filename, 'r') as file:
        dataframe={}
        # Read the header line, split by delimiter
        headers = file.readline().replace("\n", '').split(delimiter)
        for line in file:
            # Parse each individual line
            linedata = line.replace("\n", '').split(delimiter)
            row = {}
            
            # Sync row data to header category
            for i in range(len(headers)):
                if i in range(len(linedata)):
                    row[headers[i]] = linedata[i]
                else:
                    # If theres a category but no matching data in the row insert 'null'
                    row[headers[i]] = "null"  
            # insert into data frame  
            dataframe[row[pk]] = [row]
        file.close()
        return dataframe

def printData(filename):
    data = importCSV(filename)
    if not data:
        print("CSV is empty or not loaded.")
        return
    # Empty Table to hold data
    table = []

    # Takes first row gets all the keys and converts
    # To list to use as headers
    headers = list(next(iter(data.values()))[0].keys())

    table.append(headers)

    for x in data:
        rows = []
        for values in data[x][0].values():
            # Build each row
            rows.append(values)
        # Add row to table
        table.append(rows)

    for row in table:
        print(' -- '.join(row))

def addRow(data, filename):
    if not data:
        print("CSV is empty or not loaded.")
        return

    # Get headers from first row
    headers = list(next(iter(data.values()))[0].keys())
    new_row = {}
    lines_count = len(data)
    new_pid = str(lines_count+1)
    new_row[headers[0]] = new_pid
    print("Enter new row data:")

    for h in headers[1:]:
        value = input(f"{h}: ").strip()
        if value:
            new_row[h] = value
        else:
            new_row[h] = "null"

    # Use first column value as the key
    row_key = new_row[headers[0]]
    data[row_key] = [new_row]

    # Append new row to CSV
    with open(filename, "a") as f:
        line = ",".join(new_row[h] for h in headers)
        f.write("\n" + line)

    print(f"Row added: {new_row}")

def search(data, pid):
    if not data:
        print("CSV is empty or not loaded.")
        return
    lines_count = len(data)
    if int(pid) > lines_count:
        print(f"Pid [{pid}] is outdide the data range")
        return
     
    if pid in data:
        row = data[pid][0]  # grab the dictionary for that pid
        row_str = ", ".join(f"{key}: {value}" for key, value in row.items())
        print(f"Found pid {pid}:\n{row_str}")
    else:
        print(f"pid {pid} not found")

def update(data, pid):
    if not data:
        print("CSV is empty or not loaded.")
        return
    lines_count = len(data)
    if int(pid) > lines_count:
        print(f"Pid [{pid}] is outdide the data range")
        return

    headers = list(next(iter(data.values()))[0].keys())
    row = data[pid][0]

    print(f"Updating pid [{pid}]. Press Enter to keep current values.\n")
    for h in headers:
        # skip pid, no user changing it
        if h == headers[0]: 
            continue
        current_value = row[h]
        # For user clarity 
        new_value = input(f"{h} [{current_value}]: ").strip()
        if new_value:
            row[h] = new_value
    data[pid] = [row]

    # Re-write full CSV with all data (including updates)
    headers_line = ",".join(headers)
    rows_list = []
    for key, rows in data.items():
        for r in rows:
            rows_list.append(",".join(str(r[h]) for h in headers))

    with open("data.csv", "w") as f:
        f.write(headers_line + "\n")
        f.write("\n".join(rows_list))

def delete(data, pid):
    if not data:
        print("CSV is empty or not loaded.")
        return
    
    if pid not in data:
        print(f"Pid [{pid}] not found in data.")
        return

    # Get headers
    headers = list(next(iter(data.values()))[0].keys())

    new_list = []
    for key, rows in data.items():
        if key != pid:
            # If no match keep the item/row
            for row in rows:
                row_str = ",".join(str(row[h]) for h in headers)
                new_list.append(row_str)

    with open("data.csv", "w") as f:
        f.write(",".join(headers) + "\n")
        f.write("\n".join(new_list))
    
    print(f"Deleted pid [{pid}].")

if __name__ == "__main__":
    main()
