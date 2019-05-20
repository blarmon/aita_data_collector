import json
import csv
import os.path

def write_json(data_dic, thread_lock):
    with open('data.json', 'a') as data_file:
        thread_lock.acquire()

        data_json = json.dumps(data_dic)

        data_file.write(data_json)
        data_file.close()


def write_csv(data_dic, thread_lock):
    thread_lock.acquire()
    csv_columns = [k for k in data_dic.keys()]

    file_exists = os.path.isfile('data.csv')

    try:
        with open('data.csv', 'a', newline='', encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            if not file_exists:
                writer.writeheader()

            writer.writerow(data_dic)
    except IOError:
        print("I/O error")
    thread_lock.release()


def get_max_date():
    try:
        with open('data.csv', "rU") as csv_file:
            reader = csv.reader(csv_file, delimiter=",")
            next(reader)
            try:
                max_date = max(row[9] for row in reader)
            except ValueError as e:
                print(e)
                return None
        return int(float(max_date))
    except FileNotFoundError as e:
        print(e)
        return None