intxp=75 ; xp=intxp ; xpsum=intxp ;intlvl=0 ; lvl=intlvl
for i in range(66):
    #print(f"xp needed:{xp}\tlvl:{lvl}\ttotalexp:{xpsum}")
    xp+=100 ; lvl+=1
    xpsum+=xp
#print(xpsum)

levelwanted=int(input("Enter the level which you want to reach:"))-1
currentlevel=int(input("Enter the level you are at currently:"))-1
currentxp=int(input("Enter the amount of xp you currently have:"))
chatperday=eval(input("How many minutes do you chat everyday?:"))
voteboost=input("10% voteboost?y/n:-")

avgxp=30.25 if voteboost=="y" else 27.5
#goal is to calculate the xp needed for a specific level
sumtillcurrent=50*(currentlevel**2)+125*currentlevel+75
sumtillwanted=50*(levelwanted**2)+125*levelwanted+75
xpneeded=sumtillwanted-sumtillcurrent-currentxp
minutesneeded=round(xpneeded/avgxp)
daysneeded=minutesneeded/chatperday ; realistically=1440*daysneeded

print("-"*45)
print(f"You need {xpneeded} xp to reach level {levelwanted+1}\n\nAnd would require about {minutesneeded} minutes or {round(minutesneeded/60)} hours to reach")
print(f"Realistically, you'd need {round(realistically)} minutes or {round(realistically/1440)} days to reach it")
