import pandas as pd
df = pd.read_excel(r'C:\Users\Joshua\Desktop\Inventory System\InventorySystem\inventory-system\current_stocks.xlsx')
print(df)

def get_all_description(df):
    return list(df['Description'])

def get_all_case_values(df):
    return list(df['Case'])

def get_all_piece_values(df):
    return list(df['Piece'])

def get_all_ppc_values(df):
    return list(df['Piece Per Case'])