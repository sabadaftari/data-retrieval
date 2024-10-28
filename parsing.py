import argparse


def define_flag(v):
    if v.lower() in ('defined', 'undefined', ''):
        pass
    else:
        raise argparse.ArgumentTypeError('Value entered is unexpected.')
    
def add_download_args(parser):
    # Metadata args
    parser.add_argument('--Species', default='human', type=str)
    parser.add_argument('--BSource', default='PBMC', type=str)
    parser.add_argument('--BType', default = 'Unsorted-B-Cells', type=str)
    parser.add_argument('--Longitudinal', type=define_flag)
    parser.add_argument('--Age',type=define_flag)
    parser.add_argument('--Disease', type=str)
    parser.add_argument('--Subject', type=define_flag)
    parser.add_argument('--Vaccine', default=None, type=str)    
    parser.add_argument('--Chain', type=str)  
    parser.add_argument('--Isotype', type=str)  


def add_desired_seq_args(parser):
    # Pre-entry args
    parser.add_argument('--first_desired_column',default = 'sequence_alignment_aa', type=str)
    parser.add_argument('--second_desired_column',default = 'germline_alignment_aa', type=str)
    parser.add_argument('--third_desired_column',default = 'v_call', type=str)
    parser.add_argument('--fourth_desired_column',default = 'd_call', type=str)
    parser.add_argument('--fifth_desired_column',default = 'j_call', type=str)
    parser.add_argument('--sixth_desired_column',default = 'ANARCI_status', type=str)

def add_parse_args(parser):
    
    subparsers = parser.add_subparsers()

    parser_metadata = subparsers.add_parser("Metadata")
    add_download_args(parser_metadata)

    parser_pre_entry = subparsers.add_parser("Pre-entry")
    add_desired_seq_args(parser_pre_entry)
