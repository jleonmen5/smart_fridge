import pandas as pd
import numpy as np

#####THIS NEEDS TO BECOME FUNCTION INPUTS####
min_carb_intake = 10
max_carb_intake = 200
food_path = 'MyFoodData.csv'
#############################################

def print_menu(menu, fridge):
    for item in menu[:, 0]:
        print(fridge[fridge['ID'] == item])
    print('Total carbohydrates in menu: ', menu[:, 1].sum())

def prepare_fridge(food_path):
    FRIDGE_ITEMS = 30
    food_data = pd.read_csv(food_path, header=0)
    fridge = food_data.sample(n=FRIDGE_ITEMS, replace=False, ignore_index=True)
    fridge = fridge[fridge.Ranking > 1]  # removing items with rank less than 1 because in worst case they wouldn't meet average
    fridge = fridge[fridge.Group != 'Fats and Oils']  # this is an ingredient of foods, no one eats this by itself
    empty_fridge = pd.DataFrame(columns=list(fridge), index=[0])
    fridge = pd.concat([empty_fridge,fridge], ignore_index=True)
    return fridge

def check_valid_menu(proposed_menu):
    if (proposed_menu[:, 2].mean() >= TARGET_AVERAGE_RANK and
            proposed_menu[:, 1].sum() >= min_carb_intake and
            proposed_menu[:, 1].sum() <= max_carb_intake):
        result = True
    else:
        result = False
    return result


def meal_recommendation(min_carb_intake, max_carb_intake):

    if min_carb_intake < 0 or min_carb_intake > 300:
        raise ValueError(f"Invalid min carbohydrate intake: {min_carb_intake}")

    if max_carb_intake < 0 or max_carb_intake > 300 or max_carb_intake < min_carb_intake:
        raise ValueError(f"Invalid max carbohydrate intake: {max_carb_intake}")

    TARGET_AVERAGE_RANK = 8



    fridge = df.sample(n=FRIDGE_ITEMS, replace=False, ignore_index=True)  # taking 30 random items for fridge
    drinks = fridge[(fridge['Group'] == 'Beverages')]  # separating only the beverages
    fridge = fridge.sort_values(by=['Ranking'], ascending=False)  # ensures most preffered menu
    # converting pandas dataframes to numpy arrays that are faster to iterate through
    fridge_n = fridge[['ID', 'Carbohydrate', 'Ranking']].to_numpy()
    drinks_n = drinks[['ID', 'Carbohydrate', 'Ranking']].to_numpy()

    menu = np.zeros((1, 3), dtype='int64')  # initializing an empty menu

    valid_menu = False
    for idx in range(drinks_n.shape[0]):
        if drinks_n.size == 0:
            print('there is no valid menu because there are no drinks')
            break
        else:
            if drinks_n[
                idx, 1] < max_carb_intake and not valid_menu:  # checking if carbs in item are at least smaller than max
                menu[0] = drinks_n[idx]
                for idx2 in range(fridge_n.shape[0]):  # getting menu item #2
                    if fridge_n[idx2, 0] not in menu:
                        proposed_menu = np.vstack((menu, fridge_n[idx2, :]))
                        valid_menu = check_valid_menu(proposed_menu)
                        if valid_menu:
                            menu = proposed_menu
                            print_menu(menu, fridge)
                            break
                        elif total_carbs < min_carb_intake and not valid_menu:  # getting menu item #3
                            for idx3 in range(fridge_n.shape[0]):
                                if fridge_n[idx3, 0] not in menu:
                                    proposed_menu = np.vstack((menu, fridge_n[idx2, :]))
                                    valid_menu = check_valid_menu(proposed_menu)
                                    if valid_menu:
                                        menu = proposed_menu
                                        print_menu(menu, fridge)
                                        break
                                    elif total_carbs < min_carb_intake and not valid_menu:  # getting menu item #4
                                        for idx4 in range(fridge_n.shape[0]):
                                            if fridge_n[idx4, 0] not in menu:
                                                proposed_menu = np.vstack((menu, fridge_n[idx2, :]))
                                                valid_menu = check_valid_menu(proposed_menu)
                                                if valid_menu:
                                                    menu = proposed_menu
                                                    print_menu(menu, fridge)
                                                    break
    if not valid_menu:
        print('there is no valid menu')


# meal_recommendation(50, 70, 'MyFoodData.csv')