import json
import pandas as pd
import csv


def convert_data_file2csv(data_file_path, tsv_file_path, attributes, max_lines):
    data_file = open(data_file_path, "r")
    csvfile = open(tsv_file_path, 'w', newline='')
    # Writer of csv file
    writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)

    for i in range(max_lines):
        line = data_file.readline()
        # End of file
        if not line:
            break
        # Convert json String to dictionary
        dic = json.loads(line)
        # Filter edge cases
        if dic["review_count"] < 100 or dic["review_count"] > 1000:
            continue
        values = []
        for s in attributes:
            values.append(dic[s])
        writer.writerow(values)

    data_file.close()
    csvfile.close()


def generalize_csv(tsv_file_path, generalized_tsv_file_path, attributes):
    # Read tsv file using pandas
    df = pd.read_csv(tsv_file_path, sep='\t', index_col=False, header=None, names=attributes)
    # Bin each attributes into categorical range (e.g., 456 -> 400-500)
    values, labels = bin_values_and_labels(df["review_count"].max(), 1000, 100)
    df["review_count"] = pd.cut(df["review_count"], bins=values, labels=labels)
    df["yelping_since"] = bin_years(df["yelping_since"])
    values, labels = bin_values_and_labels(df["useful"].max(), 2000, 100)
    df["useful"] = pd.cut(df["useful"], bins=values, labels=labels)
    values, labels = bin_values_and_labels(df["funny"].max(), 1000, 100)
    df["funny"] = pd.cut(df["funny"], bins=values, labels=labels)
    values, labels = bin_values_and_labels(df["cool"].max(), 1000, 100)
    df["cool"] = pd.cut(df["cool"], bins=values, labels=labels)
    values, labels = bin_values_and_labels(df["fans"].max(), 200, 10)
    df["fans"] = pd.cut(df["fans"], bins=values, labels=labels)
    values, labels = bin_values_and_labels(df["average_stars"].max(), 5, 0.5)
    df["average_stars"] = pd.cut(df["average_stars"], bins=values, labels=labels)
    df = df.astype(str).replace(to_replace=r'^nan$', value='', regex=True)
    df.to_csv(generalized_tsv_file_path, sep='\t', index=False)


def bin_values_and_labels(max_value, threshold, bin_size):
    values = [0]
    labels = []
    upper = bin_size
    while upper < max_value and upper < threshold:
        values.append(upper)
        labels.append(f'{upper - bin_size}-{upper}')
        upper += bin_size
    values.append(upper)
    labels.append(f'{upper - bin_size}-{upper}')
    if threshold < max_value:
        values.append(max_value)
        labels.append(f'>{threshold}')
    return values, labels


def bin_years(origin_years):
    result = []
    for s in origin_years:
        result.append(s[0:4])
    return result
