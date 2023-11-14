#libraries
import pandas as pd 
import csv

#global variables
modals = ["ON", "HY", "IN"]
#main script
def main():
    
    # create dataframes
    raw_data = pd.read_csv(".\Transfer_cleaned.csv")
    
    list_151 = raw_data.loc[raw_data["CourseName"] == 151]
    list_152 = raw_data.loc[raw_data["CourseName"] == 152]
    list_251 = raw_data.loc[raw_data["CourseName"] == 251]
    list_252 = raw_data.loc[raw_data["CourseName"] == 252]
    
    #clear PII from individual dataframes and create a student registry
    
    student_profiles = raw_data.loc[:, ["Student", "Gender", "Ethnicity", "EHI"]]
    student_profiles.drop_duplicates(inplace = True)
    student_profiles.to_csv("Demographics.csv")
    
    list_151 = PII_scrubber(list_151)
    list_152 = PII_scrubber(list_152)
    list_251 = PII_scrubber(list_251)
    list_252 = PII_scrubber(list_252)
    
    #saves submatrices for PowerBI
    list_151.to_csv("151.csv")
    list_152.to_csv("152.csv")
    list_251.to_csv("251.csv")
    list_252.to_csv("252.csv")
    
    #builds up overlap matrix
    list151_152 = list_151.merge(list_152, left_on = "Student", right_on = "Student", suffixes = ("_x", "_y"))
    list151_152_2 = list151_152.merge(student_profiles, left_on = "Student", right_on = "Student", suffixes = (False, False))
    list151_152_2.drop_duplicates(inplace = True)
    list151_152_2.to_csv("151_152demo.csv")
    
    list152_251 = list_152.merge(list_251, left_on = "Student", right_on = "Student", suffixes = ("_x", "_y"))
    list152_251_2 = list152_251.merge(student_profiles, left_on = "Student", right_on = "Student", suffixes = (False, False))
    list152_251_2.to_csv("152_251demo.csv")
    list152_251_2.drop_duplicates(inplace = True)
    
    list251_252 = list_251.merge(list_252, left_on = "Student", right_on = "Student", suffixes = ("_x", "_y"))
    list251_252_2 = list251_252.merge(student_profiles, left_on = "Student", right_on = "Student", suffixes = (False, False))
    list251_252_2.to_csv("251_252demo.csv")
    list251_252_2.drop_duplicates(inplace = True)
    
    #builds up transfer matrix
    T151_152 = TMatrix(list151_152_2)
    N151_152 = NTMatrix(T151_152)
    T152_251 = TMatrix(list152_251_2)
    N152_251 = NTMatrix(T152_251)
    T251_252 = TMatrix(list251_252_2)
    N251_252 = NTMatrix(T251_252)
    
    matrices = [T151_152, N151_152, T152_251, N152_251, T251_252, N251_252]
    names = ["T151_152.csv", "N151_152.csv", "T152_251.csv", "N152_251.csv", "T251_252.csv", "N251_252.csv"]
    
    #saves the transfer matrices
    for i in range(0, len(matrices) - 1):
        SaveTMat(matrices[i], names[i])
    
    return 
       
#define functions
#drop demographics from list
def PII_scrubber(df):
    df = df.loc[:, ["Student", "Year", "Term", "YearTerm", "Campus", "Modality"]]
    return df

#creates transfer matrix
def TMatrix(df):
    Tmat = [["ON", 0, 0, 0], ["HY", 0, 0, 0], ["IN", 0, 0 ,0]]
    for i in range(0, 3):
        for j in range(0, 3):
            Tmat[i][j + 1] = len(df[(df["Modality_x"] == modals[i]) & (df["Modality_y"] == modals[j])])
    return Tmat

#noralizes a transfer matrix
def NTMatrix(Tmat):
    for i in range(0, 3):
        N = Tmat[i][1] + Tmat[i][2] + Tmat[i][3]
        if N == 0:
            for j in range(0, 3):
                Tmat[i][j + 1] = 0
        else:
            for j in range(0, 3):
                Tmat[i][j + 1] = Tmat[i][j + 1] / N
    return Tmat

#Saves matrix
def SaveTMat(Tmat, name):
    dftemp = pd.DataFrame(Tmat, columns = ["Modality", "ON", "HY", "IN"])
    dftemp.to_csv(name)    
    return 

main()
