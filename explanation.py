import re
import numpy as np
import pandas as pd
from IPython.display import Image, display
from datetime import date as datefunc

# Specify data paths below
general = pd.read_csv("xcbr-challenge/Data/weatherdata.csv")
ig = pd.read_csv("xcbr-challenge/Data/input_attributions_ig.csv")

TEMP_MAX = np.average(general["TEMP_MAX"])
TEMP_MIN = np.average(general["TEMP_MIN"])
TEMP_MAX = np.average(general["TEMP_MAX"])
temp_range = [TEMP_MIN,TEMP_MAX]
PRES_AVG = np.average(general["PRES_AVG"])
PRES_MAX = np.average(general["PRES_MAX"])
PRES_MIN = np.average(general["PRES_MIN"])
pres_range = [PRES_MIN,PRES_MAX]
HUM_AVG = np.average(general["HUM_AVG"])
HUM_MAX = np.average(general["HUM_MAX"])
HUM_MIN = np.average(general["HUM_MIN"])
hum_range = [HUM_MIN, HUM_MAX]

feats = []
for i in range(14):
  i = i+1
  HUM_MIN = "HUM_MIN"
  HUM_AVG = "HUM_AVG"
  HUM_MAX = "HUM_MAX"
  PRES_MIN = "PRES_MIN"
  PRES_AVG = "PRES_AVG"
  PRES_MAX = "PRES_MAX"
  feats.append(f"{HUM_MIN}_Day_{i}")
  feats.append(f"{HUM_AVG}_Day_{i}")
  feats.append(f"{HUM_MAX}_Day_{i}")
  feats.append(f"{PRES_MIN}_Day_{i}")
  feats.append(f"{PRES_AVG}_Day_{i}")
  feats.append(f"{PRES_MAX}_Day_{i}")

cols = ig.columns
ig.columns = feats

HOT = Image('/content/hot.png', width=60)
WARM = Image('/content/warm.png', width=60)
MILD = Image('/content/mild.png', width=60)
COLD = Image('/content/cold.png', width=60)

def display_thermometer(temperature):
  if temperature >=25:
    display(HOT)
  elif temperature >=15 and temperature <25:
    display(WARM)
  elif temperature >=1 and temperature <15:
    display(MILD)
  elif temperature < 1:
    display(COLD)
  else:
    display(MILD)

def getOrdinal(number):
  if type(number) != type(1):
    try:
      number = int(number)
    except:
      raise ValueError("This number is not an Int!")
  lastdigit = int(str(number)[len(str(number))-1])
  last2 = int(str(number)[len(str(number))-2:])
  if last2 > 10 and last2 < 13:
      return str(number) + "th"
  if lastdigit == 1:
      return str(number) + "st"
  if lastdigit == 2:
      return str(number) + "nd"
  if lastdigit == 3:
      return str(number) + "rd"
  return str(number) + "th"

def humaniseDate(date):
  SPLIT_DATE = date.split('-')
  INTEGER_DATES = list(map(lambda x: int(x), SPLIT_DATE))
  WORD_DATES = datefunc(year=INTEGER_DATES[0], month=INTEGER_DATES[1], day=INTEGER_DATES[2]).strftime('%A %d %B %Y')
  WORD_DATES_SPLIT = WORD_DATES.split(' ')
  WORD_DATES_SPLIT[1] = f"the {getOrdinal(WORD_DATES_SPLIT[1])} of"
  FORMATTED_WORD = " ".join(WORD_DATES_SPLIT)
  return FORMATTED_WORD

def display_emoji(temperature):
  if temperature >=25:
      return '🥵'
  elif temperature >=15 and temperature <25:
      return '😎'
  elif temperature >=0 and temperature <15:
      return '😊'
  elif temperature <1:
      return '🥶'
  else:
      return '😊'

def colour_text(text, temperature):
  if temperature >= 25:
    return f"\x1b[31m{text}\x1b[0m"
  elif temperature >= 1 and temperature < 25:
    return f"\u001b[33m{text}\x1b[0m"
  elif temperature < 1:
    return f"\u001b[34m{text}\x1b[0m"
  else: 
    return text

date_dic = {}
for idx, val in enumerate(general['DATE']):
  date_dic[val] = idx

def contributors(sample_idx):
  feat_dic_14 = {}
  feat_dic_7 = {}
  feat_dic_3 = {}

  lst_14 = ""
  lst_7 = ""
  lst_3 = ""
  final = {}
  for i in ig.columns:
    feat_dic_14[i] = ig[i][sample_idx]
  maxi = max(feat_dic_14.values())

  for i in feat_dic_14:
    if feat_dic_14[i] == maxi:
      lst_14 = i
  for i in ig.columns[-42:]:
    feat_dic_7[i] = ig[i][sample_idx]
  maxi = max(feat_dic_7.values())
  for i in feat_dic_7:
    if feat_dic_7[i] == maxi:
      lst_7 = i

  for i in ig.columns[-18:]:
    feat_dic_3[i] = ig[i][sample_idx]
  maxi = max(feat_dic_3.values())
  for i in feat_dic_3:
    if feat_dic_3[i] == maxi:
      lst_3 = i
  
  final["lst_14"] = lst_14
  final["lst_7"] = lst_7
  final["lst_3"] = lst_3
  return final



def explanation(date): #test date: 2000-01-15

  idx = date_dic[date]
  sample = idx-14
  x = contributors(sample)
  contribs = { 'lst_14': "last 14 days", "lst_7": "last week", "lst_3": "last three days",'HUM_MIN_Day_4':"the minimum humidity on the 4th day",
              'HUM_AVG_Day_4':"the average humidity on the 4th day",'HUM_MAX_Day_4':"the maximum humidity on the 4th day",
              'PRES_MIN_Day_4':"the minimum pressure on the 4th day", 'PRES_AVG_Day_4':"the average pressure on the 4th day",
              'PRES_MAX_Day_4':"the maximum pressure on the 4th day",'HUM_MIN_Day_5':"the minimum humidity on the 5th day",
              'HUM_AVG_Day_5':"the average humidity on the 5th day", 'HUM_MAX_Day_5':"the maximum humidity on the 5th day",
              'PRES_MIN_Day_5':"the minimum pressure on the 5th day",'PRES_AVG_Day_5':"the average pressure on the 5th day",
              'PRES_MAX_Day_5':"the maximum pressure on the 5th day", 'HUM_MIN_Day_6':"the minimum humidity on the 6th day",
              'HUM_AVG_Day_6':"the average humidity on the 5th day",'HUM_MAX_Day_6':"the maximum humidity on the 6th day",
              'PRES_MIN_Day_6':"the minimum pressure on the 6th day", 'PRES_AVG_Day_6':"the average pressure on the 6th day",
              'PRES_MAX_Day_6':"the maximum pressure on the 6th day",'HUM_MIN_Day_7':"the minimum humidity on the 7th day",
              'HUM_AVG_Day_7':"the average humidity on the 7th day", 'HUM_MAX_Day_7':"the maximum humidity on the 7th day",
              'PRES_MIN_Day_7':"the minimum pressure on the 7th day",'PRES_AVG_Day_7':"the average pressure on the 7th day",
              'PRES_MAX_Day_7':"the maximum pressure on the 7th day", 'HUM_MIN_Day_8':"the minimum humidity on the 8th day",
              'HUM_AVG_Day_8':"the average humidity on the 8th day",'HUM_MAX_Day_8':"the maximum humidity on the 8th day",
              'PRES_MIN_Day_8':"the minimum pressure on the 8th day", 'PRES_AVG_Day_8':"the average pressure on the 8th day",
              'PRES_MAX_Day_8':"the maximum pressure on the 8th day",'HUM_MIN_Day_9':"the minimum humidity on the 9th day",
              'HUM_AVG_Day_9':"the average humidity on the 9th day", 'HUM_MAX_Day_9':"the maximum humidity on the 9th day",
              'PRES_MIN_Day_9':"the minimum pressure on the 9th day",'PRES_AVG_Day_9':"the average pressure on the 9th day",
              'PRES_MAX_Day_9':"the maximum pressure on the 9th day", 'HUM_MIN_Day_10':"the minimum humidity on the 10th day",
              'HUM_AVG_Day_10':"the average humidity on the 10th day",'HUM_MAX_Day_10':"the maximum humidity on the 10th day",
              'PRES_MIN_Day_10':"the minimum pressure on the 10th day", 'PRES_AVG_Day_10':"the average pressure on the 10th day",
              'PRES_MAX_Day_10':"the maximum pressure on the 10th day", 'HUM_MIN_Day_11':"the minimum humidity on the 11th day",
              'HUM_AVG_Day_11':"the average humidity on the 11th day", 'HUM_MAX_Day_11':"the maximum humidity on the 11th day",
              'PRES_MIN_Day_11':"the minimum pressure on the 11th day", 'PRES_AVG_Day_11':"the average pressure on the 11th day",
              'PRES_MAX_Day_11':"the maximum pressure on the 11th day",'HUM_MIN_Day_12':"the minimum humidity on the 12th day",
              'HUM_AVG_Day_12':"the average humidity on the 12th day", 'HUM_MAX_Day_12':"the maximum humidity on the 12th day",
              'PRES_MIN_Day_12':"the minimum pressure on the 12th day",'PRES_AVG_Day_12':"the average pressure on the 12th day",
              'PRES_MAX_Day_12':"the maximum pressure on the 12th day", 'HUM_MIN_Day_13':"the minimum humidity on the 13th day",
              'HUM_AVG_Day_13':"the average humidity on the 13th day", 'HUM_MAX_Day_13':"the maximum humidity on the 13th day",
              'PRES_MIN_Day_13':"the minimum pressure on the 13th day",'PRES_AVG_Day_13':"the average pressure on the 13th day",
              'PRES_MAX_Day_13':"the maximum pressure on the 13th day", 'HUM_MIN_Day_14':"the minimum humidity on the 14th day",
              'HUM_AVG_Day_14':"the average humidity on the 14th day", 'HUM_MAX_Day_14':"the maximum humidity on the 14th day",
              'PRES_MIN_Day_14':"the minimum pressure on the 14th day",'PRES_AVG_Day_14':"the average pressure on the 14th day",
              'PRES_MAX_Day_14':"the maximum pressure on the 14th day"}
  #********************** HIGH or LOW for HUM and PRES **********************
  if np.average(general["HUM_AVG"][:idx]) > np.average(hum_range):
    hum_desc = "humidity was high"
  elif np.average(general["HUM_AVG"][:idx]) < np.average(hum_range):
    hum_desc = "humidity was low"

  if np.average(general["PRES_AVG"][:idx]) > np.average(pres_range):
    pres_desc = "pressure was high"
  elif np.average(general["PRES_AVG"][:idx]) < np.average(pres_range):
    pres_desc = "pressure was low"
  #********************** EXTRACTING DATE PERIOD **********************
  date = [] # idx 0: starting date  idx 1: ending date  idx 2: month name
  date.append(str(general['DATE'][0]))
  date.append(str(general['DATE'][idx-1]))
  date.append(general['MONTH'][0])
  temperature = general["TEMP_AVG"][idx]
  BASE = f"The temperature for {humaniseDate(str(general['DATE'][idx]))} is predicted to be {colour_text(str(temperature) + ' degrees', temperature)} {display_emoji(temperature)}. \nThis is because "
  date_desc = f"in the two weeks prior (from {humaniseDate(date[0])} to {humaniseDate(date[1])}) "

  whole_week=int(re.findall('[0-9]+', contribs[x[list(x.keys())[0]]])[0])-1+(idx-14)
  lst_week=int(re.findall('[0-9]+', contribs[x[list(x.keys())[1]]])[0])-1+(idx-14)
  lst_3=int(re.findall('[0-9]+', contribs[x[list(x.keys())[2]]])[0])-1+(idx-14)
  whole_week_day = general["DATE"][whole_week]
  lst_week_day = general["DATE"][lst_week]
  lst_3_day = general["DATE"][lst_3]
  causes_of_temps = f"{hum_desc} and {pres_desc}. \nFurthermore, our system suggests that: \n\t⚫ in the {contribs[list(x.keys())[0]]} the most important feature was {contribs[x[list(x.keys())[0]]]} ({whole_week_day}); \n\t⚫ that in the {contribs[list(x.keys())[1]]} the most important feature was {contribs[x[list(x.keys())[1]]]} ({lst_week_day}); \n\t⚫ and finally in the {contribs[list(x.keys())[2]]} the most important feature was {contribs[x[list(x.keys())[2]]]} ({lst_3_day})."
  final = BASE+date_desc+causes_of_temps
  display_thermometer(temperature)
  print(final)


def main():
    date = input("Please enter a date in the following format: YYYY-MM-DD\n")
    explanation(date)

if __name__ == "__main__":
    main()




