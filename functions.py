import mysql.connector

hostname = "localhost"
username = "root"
password = "pipiriukaS56"
database = "sakila"
portAddress = 3317


# Imports data from sql server according to given SQL query as a list of tuples:
def getSQLData(SQLquery):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(host=hostname, port=portAddress, user=username, password=password, database=database)
        cursor = connection.cursor()
        query = SQLquery
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# From given list of tupples, changes them to lists and number in indeex place to float:
def changeToFloat(sampleData, index):
    for i in range(len(sampleData)):
        sampleData[i] = list(sampleData[i])
        sampleData[i][index] = float(sampleData[i][index])
    return sampleData


# Prints given number of rows with a note at the end:
def printRows(sampleData,lines = 0):
    for i in range(len(sampleData)):
        if lines == 0:
            print(sampleData[i])
        else:
            if i < lines:
                print(sampleData[i])
            if i == lines:
                print(f'Only first {lines} rows printed.')


# From given list of tuples does GROUP BY sum (count = Falce and addValueFromIndex with value) or count by given value:
def sumBy(sampleData, byValue, addValueFromIndex = None, count = True):
    outputDict = {}
    for i in sampleData:
        if count == True:
            if i[byValue] not in outputDict:
                outputDict[i[byValue]] = 0
            outputDict[i[byValue]] += 1
        if count == False:
            if i[byValue] not in outputDict:
                outputDict[i[byValue]] = 0.0
            outputDict[i[byValue]] += i[addValueFromIndex]
            outputDict[i[byValue]] = round(outputDict[i[byValue]], 2)
    return outputDict


