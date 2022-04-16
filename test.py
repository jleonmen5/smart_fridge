import pandas as pd

#####THIS NEEDS TO BECOME FUNCTION INPUTS####
min_carb_intake = 10
max_carb_intake = 200
food_path = 'MyFoodData.csv'
#############################################
TARGET_AVERAGE_RANK = 8

if min_carb_intake < 0 or min_carb_intake > 300:
    raise ValueError(f"Invalid min carbohydrate intake: {min_carb_intake}")

if max_carb_intake < 0 or max_carb_intake > 300 or max_carb_intake < min_carb_intake:
    raise ValueError(f"Invalid max carbohydrate intake: {max_carb_intake}")


#############################################

def prepare_fridge(food_path):
    FRIDGE_ITEMS = 7
    food_data = pd.read_csv(food_path, header=0)
    fridge = food_data.sample(n=FRIDGE_ITEMS, replace=False, ignore_index=True)
    empty_fridge = pd.DataFrame(columns=list(fridge), index=[0])
    fridge = pd.concat([empty_fridge, fridge], ignore_index=True)
    return fridge


def check_valid_menu(proposed_menu):
    proposed_menu.drop_duplicates()
    total_carbs_check = min_carb_intake <= proposed_menu.loc[:, 'Carbohydrate'].sum() <= max_carb_intake
    total_item_check = 2 <= proposed_menu.loc[:, 'Carbohydrate'].count() <= 4
    average_rank_check = proposed_menu.loc[:, 'Ranking'].mean() >= 8
    contains_beverage = not proposed_menu[proposed_menu.isin(['Beverages'])].dropna(how='all').empty
    return (total_carbs_check and total_item_check and
            average_rank_check and contains_beverage)


menu = pd.DataFrame()


def meal_recommendation(menu, fridge):
    if not fridge[fridge.isin(['Beverages'])].dropna(how='all').empty:
        return print("no valid menu because there are no drinks")
    for i in range(fridge.shape[0]):
        menu = pd.concat([menu, fridge.iloc[[i]]], ignore_index=True)
        for i2 in range(fridge.shape[0]):
            menu = pd.concat([menu, fridge.iloc[[i2]]], ignore_index=True)
            for i3 in range(fridge.shape[0]):
                menu = pd.concat([menu, fridge.iloc[[i3]]], ignore_index=True)
                for i4 in range(fridge.shape[0]):
                    menu = pd.concat([menu, fridge.iloc[[i4]]], ignore_index=True)
                    if check_valid_menu(menu):
                        return print(menu)
                    menu.drop([3], inplace=True)
                menu.drop([2], inplace=True)
            menu.drop([1], inplace=True)
        menu.drop([0], inplace=True)
    else:
        return print("No valid Menu")


fridge = prepare_fridge(food_path)
meal_recommendation(menu, fridge)