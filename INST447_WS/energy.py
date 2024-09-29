""" Build a database of energy sources in the US. """


from argparse import ArgumentParser
import sqlite3
import sys



class EnergyDB:
    """
    Creates a sqlite database and reads in data from a csv file
    
    Attributes:
        conn(Connection Object): connection to an in-memory database
    
    """
    
    def __init__(self, filename):
        """
        Instantiates the class
        
        Args: 
            filename (string): string representing the path to a file
        
        """
        self.conn = sqlite3.connect(':memory:')
        self.read(filename)
        
    def __del__(self):
        """ Clean up the database connection. 
        
        Side Effects:
            Closes database connection
            
        """
        try:
            self.conn.close()
        except:
            pass
        
    def read(self, filename):
        """
        
        Args:
            filename(string): refers to path of file
            
        Side Effects:
            Creates a SQL database and inserts information from the csv
                into the DB as a table        
        """
        cur = self.conn.cursor()
        production = '''CREATE TABLE production (
                        year integer, state text, source text, mwh real
                        )'''
        cur.execute(production)
        with open(filename, 'r') as f:
            next(f)
            for line in f:
                year, state, source, mwh = line.strip().split(',')
                year = int(year)
                mwh = float(mwh)
                cur.execute("INSERT INTO production VALUES (?,?,?,?)",
                               (year, state, source, mwh))
        self.conn.commit()
        
    def production_by_source(self, source, year):
        """
        Calculates the total energy production by source and year for 2017
        
        Args:
            source(string): value from Source column in the file
            year(int): value from year in the file
            
        Returns:
            totaw_mwh(float): the sum of the megawhatt hours for chosen 
                              source in 2017
        
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT mwh FROM production WHERE source=? AND year=?", (source, year))
        rows = cursor.fetchall()
        total_mwh = sum(row[0] for row in rows)
        return total_mwh

def main(filename):
    """ Build a database of energy sources and calculate the total production
    of solar and wind energy.
    
    Args:
        filename (str): path to a CSV file containing four columns:
            Year, State, Energy Source, Megawatthours.
    
    Side effects:
        Writes to stdout.
    """
    e = EnergyDB(filename)
    sources = [("solar", "Solar Thermal and Photovoltaic"),
               ("wind", "Wind")]
    for source_lbl, source_str in sources:
       print(f"Total {source_lbl} production in 2017: ",
             e.production_by_source(source_str, 2017))


def parse_args(arglist):
    """ Parse command-line arguments. """
    parser = ArgumentParser()
    parser.add_argument("file", help="path to energy CSV file")
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)
