import argparse
import os
import pandas as pd
from datetime import datetime
from tabulate import tabulate


def init_data():
    features = ["title", "note", "date"]
    plan = pd.DataFrame(columns=features)

    loc_dir = os.path.abspath(os.getcwd())
    dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))
    data_path = os.path.abspath(os.path.join(dir_path, "data.csv"))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        plan.to_csv(data_path, index=False)
    else:
        if not os.path.exists(data_path):
            plan.to_csv(data_path, index=False)

        else:
            plan = pd.read_csv(data_path, index_col=False)
    return plan


def update_data(plan):
    loc_dir = os.path.abspath(os.getcwd())
    dir_path = os.path.abspath(os.path.join(loc_dir, "..", "data"))
    data_path = os.path.abspath(os.path.join(dir_path, "data.csv"))
    plan.to_csv(data_path, index=False)
    return


def add_note(args, plan):
    item = {}
    for name in plan.columns:
        item[str(name)] = vars(args)[str(name)]

    plan = plan.append(pd.DataFrame(item, index=[0]))
    update_data(plan)

    return plan  # questo credo che vada eliminato


def add_note_verbose(
        args: argparse.Namespace,  # parser arguments
        plan: pd.DataFrame  # DataFrame to be updated
        ) -> pd.DataFrame:
    """
    Parameters
    ----------
    plan: pd.DataFrame

    Returns
    -------
    plan: pd.DataFrame with the added note

    Notes
    -----
    This function adds a new note to the existing planner.
    It uses an input/output interface; this is more convenient to use with larger notes or notes with tags.

    Warnings
    --------
    This function must be updated everytime the columns of the plan are changed
    """

    item = {}  # initializing the new note

    "title"
    title = input("Please, insert the title: ")
    item["title"] = title

    "body"
    print("It's time to write your note")
    note = input()
    item["note"] = note

    "data"
    data = input("Insert the data (press Enter to use the current data): ")
    if data == '':  # insert the current data if requested
        data = datetime.today().strftime('%Y-%m-%d')
    item["date"] = data

    "updating the plan"
    plan = plan.append(pd.DataFrame(item, index=[0]))
    update_data(plan)


def print_planner(plan):
    plan_tab = lambda plan: tabulate(plan,
                                     headers=[str(plan.columns[0]), str(plan.columns[1]), str(plan.columns[2])],
                                     tablefmt="fancy_grid",
                                     showindex=False)
    print(plan_tab(plan))
    return


def search_and_print(args):
    pass


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='possible actions', dest='subparser')

    plan = init_data()

    # insert parser
    insert_parser = subparsers.add_parser('insert', help='Insert a new item into the planner')
    insert_parser.add_argument("-v", "--verbose",
                               help="increase output verbosity", action="store_true")
    insert_parser.add_argument(str(plan.columns[0]),
                               help='Title of the note', type=str, nargs='?', default="...")
    insert_parser.add_argument(str(plan.columns[1]),
                               help='Body of the note', type=str, nargs='?', default="...")
    insert_parser.add_argument(str(plan.columns[2]),
                               help='Date of the note', type=str, nargs='?',
                               default=datetime.today().strftime('%Y-%m-%d'))

    # print parser
    print_parser = subparsers.add_parser('print', help='Print out all the notes')

    # search parser
    search_parser = subparsers.add_parser('search', help='Find and print the notes that contain -word-')
    search_parser.add_argument('word',
                               help='word to be searched in planner and printed out',
                               type=str)

    args = parser.parse_args()

    if args.subparser == 'insert':
        if args.verbose:
            plan = add_note_verbose(args, plan)
        else:
            plan = add_note(args, plan)

    elif args.subparser == 'print':
        print_planner(plan)

    elif args.subparser == 'search':
        search_and_print(args)


if __name__ == '__main__':
    main()
