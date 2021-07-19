import datetime
from environment import *

# Decide what to do
def choice():
    print('')
    print('What do you want to do?')
    print('"1" to add a new asset')
    print('"2" to delete an asset')
    print('"3" to check portfolio')
    print('"4" refresh prices in portfolio')
    print('"5" to quit')
    option = str(input('Option: '))
    # option 1 inserts asset
    if option == str(1):
        while True:
            asset = str(input('\nInsert asset: ')).upper()
            try:
                cryptocompare.get_price([asset],['USD'])[asset]['USD']
                break
            except TypeError:
                print('The token couldnt be found, try with another one')
        if check_asset(asset) == True: # if the asset already exists
            change_amount(asset)
            asset_balance(asset)
            write_date(asset)
            write_time(asset)
        elif check_asset(asset) == False: # if the asset doesn't exists
            write_data(1,asset)
    elif option == str(2):
        delete_asset()
    elif option == str(3):
        print_portfolio()
    elif option == str(4):
        refresh_prices()
    elif option == str(5):
        print('')
        print('Thank you for using this not so well made Python Portfolio')
        print('Byebye')
        print('')
        return
    else:
        print('\nYou did not choose a correct option, try again\n')
    choice()

# Delete Asset
def delete_asset():
    while True:
        asset = str(input('\nInsert the asset you want to delete from this portfolio: ')).upper()
        try:
            cryptocompare.get_price([asset],['USD'])[asset]['USD']
            break
        except TypeError:
            print('')
            print('The token you are writing couldnt be found, try with another one.')
    check = check_asset(asset)
    if check == False:
        print(str(asset) + " is not in the portfolio")
        print('Do you want to add it?')
        option = str(input('If Yes, write "1".\nIf No, write "2"\nOption: '))
        if option == str(1):
            write_data(1,asset)
        elif option == str(2):
            return
        else:
            print('\nYou did not choose a correct option, try again\n')
    elif check == True:
        workbook.create_sheet('Deleted_sheet')
        sheet1 = workbook['Cryptofolio']
        sheet2 = workbook['Deleted_sheet']
        for rows in range (1 , sheet1.max_row + 1):
            if sheet1.cell(row = rows, column = 1).value != asset:
                for i in range (1,sheet1.max_column + 1):
                    sheet2.cell(row = rows, column = i).value = sheet1.cell(row = rows, column = i).value
                for rows in range (1,sheet2.max_row + 1 ):
                    if sheet2.cell(row = rows, column = 1).value == None:
                        sheet2. delete_rows(rows)
        sheet1.title = 'Deleted_sheet1'
        sheet2.title = 'Cryptofolio'
        del workbook['Deleted_sheet1']
        workbook.active = workbook['Cryptofolio']
    print(str (asset) + ' was successfully deleted from the portfolio.')
    formatting()

# Check if Asset is already in file
def check_asset(data):
    bandera = None
    for rows in range (2 , workbook.active.max_row + 1):
        if workbook.active.cell(row = rows, column = 1).value == data:
            print(str(data) + ' is already in the Portfolio\n')
            bandera = True
    if bandera == True:
        return True
    else:
        return False

# Write assets
def write_data(columns, data):
    for rows in range (2 , workbook.active.max_row +  2):
        if workbook.active.cell(row = rows, column = columns).value == None:
            cells = workbook.active.cell(row = rows, column = columns)
            cells.value = data
            print(str(data) + ' added to the portfolio\n')
            write_asset_price(data)
            amount_input(data)
            asset_balance(data)
            write_date(data)
            write_time(data)

# Write asset prices
def write_asset_price(data):
    for rows in range (2 , workbook.active.max_row + 1):
        if workbook.active.cell(row = rows, column = 1).value == data:
            cells = workbook.active.cell(row = rows, column = 2)
            cells.value = cryptocompare.get_price([data],['USD'])[data]['USD']

# User inputs amount of asset
def amount_input(data):
    for rows in range (2 , workbook.active.max_row + 1):
        if workbook.active.cell(row = rows, column = 1).value == data:
            amount = float(input('Write the amount of ' + str(data) + ' that you own: '))
            cells = workbook.active.cell(row = rows, column = 3)
            cells.value = amount

# Individual Asset Balance Calculation
def asset_balance(data):
    for rows in range (2 , workbook.active.max_row + 1):
        if workbook.active.cell(row = rows, column = 1).value == data:
            price = workbook.active.cell(row = rows, column= 2).value
            amount = workbook.active.cell(row = rows, column= 3).value
            balance = price * amount
            cells = workbook.active.cell(row = rows, column = 4)
            cells.value = balance

# To change amount
def change_amount(data):
    print('Do you want to add or substract ' + str(data) + '?')
    option = int(input('If Yes, write "1".\nIf No, write "2"\nOption: '))
    if option == 1:
        for rows in range (2 , workbook.active.max_row+1):
            if workbook.active.cell(row = rows, column = 1).value == data:
                current_amount = workbook.active.cell(row = rows, column = 3).value
                new_amount = float(input('Write the amount of ' + str(data) + ' that you want to add: '))
                cells = workbook.active.cell(row = rows, column = 3)
                cells.value = new_amount + float(current_amount)
    if option == 2:
        return

# Writes date
def write_date(data):
    for rows in range (2 , workbook.active.max_row + 1):
        if workbook.active.cell(row = rows, column = 1).value == data:
            workbook.active.cell(row = rows, column = 5).value = datetime.datetime.now().strftime("%d/%m/%y") # Date

# Writes time
def write_time(data):
    for rows in range (2 , workbook.active.max_row + 1):
        if workbook.active.cell(row = rows, column = 1).value == data:
            workbook.active.cell(row = rows, column = 6).value = datetime.datetime.now().strftime("%X") # Time

# Funtion to print portfolio
def print_portfolio():
    print("\n")
    for i in range (0,105):
        print(end='-')
    print("")
    for row in workbook.active.rows:
        for cell in row:
            filled_space = 20 - len(str(cell.value))
            for i in range (1,filled_space):
                if i == 1:
                    print(cell.value,end=" ")
                if i > 1:
                    print(end=" ")
        print('')
    for i in range (0,105):
        print(end='-')
    print("\n")

# Funtion refresh prices
def refresh_prices():
    for rows in range (2 , workbook.active.max_row + 1):
        if workbook.active.cell(row = rows, column = 1).value != None:
            asset_name = workbook.active.cell(row = rows, column = 1).value
            cells = workbook.active.cell(row = rows, column = 2)
            cells.value = cryptocompare.get_price([asset_name],['USD'])[asset_name]['USD']

