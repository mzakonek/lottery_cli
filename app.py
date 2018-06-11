import argparse
import json
import sys
import itertools
import sqlite3
import random

conn = sqlite3.connect("people_and_numbers.db", isolation_level=None)  # autocommit mode ON
cursor = conn.cursor()


def run(args):
    if args.person_details and args.predicted_numbers:
        name = args.person_details[0]
        surname = args.person_details[1]
        numbers_list = args.predicted_numbers
        # using zip to create an iterator
        values_to_insert = zip(itertools.repeat(name), itertools.repeat(surname), numbers_list)

        # insert name/surname/number into db using zip object
        cursor.executemany("INSERT INTO info (name, surname, number) VALUES (?, ?, ?)", values_to_insert)

        print("Data successfully inserted into database.")
    elif args.predicted_numbers:
        print("Include person details. Run again with adding '-input_person' phrase and input name and surname")
    elif args.person_details:
        print("Include predicted numbers. Run again with adding '-add_numbers' phrase and input numbers.")
    elif args.json_file:
        # numbers generator function
        def generate_numbers(numbers_quantity_value, min_value, max_value):
            drawn_numbers = []
            for i in range(numbers_quantity_value):
                drawn_numbers.append(random.randrange(min_value, max_value+1))
            return drawn_numbers

        with open(args.json_file[0]) as f:
            try:
                # loading data from json file
                guidelines_dict = json.load(f)
                numbers_quantity = guidelines_dict['numbers-quantity']
                min_ = guidelines_dict["numbers-range"]["min"]
                max_ = guidelines_dict["numbers-range"]["max"]
                prize_pool = guidelines_dict["prize-pool"]
                # generating winning numbers
                winning_numbers = generate_numbers(numbers_quantity, min_, max_)
                # select winners from db
                cursor.execute(('''SELECT name || ' ' || surname AS new_col FROM info WHERE number IN {} '''
                                .format(tuple(winning_numbers))))
                winners = cursor.fetchall()
                # creating dict with number of wins for winners
                counted_winners_dict = dict((i, winners.count(i)) for i in set(winners))
                # creating total number of winners
                total_number = 0
                for i in counted_winners_dict.values():
                    total_number += i
                # catch ZeroDivisionError
                if total_number == 0:
                    print("No winners.")
                    exit()
                else:
                    prize_per_one = prize_pool / total_number
                for k, v in counted_winners_dict.items():
                    counted_winners_dict[k] = v*prize_per_one
                print("Winning numbers:", winning_numbers)
                print("The winners with the amount of prize:", counted_winners_dict)
            except ValueError as e:
                print("Invalid json file: %s" % e)
    elif len(sys.argv) == 1:
        print("Welcome to the lottery! To get instruction, run again with adding '-h' phrase.")


def main():
    parser = argparse.ArgumentParser(description="Welcome to the lottery CLI. Go to section "
                                                 "'optional arguments' to find functionalities.")
    parser.add_argument("-add_person", help="Input name and surname, in the following order: 1. name 2. surname",
                        dest="person_details", type=str, nargs=2)
    parser.add_argument("-add_numbers", help="Add predicted numbers for mentioned person",
                        dest="predicted_numbers", type=int, nargs='*')
    parser.add_argument("-start_lottery", help="Load json file with guidelines and START the lottery.",
                        dest="json_file", nargs=1, type=str)
    parser.set_defaults(func=run)
    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()


