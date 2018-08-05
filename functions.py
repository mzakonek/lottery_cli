import itertools
import sqlite3
import json
import random

conn = sqlite3.connect("people_and_numbers.db", isolation_level=None)  # autocommit mode ON
cursor = conn.cursor()


class Functions(object):

    @staticmethod
    def insert_data_into_db(name, surname, numbers_list):
        # use zip to create an iterator
        values_to_insert = zip(itertools.repeat(name), itertools.repeat(surname), numbers_list)

        # insert name/surname/number into db using zip object
        cursor.executemany("INSERT INTO info (name, surname, number) VALUES (?, ?, ?)", values_to_insert)

        print("Data successfully inserted into database.")

    @staticmethod
    def start_lottery(json_file):

        def generate_numbers(numbers_quantity_value, min_value, max_value):
            drawn_numbers = []
            for i in range(numbers_quantity_value):
                drawn_numbers.append(random.randrange(min_value, max_value+1))
            return drawn_numbers

        def load_data_from_json(json_file):
            guidelines_dict = json.load(json_file)
            numbers_quantity = guidelines_dict['numbers-quantity']
            min_ = guidelines_dict["numbers-range"]["min"]
            max_ = guidelines_dict["numbers-range"]["max"]
            prize_pool = guidelines_dict["prize-pool"]
            return numbers_quantity, min_, max_, prize_pool

        with open(json_file) as f:
            try:
                # load data from json file
                json_data = load_data_from_json(f)

                # generate winning numbers
                winning_numbers = generate_numbers(json_data[0], json_data[1], json_data[2])

                # select winners from db
                cursor.execute(('''SELECT name || ' ' || surname AS new_col FROM info WHERE number IN {} '''
                                .format(tuple(winning_numbers))))
                winners = cursor.fetchall()

                # create dict with number of wins for winners
                counted_winners_dict = dict((i, winners.count(i)) for i in set(winners))

                # create total number of winners
                total_number = 0
                for i in counted_winners_dict.values():
                    total_number += i
                # catch ZeroDivisionError
                if total_number == 0:
                    print("No winners.")
                    exit()
                else:
                    prize_per_one = json_data[3] / total_number
                for k, v in counted_winners_dict.items():
                    counted_winners_dict[k] = v*prize_per_one
                print("Winning numbers:", winning_numbers)
                print("The winners with the amount of prize:", counted_winners_dict)
            except ValueError as e:
                print("Invalid json file: %s" % e)
