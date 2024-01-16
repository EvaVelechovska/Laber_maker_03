import logging
from itertools import zip_longest

LABELS_PER_PAGE = 60

log = logging.getLogger(__name__)


def split_to_page_size(data):
    """split data to chunks based on labels per page"""
    log.debug('splitting data to pages')
    # prepare fill dict with empty values
    # NOTE: this is so the rest of the page fills as blank and is not printed
    fill_value = {k: '' for k in data[0]}
    args = [iter(data)] * LABELS_PER_PAGE
    log.debug('done')
    return zip_longest(*args, fillvalue=fill_value)


def enumerate_keys(page_data):
    """Edit keys so they can be used in replacement.

    name -> name_1, name_2 ...
    """
    log.debug('enumerating keys')
    result = []
    for num, item in enumerate(page_data, start=1):
        renamed = {}
        for key, value in item.items():
            renamed[f'{key}_{num}'] = value
        result.append(renamed)
    log.debug('done')
    return result


def merge_page_data(data):
    """Merge list of dictionaries into one."""
    log.debug('merging page data to a single dictionary')
    data_dict = {}
    for dct in data:
        data_dict = {**data_dict, **dct}
    log.debug('done')
    return data_dict


def prepare_rows(data):
    """Reformat the dicts for replacing.

    We need keys "raw1" "raw2" "raw3" "raw3" "raw4" "raw5"
    """
    log.debug('preparing rows')
    new_data = []
    for dct in data:
        raw1 = '{assay_no}: {aliquotes}'.format(**dct)
        raw2 = 'Project: {project}'.format(**dct)
        raw3 = '{cell_line}'.format(**dct)
        raw4 = 'in {medium}/10%DMSO'.format(**dct)
        raw5 = '{conc}x10e6 c/ml, {date}'.format(**dct)

        new_data.append(
            {
                'raw1'  : raw1,
                'raw2'  : raw2,
                'raw3'  : raw3,
                'raw4'  : raw4,
                'raw5'  : raw5,
            }
        )
    log.debug('done')
    return new_data


def prepare_rows_bac(data):
    """Reformat the dicts for replacing.

    We need keys "raw1" "raw2" "raw3" "raw3" "raw4" "raw5"
    """
    log.debug('preparing rows')
    new_data = []
    for dct in data:
        raw1 = '{assay}: {solution}, {aliquotes}'.format(**dct)
        raw2 = 'Project: {project}'.format(**dct)
        raw3 = '{insert}'.format(**dct)
        raw4 = '{bacteria}'.format(**dct)
        raw5 = '{conc}, {date}'.format(**dct)

        new_data.append(
            {
                'raw1'  : raw1,
                'raw2'  : raw2,
                'raw3'  : raw3,
                'raw4'  : raw4,
                'raw5'  : raw5,
            }
        )
    log.debug('done')
    return new_data


def prepare_rows_pr(data):
    """Reformat the dicts for replacing.

    We need keys "raw1" "raw2" "raw3" "raw3" "raw4" "raw5"
    """
    log.debug('preparing rows')
    new_data = []
    for dct in data:
        raw1 = '{supplier}'.format(**dct)
        raw2 = '{c}, {lot}'.format(**dct)
        raw3 = '{name}'.format(**dct)
        raw4 = '{conc}, {unit}'.format(**dct)
        raw5 = '{date}, {aliquotes} '.format(**dct)

        new_data.append(
            {
                'raw1'  : raw1,
                'raw2'  : raw2,
                'raw3'  : raw3,
                'raw4'  : raw4,
                'raw5'  : raw5,
            }
        )
    log.debug('done')
    return new_data

def bac_to_csv(klice, output):
    with open("templates/bac_data.csv", "w") as f:
        f.write('"')
        f.write('","'.join(klice))
        f.write('"\n')
        for row in output:
            f.write('"')
            f.write('","'.join(str(x) for x in row))
            f.write('"\n')


def cc_to_csv(klice, output):
    with open("templates/cc_data.csv", "w") as f:
        f.write('"')
        f.write('","'.join(klice))
        f.write('"\n')
        for row in output:
            f.write('"')
            f.write('","'.join(str(x) for x in row))
            f.write('"\n')

def pr_to_csv(klice, output):
    with open("templates/pr_data.csv", "w") as f:
        f.write('"')
        f.write('","'.join(klice))
        f.write('"\n')
        for row in output:
            f.write('"')
            f.write('","'.join(str(x) for x in row))
            f.write('"\n')