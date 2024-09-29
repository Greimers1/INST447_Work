from argparse import ArgumentParser
import requests
import sys
import json

url = f""

def get_holidays(cc, year):
    url = f"https://date.nager.at/Api/v1/Get/{cc}/{year}"
    holi = requests.get(url).json()
    for cc in holi:
        print(f"""{cc['date']}: {cc['name']}""")
    
    
def parse_args(arglist):
    """ Parse command-line arguments. """
    parser = ArgumentParser()
    parser.add_argument("country_code", help="2 letter country code")
    parser.add_argument("year", help="year for holidays")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    get_holidays(args.country_code, args.year)