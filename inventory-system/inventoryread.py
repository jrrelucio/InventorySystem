import pandas as pd
from openpyxl import load_workbook
#df = pd.read_excel("current_stocks.xlsx") #changed directory, make sure that the program runs on the location of file \inventory-system\
stocks = load_workbook(filename="current_stocks.xlsx")

def get_all_description(df):
    return list(df['Description'])

def get_all_case_values(df):
    return list(df['Case'])

def get_all_piece_values(df):
    return list(df['Piece'])

def get_all_ppc_values(df):
    return list(df['Piece Per Case'])

def update_stocks_df(df, index, newcase, newpiece):
   df.at[index, "Case"] = newcase
   df.at[index, "Piece"] = newpiece
   df.to_excel("current_stocks.xlsx", sheet_name="Inventory", index=False)
   print("Dataframe updated")

def update_history_ml(history, sheet):
    df = pd.DataFrame(history, columns = ['Agent', 'Description', 'Case', 'Piece'])
    df.to_excel("historyml.xlsx", sheet_name=sheet, index=False)
    print("History Updated")

def update_history_bl(history, sheet):
    df = pd.DataFrame(history, columns = ['Agent', 'Description', 'Case', 'Piece'])
    df.to_excel("historybl.xlsx", sheet_name=sheet, index=False)
    print("History Updated")

