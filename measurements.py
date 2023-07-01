import pandas as pd

class Meas():
    def __init__(self):
        from database import DBHandler
        self.db = DBHandler()
        self.pots = self.db.read_pot_tbl()

    def read_csv(self, pot_id):
        file_path = f"PyFloraPots/pot_data_id_{pot_id}.csv"
        df = pd.read_csv(file_path)
        df.datetime = df.datetime.str.slice(0,19)
        df.datetime = pd.to_datetime(df.datetime)
        return df

    def read_csv_all(self):
        return tuple(self.read_csv(pot.id_number) for pot in self.pots)

#if __name__ == '__main__':
    #meas_app = Meas()
    #print(meas_app.read_csv(1))
    #print(meas_app.read_csv_all()[1])
