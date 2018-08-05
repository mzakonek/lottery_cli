import argparse
import sys
from functions import Functions


def run(args):
    if args.person_details and args.predicted_numbers:
        # insert name[0]/surname[1]/numbers into db
        Functions.insert_data_into_db(args.person_details[0], args.person_details[1], args.predicted_numbers)
    elif args.predicted_numbers:
        print("Include person details. Run again with adding '-add_person' phrase and input name and surname")
    elif args.person_details:
        print("Include predicted numbers. Run again with adding '-add_numbers' phrase and input numbers.")
    elif args.json_file:
        # load json file, generate winning numbers and show winners with their prizes
        Functions.start_lottery(args.json_file[0])
    elif len(sys.argv) == 1:
        print("Welcome to the lottery! To get instruction, run again with adding '-h' phrase.")


def main():
    parser = argparse.ArgumentParser(description="Welcome to the lottery CLI. Go to section "
                                                 "'optional arguments' to find functionalities.")
    parser.add_argument("-add_person", help="Input name and surname, in the following order: 1. name 2. surname",
                        dest="person_details", type=str, nargs=2)
    parser.add_argument("-add_numbers", help="Add predicted numbers for mentioned person, without using ',' ",
                        dest="predicted_numbers", type=int, nargs='*')
    parser.add_argument("-start_lottery", help="Load json file with guidelines and START the lottery.",
                        dest="json_file", nargs=1, type=str)
    parser.set_defaults(func=run)
    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()


