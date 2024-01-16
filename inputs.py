"""Inputs.

Take input and return data in format of list[dict]


Example of output:
[
    {
    'assay_no': 'Eve_123', "aliquote": '1/20',
    'project': 'No. 23',
    'cell_line': 'COLO205'
    'conc': 'x10e6 cell/ml',
    'medium': 'RPMI-1640/10%DMSO',
    'date': '23.1.2010',
    },
    {
    'assay_no': 'Eve_123', "aliquote": '2/20',
    'project': 'No. 23',
    'cell_line': 'COLO205'
    'conc': 'x10e6 cell/ml',
    'medium': 'RPMI-1640/10%DMSO',
    'date': '23.1.2010',
    },
    {...},
    {...},
]

"""
import csv
import logging
from database_app import project_database_con, cell_culture_database_con, bac_database_con, protein_database_con

log = logging.getLogger(__name__)

# All
valid_projects = project_database_con()
VALID_PROJECTS = []
for index, value in enumerate(valid_projects):
    first_item = value[0]
    second_item = value[1]
    if first_item < 10:
        edited_first_item = f"0{first_item}"
    else:
        edited_first_item = first_item
    shortened = (edited_first_item, second_item)
    VALID_PROJECTS.append(shortened)

# Bacteria
VALID_BAC = bac_database_con()

# Cell Culture
cc_in_database = cell_culture_database_con()
CELL_MEDIUM = dict(cc_in_database)

# Protein
VALID_UNITS = protein_database_con()

def better_input(question, value_type, valid_options=None):
    """Validate input based on the passed value type.

    Upon error continuously prompt user for correct answer.
    """

    while True:
        try:
            answer = value_type(input(f'{question}{valid_options if valid_options is not None else ""}: '))

            if valid_options and answer not in valid_options:
                raise ValueError('neni z povolených hodnot')

            if not answer:
                raise ValueError('Nepovolujeme prázné hodnoty a nuly.')

        except ValueError:
            print('Špatně zadaná hodnota')

        else:
            return answer


def user_input():
    """Take input from user.

    Exmaple input:
    'assay_no': 'Eve_123',
    "total_aliquotes": 20,
    'project': 'No. 23',
    'cell_line': 'COLO205'
    'conc': '10x10e6 cell/ml',
    'medium': 'RPMI-1640/10%DMSO',
    'date': '23.1.2010',
        -- další? [a/n]:
    """

    entries = []
    while True:
        item = {
            'assay_no'      : better_input('assay_no', str),
            'total_aliquotes'     : better_input('total_aliquotes', int),
            'project'       : better_input('project', str, valid_options=VALID_PROJECTS),
            'cell_line'     : better_input('cell line', str, valid_options=CELL_MEDIUM.keys()),
            'conc'          : better_input('conc', int),
            #'medium'        : better_input('medium', str, valid_options=VALID_MEDIUM),
            'date'          : better_input('date', str),
        }
        item["medium"] = CELL_MEDIUM.get(item["cell_line"], "")
        entries.append(item)

        next_q = input('-- další? [a/n]: ')
        if next_q == 'n':
            return entries


def csv_input(file_path):
    pass
    """Load data from csv."""
    log.info('loading data from csv file')
    with open(file_path, encoding='UTF-8') as file:
        reader = csv.DictReader(file, quoting=csv.QUOTE_NONNUMERIC)
        data = list(reader)
    for item in data:
        VALID_PROJECTS.append(item)
        #item["unit"] = VALID_FORMS.get(item["form"], "")
    # TODO: validate data, remove and notify about the unvalid
    return data
