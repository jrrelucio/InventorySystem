import pandas as pd
import numpy as np
from datetime import date
#df = pd.read_excel("current_stocks.xlsx") #changed directory, make sure that the program runs on the location of file \inventory-system\

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

def update_delivery(df_initial, index, newcase, newpiece):
    df_initial.at[index, "Delivery (Case)"] = newcase
    df_initial.at[index, "Delivery (Piece)"] = newpiece
    df_initial.to_excel("initial_stocks.xlsx", sheet_name="Inventory", index=False)
    print("Dataframe updated")


#df_current_stocks = pd.read_excel("current_stocks.xlsx")
#description_list = get_all_description(df_current_stocks)

#DESCRIPTION
def create_description_df(description_list):
    mux = pd.MultiIndex.from_product([['DESCRIPTION'], ['ITEMS']])   
    df_description = pd.DataFrame(description_list, columns=mux)
    return df_description

#INITIAL STOCKS
def create_stocks_table(df_current_stocks, title):
    mux = pd.MultiIndex.from_product([[title], ['CASE','PIECE']])
    case_list = get_all_case_values(df_current_stocks)
    piece_list = get_all_piece_values(df_current_stocks)
    #merge case and piece into one tuple
    case_piece_tuples = list(zip(case_list, piece_list))
    df_stocks = pd.DataFrame(case_piece_tuples, columns=mux)
    return df_stocks


#MORNING LOAD initialization
df_history_ml = pd.read_excel("historyml.xlsx")

def load_table(df_history, description_list, title): #this function creates a morning/backload table and fills the values based on df_history
    agent_names = sorted(list(set(list(df_history['Agent']))))
    mux = pd.MultiIndex.from_product([agent_names, ['CASE','PIECE']])
    data = [tuple([None]*len(agent_names)*2) for x in range(len(description_list))] #empty data
    #print(len(data[0]))
    df_load = pd.DataFrame(data, columns=mux)
    df_load["END"] = np.nan
    #print(df_morning_load)
    #print(df_morning_load)

    #ITERATE OVER HISTORY DF
    for ind in df_history.index:
        agent = df_history['Agent'][ind]
        description = df_history['Description'][ind]
        case = df_history['Case'][ind]
        piece = df_history['Piece'][ind]
        #print([agent, description, case, piece])
        description_index = description_list.index(description)
        if case != 0:
            df_load.at[description_index, (agent, "CASE")] = case
        if piece != 0:
            df_load.at[description_index, (agent, "PIECE")] = piece
        #print(agent_index)
    return df_load

def copy_current_to_initial(df_current):
    df_current.to_excel("initial_stocks.xlsx", sheet_name="Inventory", index=False)
    print('INITIAL STOCKS UPDATED')

#BACKLOAD EMPTY

#agent_names = list(set)
#agent_names 




#print(result)
