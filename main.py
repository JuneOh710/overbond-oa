import sys


def list_to_csv(l: list) -> str:
    csv = ""
    for element in l:
        csv += element + ", "
    return csv.rstrip(", ") + '\n'


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


def main() -> int:
    # check for command line arguments
    if len(sys.argv) != 3:
        print("Usage:\n\tPass both the file name to parse and output.\n\tpython3 main.py <input> <output>")
        return 0
    else:
        input_file_name = sys.argv[1]
        output_file_name = sys.argv[2]

    input_file = open(input_file_name, 'r')
    data_list = input_file.readlines()
    output_file = open(output_file_name, 'w')
    output_file.write("Issuance Date, CleanBid, CleanAsk, Last Price\n")
    code_to_column = {
        "DIs": 0,
        "BPr": 1,
        "APl": 2,
        "Pl": 3
    }
    row = [0, 0, 0, 0]
    for i in range(len(data_list)):
        line = data_list[i]
        # remove whitespaces and turn string into list
        line = line.split()
        for s in line:
            prefix = extract_prefix(s)
            row[code_to_column[prefix]] = s.lstrip(prefix)

        if (i+1) % 10 == 0:
            # write to output at the end of each entry (10 rows)
            output_file.write(list_to_csv(row))

    input_file.close()
    output_file.close()
    return 1


if __name__ == "__main__":
    main()
