import pandas as pd
import numpy as np
import re

#Cleaning tools fucntions 

def clean_invalid_columns(df):
    df = df.drop(["pdf","href","Source","href formula","Unnamed: 11","Case Number",
         "Case Number.1","original order","Unnamed: 21","Unnamed: 22","Name"], axis =1)
    return df
    
def clean_nan_rows (df):
    
    df.dropna(thresh= 12, inplace=True)
    
    return df

def clean_duplicates(df):
    
    df = df.drop_duplicates()
    
    return df

def rename_species (df):
    
    df.rename(columns = {"Species ": 'Species'}, inplace=True)
    
    return df

def clean_activity(df):
    
    pattern = re.compile("surf", re.IGNORECASE)
    df.Activity = df.Activity.apply(lambda x: "surf" if re.search(pattern, x.lower()) else x)
    pattern = re.compile("swim", re.IGNORECASE)
    df.Activity = df.Activity.apply(lambda x: "swim" if re.search(pattern, x.lower()) else x)
    pattern = re.compile("diving", re.IGNORECASE)
    df.Activity = df.Activity.apply(lambda x: "diving" if re.search(pattern, x.lower()) else x)
    pattern = re.compile("fish", re.IGNORECASE)
    df.Activity = df.Activity.apply(lambda x: "fish" if re.search(pattern, x.lower()) else x)

    return df

def clean_gender (df):
    
    df.Sex = df.Sex.str.replace('lli','M')
    return df

def format_age (age):
        if isinstance(age, int):
            return age
        elif age == np.nan:
            return age
        elif isinstance(age, str):
            numbers = re.findall(r'\d+', age)
            total = 0
            for x in numbers:
                total += int(x)
                if isinstance(numbers[0], int):
                    return (total/len(numbers))
                    
                
        

def cleaning_tool(df):
    df = clean_invalid_columns(df)
    df = clean_nan_rows(df)
    df = clean_duplicates(df)
    df = clean_gender(df)
    df = clean_activity(df)
    df = rename_species(df)
    df.Age = df.Age.apply(format_age)
    df
    return df

def printing_is():
    print("is fun fun fun")
    return 0

def classify_time(time_str):
    # Define default classification
    time_str = str(time_str).strip().lower()
    if "morning" in time_str or "daybreak" in time_str:
        return "Morning"
    elif "afternoon" in time_str or "midday" in time_str or "noon" in time_str:
        return "Afternoon"
    elif "evening" in time_str or "sunset" in time_str:
        return "Evening"
    elif "night" in time_str or "dusk" in time_str or "midnight" in time_str or "dark" in time_str:
        return "Night"
    # Handle times like 14h00, 8:00 pm, etc.
    try:
        if "h" in time_str or ":" in time_str:
            # Convert to 24-hour format
            if "pm" in time_str or "p.m." in time_str:
                time_str = time_str.replace("pm", "").replace("p.m.", "").strip()
                hour = int(time_str.split("h")[0]) + 12
            elif "am" in time_str or "a.m." in time_str:
                time_str = time_str.replace("am", "").replace("a.m.", "").strip()
                hour = int(time_str.split("h")[0])
            else:
                hour = int(time_str.split("h")[0])
            if 5 <= hour < 12:
                return "Morning"
            elif 12 <= hour < 17:
                return "Afternoon"
            elif 17 <= hour < 21:
                return "Evening"
            elif (21 <= hour <= 24) or (0 <= hour < 5):
                return "Night"
    except:
        pass
    # If unable to classify, return NaN
    return np.nan


