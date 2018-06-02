#!/usr/bin/env python
from argparse import ArgumentParser
from bio_chem_data import BioChemData
from data_summary import DataSummary

#from pprint import pprint


def main():

    # cli args
    parser = ArgumentParser()

    parser.add_argument(
        '-v', '--verbose',
        help='More verbose output',
        action='store_true',
        default=False,
    )


    parser.add_argument(
        '-r', '--rootpath',
        help='root path',
        required=True
    )

    parser.add_argument(
        '-p', '--pattern',
        help='pattern to look for',
        required=True
    )

    args = parser.parse_args()

    df1 = BioChemData(
        root_path=args.rootpath,
        pattern=args.pattern,
    )

    args = parser.parse_args()

    df2 = DataSummary(
        root_path=args.rootpath,
        pattern=args.pattern,
    )

    #df1.modify_biochem2()
    #df1.analyze_biochem()
    df2.generate_summary()



    

    

   




if __name__ == '__main__':
    main()