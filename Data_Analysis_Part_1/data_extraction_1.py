# Function itself
def Data_Extract(name):
    """
    Data_Extract( str ) -> dictionairy
    This function takes the name (or path) of a raw HoQI data file and extracts the collumns of this file as lists embedded in a dictionairy, using the headers of columns as keys for the lists that are made up of the values of said columns
    """
    with open(name, 'r') as file:
        column_line = file.readline()
        column_names = column_line.split()
        # Removing the # at the start of the column names
        column_names.pop(0)

        dictionairy_columns = {column: [] for column in column_names}
        next(file)

        for line in file:
            line_split = line.split()
            for i in range(0,len(line_split)):
                 dictionairy_columns[column_names[i]].append(float(line_split[i]))
    
    return dictionairy_columns

# Testing code of the function in abstraction
with open('Data_Analysis_Part_1/20260421_HoQIs.txt', 'r') as file:
        column_line = file.readline()
        column_names = column_line.split()
        column_names.pop(0)

        dictionairy_columns = {column: [] for column in column_names}
        next(file)

        for line in file:
            line_split = line.split()
            for i in range(0,len(line_split)):
                 dictionairy_columns[column_names[i]].append(float(line_split[i]))