import csv

FILENAMES = ["IDCJAC0009_040212_1800", "IDCJAC0009_040224_1800",
             "IDCJAC0009_040320_1800", "IDCJAC0009_040770_1800",
             "IDCJAC0009_040790_1800", "IDCJAC0009_040842_1800",
             "IDCJAC0009_040913_1800", "IDCJAC0009_040965_1800",
             "IDCJAC0009_040976_1800"]

def csvlist2list(file_names, summary = False):
    """
    csvlist2list converts the nice csv files to a list of python dictionarys
    
    Parameters
    ----------
    file_names : list<string>
        The list of folder names, e.g ["IDCJAC0009_040320_1800"]
    Returns
    -------
    a map of (day, month, year) -> value measured
    """
    
    data = []
    meta = {}
    summary_data = []
    for filename in file_names:
        file = open(filename+"/"+filename+"_Data.csv")
        txtfile = open(filename+"/"+filename+"_Note.txt").readlines()
        data.append({})
        summary_data.append(0)
        filecontent = csv.reader(file, delimiter = ",")
        for line in list(filecontent)[1:]:
            if line[6] == "" or line[5] == "" or line[5] == "0":
                summary_data[len(summary_data)-1] += 1
                continue
            data[len(data)-1][(int(line[4]), int(line[3]), int(line[2]))] = float(line[5])/float(line[6])
        meta[int(filename.split("_")[1])] = (float(txtfile[13].split(":")[1]),float(txtfile[14].split(":")[1]))
        file.close()
    
    if summary:
        for sensor in range(len(data)):
            print("Sensor " + str(list(meta.keys())[sensor]) + ", is located at position " + str(meta[list(meta.keys())[sensor]]) + ".")
            print("The data spans from " + str(list(data[sensor].keys())[0]) + ", till " + str(list(data[sensor].keys())[len(data[sensor].keys())-1]))
            print("Of the " + str(len(data[sensor]) + summary_data[sensor]) + " days the sensor was online, " +  str(len(data[sensor])) + " days were operational")
            print("")
    return data, meta


if __name__ == "__main__":
    DATA, META = csvlist2list(FILENAMES, summary = True)