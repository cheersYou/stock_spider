import csv
csv_writter = None


def initCSV(path):
    global csv_writter
    # csv在excel中乱码，则采用utf_8_sig编码方式
    f = open(path, "w", encoding="utf_8_sig", newline="\n")
    csv_writter = csv.writer(f)
    return f


def writeCsvHeader(header):
    csv_writter.writerow(header)


def writeCsvRow(row):
    csv_writter.writerow(row)
