import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pyrankvote
from pyrankvote import Candidate, Ballot
import time

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sh = client.open("SheetName")
sheet = sh.get_worksheet(0) #sheetnumber

A = Candidate("CandA") #1stcandidate
B = Candidate("CandB") #2ndcandidate
C = Candidate("CandC") #3rdcandidate
D = Candidate("CandD") #4thcandidate

dictCandidate = {"A": A, "B":B, "C": C, "D": D} #dictionary to map it

candidates = [A,B,C,D]
def replace(): #replaces all the names in the sheet with letters
    cellsA = sheet.findall("CandA") #you need to change their names here as well as above
    i = 0
    while i < len(cellsA):
        cellsA[i].value = 'A'
        i = i + 1
    sheet.update_cells(cellsA)

    cellsB = sheet.findall("CandB")
    ii = 0
    while ii < len(cellsB):
        cellsB[ii].value = 'B'
        ii = ii + 1
    sheet.update_cells(cellsB)

    cellsC = sheet.findall("CandC")
    j = 0
    while j < len(cellsC):
        cellsC[j].value = 'C'
        j = j + 1
    sheet.update_cells(cellsC)

    cellsD = sheet.findall("CandD")
    jj = 0
    while jj < len(cellsD):
        cellsD[jj].value = 'D'
        jj = jj + 1
    sheet.update_cells(cellsD)
replace() #calls the replacement

data = sheet.get_all_records()
numRows = len(data)


def getCandidates(candidatelist):
    returndict = []
    for candidate in candidatelist:
        returndict.append(dictCandidate[candidate])
    return returndict


ballots = []
def addvote(num):
    ballots.append(Ballot(ranked_candidates = getCandidates(sheet.row_values(num))))

j = 2 
while j <= numRows + 1: #loops through all the rows and adds it to be tabulated
    time.sleep(0.75)
    addvote(j)
    j = j + 1


electIRV = pyrankvote.instant_runoff_voting(candidates, ballots)
winIRV = electIRV.get_winners()
print(electIRV)
                                            #IRV used for one seat
                                            #STV used for multiple, change the 2  below to the amount of seats
                                            #comment/uncomment whichever one you need to use
#electSTV = pyrankvote.single_transferable_vote(candidates,ballots, 2)
#winSTV = electSTV.get_winners()
#print(electSTV)       
