import sys
import pandas as pd
import matplotlib.pyplot as plt


def list_to_csv(l: list) -> str:
    csv = ""
    for element in l:
        csv += element + ","
    return csv.rstrip(",") + '\n'


def extract_prefix(s: str) -> str:
    prefix = ""
    if s.startswith("BPr"):
        prefix = "BPr"
    elif s.startswith("DIs"):
        prefix = "DIs"
    elif s.startswith("APl"):
        prefix = "APl"
    elif s.startswith("Pl"):
        prefix = "Pl"
    return prefix


def process_prefix(s: str, prefix: str) -> str:
    s = s.lstrip(prefix)
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    if prefix == "DIs":
        # process insurance date
        year = s[0:4]
        month = month_names[int(s[4:6].lstrip("0"))]
        day = s[6:]
        s = f"{year}-{month}-{day}"

    return s


def plot_data(file_name: str):
    df = pd.read_csv(file_name, parse_dates=True)
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(x=df["Insurance Date"],
                y=df["CleanBid"], s=10, c='r', label='CleanBid')
    ax1.scatter(x=df["Insurance Date"],
                y=df["CleanAsk"], s=10, c='g', label='CleanAsk')
    ax1.scatter(x=df["Insurance Date"],
                y=df["Last Price"], s=10, c='b', label='Last Price')
    plt.legend(loc='upper left')
    plt.show()


def write_to_csv(input_file_name: str, output_file_name: str):
    input_file = open(input_file_name, 'r')
    data_list = input_file.readlines()
    output_file = open(output_file_name, 'w')
    output_file.write("Insurance Date,CleanBid,CleanAsk,Last Price\n")
    code_to_column = {"DIs": 0, "BPr": 1, "APl": 2, "Pl": 3}
    row = [0, 0, 0, 0]
    for i in range(len(data_list)):
        line = data_list[i]
        # remove whitespaces and turn string into list
        line = line.split()
        for s in line:
            prefix = extract_prefix(s)
            if prefix != "":
                row[code_to_column[prefix]] = process_prefix(s, prefix)

        if (i+1) % 10 == 0:
            # write to output at the end of each entry (10 rows)
            output_file.write(list_to_csv(row))

    input_file.close()
    output_file.close()


def main() -> int:
    # check for command line arguments
    if len(sys.argv) != 3:
        print("Usage:\n\tPass both the file name to parse and output.\n\tpython3 main.py <input>.txt <output>.csv")
        return 0
    else:
        input_file_name = f"./input/{sys.argv[1]}"
        output_file_name = f"./output/{sys.argv[2]}"

    write_to_csv(input_file_name, output_file_name)
    plot_data(output_file_name)
    return 1


if __name__ == "__main__":
    main()
