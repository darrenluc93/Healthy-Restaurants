# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
import pandas as pd

#Make sure to run the NutrientsConverter in the Jupyter Notebook folder to be able to call the DataFrames Stored. 
#DataFrames with the combine info.

get_ipython().run_line_magic('store', '-r maleInfo')

get_ipython().run_line_magic('store', '-r femaleInfo')

get_ipython().run_line_magic('store', '-r foodFiltered_df')


# %%
maleInfo[0].iloc[0,0]


# %%
#Males --------

#Gives points to each of the restaurants based on parameters for each of the age groups and lifestyles

#Creates a list to store DataFrames
maleMerged_df = []

for i in range(len(maleInfo)): #for 1 to 3

    #Empty list to store dictionaries for each row iteration.
    dictStore_list = [] 

    for index, row in maleInfo[i].iterrows(): #For each index and row in dataframe maleinfo[i]
        
        #Creates empy dictionary for each iteration. 
        restaurantTally_dict = {} 

        for food in range(len(foodFiltered_df)): #for each row in maleinfo[i] iterates through the restaurant data set and gives points to each restaurant based on the parameters.
            
            if foodFiltered_df.loc[food,'Restaurant'] not in restaurantTally_dict.keys():
                restaurantTally_dict[foodFiltered_df.loc[food,'Restaurant']] = 0 
            
            goodNutritionCounter = 0
                
            #If food calores is lower than the per meal calculatued total, then analyze.
            if (foodFiltered_df.loc[food,'Calories'] <= row['Calories per Meal']):
                goodNutritionCounter += 1
        
            if  ((row['Protein (Cal)'] - (0.045 * maleInfo[i].iloc[index,0]) <= foodFiltered_df.iloc[food,'Protein (Cal)']) & ((row['Protein (Cal)'] + 0.045) >= foodFiltered_df.loc[food,'Protein (Cal)']) : # 
                goodNutritionCounter += 1  

            if  ((row['Carbohydrate (Cal)'] + 0.075) >= foodFiltered_df.loc[food,'Carbohydrate (Cal)']): #((row['Carbohydrate (Cal)'] - 0.075) <= foodFiltered_df.loc[food,'Carbohydrate (Cal)']) &
                goodNutritionCounter += 1  
                
            if ((row['Fiber (gr)'] + 11) > foodFiltered_df.loc[food,'Fiber (gr)']): #((row['Fiber (gr)'] - 11) <= foodFiltered_df.loc[food,'Fiber (gr)']) & 
                goodNutritionCounter += 1
            

            if (foodFiltered_df.loc[food,'Total Sugar (Cal)'] <= row['Total Sugar (Cal)']):
                goodNutritionCounter += 1

            if  ((row['Total lipid (Cal)'] + 2) >= foodFiltered_df.loc[food,'Total Fat (Cal)']): #((row['Total lipid (Cal)'] - 2) <= foodFiltered_df.loc[food,'Total Fat (Cal)']) &
                goodNutritionCounter += 1

            if (foodFiltered_df.loc[food,'Total Trans Fat (Cal)'] < row['Total Trans Fat (Cal)']):
                goodNutritionCounter += 1

            if (foodFiltered_df.loc[food,'Total Saturated Fat (Cal)'] <= row['Total Saturated Fat (Cal)']):
                goodNutritionCounter += 1

            if (foodFiltered_df.loc[food,'Cholesterol (mg)'] < row['Cholesterol (mg)']):
                goodNutritionCounter += 1

            if ((row['Calcium (mg)'] + 252.5)  > foodFiltered_df.loc[food,'Calcium (mg)']): #((row['Calcium (mg)'] - 252.5)  <= foodFiltered_df.loc[food,'Calcium (mg)']) & 
                goodNutritionCounter += 1

            if  ((row['Iron (mg)'] + 5) > foodFiltered_df.loc[food,'Iron (mg)']): #((row['Iron (mg)'] - 5) <= foodFiltered_df.loc[food,'Iron (mg)']) &
                goodNutritionCounter += 1

            if  ((row['Sodium, (mg)'] + 310) > foodFiltered_df.loc[food,'Sodium (mg)']): #((row['Sodium, (mg)'] - 310) <= foodFiltered_df.loc[food,'Sodium (mg)']) &
                goodNutritionCounter += 1
             
            if ((row['Vitamin A (mcg RAE)'] + 615) > foodFiltered_df.loc[food,'Vitamin A (mcg RAE)']): #((row['Vitamin A (mcg RAE)'] - 615) <= foodFiltered_df.loc[food,'Vitamin A (mcg RAE)']) &
                goodNutritionCounter += 1

            if (foodFiltered_df.loc[food,'Vitamin C (mg)'] <= row['Vitamin C (mg)']):
                goodNutritionCounter += 1
            
            if  (goodNutritionCounter == 14): 

                #Only count if the restaruant meets the min conditions or at least 9 combined conditions.
                restaurantTally_dict[foodFiltered_df.loc[food,'Restaurant']] += (1 / foodFiltered_df['Restaurant'].value_counts()[foodFiltered_df.loc[food,'Restaurant']])
                

        #When code is done iterating the data set, append the dictionary to empty list. 
        dictStore_list.append(restaurantTally_dict)
    
    #When code is done iterating trough the maleinfo[i] dataframe, mergues the maleinfo[i] dataframe and create a dataframe from the dictionary list and append both DataFrames using the index of both DataFrames.
    maleMerged_df.append((pd.merge(maleInfo[i], pd.DataFrame(dictStore_list), left_index = True, right_index = True)))

maleMerged_df[0]#.iloc[:,15:]


# %%
maleMerged_df[0].iloc[:,15:]


# %%
#drops empty columns for each dataFrame 
for i in range(len(maleMerged_df)):

    #sorts columns based on average
    columnOrder = (maleMerged_df[i].iloc[0,:15].index).to_list() + (maleMerged_df[i].iloc[:,15:].mean().sort_values(ascending = False).index).to_list()
    #Re orders columns
    maleMerged_df[i] = maleMerged_df[i][columnOrder]
    #Drops columns with values =0
    maleMerged_df[i] = maleMerged_df[i].loc[:,(maleMerged_df[i]!= 0).any(axis=0)]
    #Transpose the data.
    maleMerged_df[i] = maleMerged_df[i].T

    #printsCSV
    maleMerged_df[i].to_csv(f'male{i}.csv')


# %%
#Females --------

#Gives points to each of the restaurants based on parameters for each of the age groups and lifestyles

#Creates a list to store DataFrames
femaleMerged_df = []

for i in range(len(femaleInfo)): #for 1 to 3

    #Empty list to store dictionaries for each row iteration.
    dictStore_list = [] 

    for index, row in femaleInfo[i].iterrows(): #For each index and row in dataframe maleinfo[i]
        
        #Creates empy dictionary for each iteration. 
        restaurantTally_dict = {} 

        for food in range(len(foodFiltered_df)): #for each row in maleinfo[i] iterates through the restaurant data set and gives points to each restaurant based on the parameters.
            
            if foodFiltered_df.loc[food,'Restaurant'] not in restaurantTally_dict.keys():
                restaurantTally_dict[foodFiltered_df.loc[food,'Restaurant']] = 0 

            goodNutritionCounter = 0

            #If food calores is lower than the per meal calculatued total, then analyze.
            if (foodFiltered_df.loc[food,'Calories'] <= row['Calories per Meal']):
                goodNutritionCounter += 1
        
            if  ((row['Protein (Cal)'] + 0.045) >= foodFiltered_df.loc[food,'Protein (Cal)']) : #((row['Protein (Cal)'] - 0.045) <= foodFiltered_df.loc[food,'Protein (Cal)']) &
                goodNutritionCounter += 1
                #proteinCheck = True        

            if  ((row['Carbohydrate (Cal)'] + 0.075) >= foodFiltered_df.loc[food,'Carbohydrate (Cal)']): #((row['Carbohydrate (Cal)'] - 0.075) <= foodFiltered_df.loc[food,'Carbohydrate (Cal)']) &
                goodNutritionCounter += 1
                #carbCheck = True      
                
            if ((row['Fiber (gr)'] + 11) > foodFiltered_df.loc[food,'Fiber (gr)']): #((row['Fiber (gr)'] - 11) <= foodFiltered_df.loc[food,'Fiber (gr)']) & 
                goodNutritionCounter += 1
                #fiberCheck = True

            if (foodFiltered_df.loc[food,'Total Sugar (Cal)'] <= row['Total Sugar (Cal)']):
                goodNutritionCounter += 1
                #sugarsCheck = True

            if  ((row['Total lipid (Cal)'] + 2) >= foodFiltered_df.loc[food,'Total Fat (Cal)']): #((row['Total lipid (Cal)'] - 2) <= foodFiltered_df.loc[food,'Total Fat (Cal)']) &
                goodNutritionCounter += 1
                #fatCheck = True

            if (foodFiltered_df.loc[food,'Total Trans Fat (Cal)'] < row['Total Trans Fat (Cal)']):
                goodNutritionCounter += 1

            if (foodFiltered_df.loc[food,'Total Saturated Fat (Cal)'] <= row['Total Saturated Fat (Cal)']):
                goodNutritionCounter += 1
                #satfatCheck = True

            if (foodFiltered_df.loc[food,'Cholesterol (mg)'] < row['Cholesterol (mg)']):
                goodNutritionCounter += 1

            if ((row['Calcium (mg)'] + 252.5)  > foodFiltered_df.loc[food,'Calcium (mg)']): #((row['Calcium (mg)'] - 252.5)  <= foodFiltered_df.loc[food,'Calcium (mg)']) & 
                goodNutritionCounter += 1

            if  ((row['Iron (mg)'] + 5) > foodFiltered_df.loc[food,'Iron (mg)']): #((row['Iron (mg)'] - 5) <= foodFiltered_df.loc[food,'Iron (mg)']) &
                goodNutritionCounter += 1

            if  ((row['Sodium, (mg)'] + 310) > foodFiltered_df.loc[food,'Sodium (mg)']): #((row['Sodium, (mg)'] - 310) <= foodFiltered_df.loc[food,'Sodium (mg)']) &
                goodNutritionCounter += 1
                #sodiumCheck = True

            if ((row['Vitamin A (mcg RAE)'] + 615) > foodFiltered_df.loc[food,'Vitamin A (mcg RAE)']): #((row['Vitamin A (mcg RAE)'] - 615) <= foodFiltered_df.loc[food,'Vitamin A (mcg RAE)']) &
                goodNutritionCounter += 1

            if (foodFiltered_df.loc[food,'Vitamin C (mg)'] <= row['Vitamin C (mg)']):
                goodNutritionCounter += 1
            
            if  (goodNutritionCounter == 14): 

                #Only count if the restaruant meets all conditions.
                restaurantTally_dict[foodFiltered_df.loc[food,'Restaurant']] += (1 / foodFiltered_df['Restaurant'].value_counts()[foodFiltered_df.loc[food,'Restaurant']])

        #When code is done iterating the data set, append the dictionary to empty list. 
        dictStore_list.append(restaurantTally_dict)
    
    #When code is done iterating trough the maleinfo[i] dataframe, mergues the maleinfo[i] dataframe and create a dataframe from the dictionary list and append both DataFrames using the index of both DataFrames.
    femaleMerged_df.append((pd.merge(femaleInfo[i], pd.DataFrame(dictStore_list), left_index = True, right_index = True)))


femaleMerged_df[0].head()


# %%
#drops empty columns for each dataFrame 
for i in range(len(femaleMerged_df)):

    #sorts columns based on average
    columnOrder = (femaleMerged_df[i].iloc[0,:15].index).to_list() + (femaleMerged_df[i].iloc[:,15:].mean().sort_values(ascending = False).index).to_list()
    #Re orders columns
    femaleMerged_df[i] = femaleMerged_df[i][columnOrder]
    #Drops columns = 0
    femaleMerged_df[i] = femaleMerged_df[i].loc[:,(femaleMerged_df[i]!= 0).any(axis=0)] 
    #Transpose Data
    femaleMerged_df[i] = femaleMerged_df[i].T
    #printsCSV
    femaleMerged_df[i].to_csv(f'female{i}.csv')


# %%
get_ipython().run_line_magic('store', 'femaleMerged_df')

get_ipython().run_line_magic('store', 'maleMerged_df')


# %%


