import json
import os
from datetime import datetime


#USSD codes list initialisation
codes = ["#144#", "#123#"]
code_pin = 2098
transfer_amount_dict = {}
transfer_details = {}
transfer_list = []



def retrieve_json_file():
    """Retrieving balance state"""

    if os.path.exists("balance.json"):
        with open("balance.json", "r") as file:
            content = file.read()
            return json.loads(content)
    else:
         return {"solde": 10000}


#Money balance initialistion
balance = retrieve_json_file()


def update_json_file():
    """ Dumping datas to balance.json file"""

    with open("balance.json", "w") as file:
        json.dump(balance,file)



def show_main_menu():
        """Show the menu according to the ussd code"""

        if ussd_code == "#144#":
            print("**Welcome to the OM menu \n" \
            "1. Balance\n"
            "2. Buy credit\n"
            "3. Transfer money\n" \
            "4. Withdrawal\n"
            "0. Exit")
        else:
            print("Invalid code")
            exit()
        

def show_sub_menu(ussd_code, option):
    """Show submenu according to ussd code entered"""
    
    if ussd_code == "#144#":
        match option:
            case 1:
                print("****Balance services****\n" \
                "1. Orange Money balance\n" \
                "2. My savings\n" \
                "3. International transfer\n" \
                "0. Exit\n"
                "9. Back to the main menu\n")
            case 2:
                print("****Credit services****\n" \
                "1. For myself\n" \
                "2. For another Orange tel\n" \
                "3. International transfer\n" \
                "0. Exit\n" \
                "9. Back to the main menu\n")
            case 3:
                print("****Welcome to the money transfering menu****\n" \
                "1. National transfer\n" \
                "2. International transfer\n" \
                "3. Undo last transfer\n"
                "4. Historic"
                "0. Exit\n" \
                "9. Back to the main menu\n")
            case 4:
                print("****Withdrawal menu****\n" \
                "1. Pass 100 Mo - 500 \n" \
                "2. Pass 500 Mo - 1000\n" \
                "3. Pass 1Go - 2000\n" \
                "0. Exit\n" \
                "9. Back to the main menu\n")
            case 0:
                exit()
            case 9:
                show_main_menu()
            



def show_menu_according_option(option, sub_option) :
    """Show menu according to the option"""
    if option == 1:
        match sub_option:
            case 1:
                with open("balance.json", "r") as file:
                    content_string = file.read()
                    content = json.loads(content_string)
                print(f"Balance : {content["solde"]}")
                update_json_file()
            case 9:
                show_sub_menu(ussd_code, option)
            case 0:
                exit()

    elif option == 2:
        match sub_option:
            case 1:
                try:
                    credit_amount = int(input("How much would you like to buy for credit ? Amount : "))
                    with open("balance.json", "r") as file:
                        content_string = file.read()
                        content = json.loads(content_string)
                    if balance["solde"] >= credit_amount:
                        balance["solde"] -= credit_amount
                        print(f"Success ! Balance : {balance["solde"]}")
                        update_json_file()
                    else :
                        print("Failed ! Not enough balance. Please recharge ! ")
                except TypeError:
                    print("Invalid amount")
                    show_menu_according_option(option, sub_option)
                
    elif option == 3:
        match sub_option:
            case 1:
                    number_call_entered = input("Please enter the number that you would like to send money\n Tel : ")
                    number_call_filtered = number_call_entered.strip()
                    print(number_call_filtered)
                    if (len(number_call_filtered) == 9) & number_call_filtered.startswith("7"):
                        while True:
                            try:
                                amount = int(input("Please enter the amount : "))
                                with open("balance.json", "r") as file:
                                    content_string = file.read()
                                    content = json.loads(content_string)
                                if balance["solde"] >= amount :
                                    secret_code = int(input("Please enter your secret code\n"))
                                    if secret_code == code_pin:
                                        date = str(datetime.now())
                                        balance["solde"] -= amount
                                        transfer_amount_dict[balance["solde"]] = amount
                                        print(transfer_amount_dict)
                                        transfer_details["amount"] = amount
                                        transfer_details["receiver"] = number_call_filtered
                                        transfer_details["datetime"] = date
                                        transfer_list.append(transfer_details)
                                        print(f"Transfer done to {number_call_filtered}\n")
                                        update_json_file()
                                        try:
                                            with open("transfer_historic.json", "w") as file:
                                                json.dump(transfer_list,file)
                                        except json.JSONDecodeError:
                                             print("Json Decodage error")
                                        except IOError:
                                            print("IO error")
                                        except Exception as e:
                                             print(f"This error occurs {e}")
                                                  

                                    else:
                                        print("Incorrect pin. Try Again")
                                        
                                else:
                                    print("Transfer failed ! Your balance is not enough ! ")
                            except (TypeError, ValueError):
                                print("Invalid amount")
                            break;
                    else:
                        while True:
                            print("Invalid number call.")
                            number_call_entered = input("Please enter the number that you would like to send money\n Tel : ")

            case 3:
                undo_confirm() 
            case 4:
                retrieve_transfer_historic()
        

    elif option == 4:
        with open("balance.json", "r") as file:
                    content_string = file.read()
                    content = json.loads(content_string)
        match sub_option:
            
            case 1:
                if balance["solde"] >= 500:
                    print(f"Success ! Balance : {balance["solde"] - 500}")
                    update_json_file()

                else:
                    print("Not enough balance!")
            case 2:
                if balance["solde"] >= 1000:
                    print(f"Success ! Balance : {balance["solde"] - 1000}")
                    update_json_file()

                else:
                    print("Not enough")
            case 3: 
                if balance["solde"] >= 2000:
                    print(f"Success ! Balance : {balance["solde"] - 2000}")
                    update_json_file()

                else:
                    print("Not enough")


#Undo or confirm transfer option
def undo_confirm():
            with open("balance.json", "r") as file:
                    content_string = file.read()
                    content = json.loads(content_string)
            option = int(input("Undo the last transfer. Press 1 to undo it :"))
            if option == 1 and len(transfer_amount_dict) != 0 :
                    last_transfer = list(transfer_amount_dict.keys())[-1]
                    last_transfer_value = list(transfer_amount_dict.values())[-1]
                    balance["solde"] = last_transfer+last_transfer_value
                    print(f"Undo ! Balance = {balance["solde"]}")
                    update_json_file()

            else: 
                    print("Invalid")
                    show_main_menu()

                
def retrieve_transfer_historic():
    """Shows transfer historic"""
    try:
        if os.path.exists("transfer_historic.json"):
            with open("transfer_historic.json", "r") as file:
                content = file.read()
                content_str = json.loads(content)
        print("====HISTORIC====\n")
        for i in content_str:
                print(f"{i}\n")
                print(f"{i}\n")
                print(f"{i}\n")
                
    except json.JSONDecodeError:
        print("Json Decodage error")
    except IOError:
        print("IO error")
    except Exception as e:
        print(f"This error occurs {e}")   


    


#Main program
while True :
    while True:
        ussd_code = input("\nIf you want to exit press 0. Please enter a valid ussd_code : ")
        show_main_menu()

        while ussd_code not in codes:
            ussd_code = input("\nIncorrect. If you want to exit press 0. \nPlease enter a valid ussd_code : ")
            show_main_menu()
        break


    while True:
        try:
            option = int(input("\nPlease choose an option : "))
            show_sub_menu(ussd_code, option)
            break
        except (ValueError, TypeError):
            print("Please enter a valid option. It must be a number")
            show_main_menu()
            show_sub_menu(ussd_code, option)



    

    while True:
        try:
            sub_option = int(input("\n Please choose an option : "))
            show_menu_according_option(option, sub_option)
            break
        except (ValueError, TypeError):
            print("Please enter a valid option")
            show_menu_according_option(option, sub_option)
                                                                                                                                                                                                                          




