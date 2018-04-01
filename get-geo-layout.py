#!/usr/bin/python3

layout = ''
varset = set()
with open("./geo/layout.txt","r") as file:
   for row in file:
      if row.isupper():
         var = row.strip()
         if var == 'BLANK' or (var not in varset and var[0].isalpha()):
            varset.add(var)
            if len(layout) > 0:
               layout = layout + ',' + row.strip()
            elif len(layout) == 0:
               layout = row.strip()
            else:
               print("Problem.")
with open("./geo/gyyyyp.lay","w") as file:
   file.write(layout + '\n')
   
print(layout)

