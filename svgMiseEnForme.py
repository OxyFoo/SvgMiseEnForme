"""
Listes des choses à faire : 

    - Enlever la ligne version encoding et la ligne en dessous 
    - <svg> garder seulement les éléments essentiels 
    - Laisser les styles comme tel (puis enlever les styles non utilisé plus tard)
    - Bien indenter les linear gradiant 
    - Bien indenter et mettre sur une ligne les paths 
    - <g> mettre les paths sur une ligne 

    - Au niveau plus général, regarder si les noms sont bien utilisés, sinon les delete (surtout les noms à rallonge)
"""

# Créer un dossier de réception (où on mettra les nouveaux fichiers créés + avec la même architecture que celle qu'on a là)

# go through tous les fichiers 

# Commencer l'analyse un par un 

import os

def findPosition (text, mot, wantDebut) : 
    posStart = text.find(mot)
    posFin = posStart + len(mot)
    if wantDebut :
        return posStart
    else : 
        return posFin

def getStringEntre(text, firstWord, lastWord) : 
    firstPos = (findPosition(text, firstWord, True)) 
    lastPos = firstPos + (findPosition(text[firstPos:], lastWord, False))
    return (text[firstPos:lastPos], text[lastPos:])

def bprint(str) : 
    print(str)
    print("-" * 50)

def tprint(array) : 
    for i in range(len(array)) : 
        print(array[i])
        print("*" * 30)

def functionLinear(thisLine): 
    newLine = ""
    while (thisLine != "" or len(thisLine)>10) : 
        line, thisLine = getStringEntre(thisLine, "<" , ">")
        if (line.find("stop") != -1) : line = "\t\t" + line
        elif (line.find("</") != -1) : line = "\t" + line 
        newLine += line + "\n"
    return newLine

print("==========================================================================================================================================================================================================================================================================================================================================")

directory = 'test'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if (f.endswith(".svg")) : 
        bprint(f) 
        if os.path.isfile(f):
            with open(f, 'rb') as svgf:
                svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">'

                groups = []
                lastText = ""
                contents = svgf.read()
                contents = contents.decode('utf8').replace("'", '"')

                # style
                styleText, lastText = getStringEntre(contents, "<style" , "</style>")
                svg += "\n" + styleText 

                """ idée de features : 
                        - regarder si le st apparait > 1 fois sinon inutile """

                # différents groupes (couleurs, contours, bouttons des fois)
                while ((len(lastText) > 10) or lastText.replace(" ", "").replace("\n","").replace("\t","") != "</svg>") : 
                    groupeText, lastText = getStringEntre(lastText, '<g id="' , "</g>")
                    groups.append(groupeText)
                #tprint(groups)

                # traitement des groupes 
                for i in range(len(groups)) : 
                    thisGroup, lastText = getStringEntre(groups[i], '<g id="' , ">") 
                    nbLignes = groups[i].count("<path") + groups[i].count("<linearGradient") + groups[i].count("<ellipse") # on compte le nombre d'élements  
                    _, lastText = getStringEntre(lastText, '<g' , '>')
                    for j in range(nbLignes):
                        category, _ = getStringEntre(lastText, '<' , ' ') # on chope le category (path, linear, ellipse) 
                        category = category[1:].replace(" ","")
                        if (category == "linearGradient") : 
                            thisLine, lastText = getStringEntre(lastText, '<linearGradient' , "</linearGradient>") # on récupère le bloc linearGradient 
                            thisLine = functionLinear(thisLine) # on le remet de belle manière 
                        elif (category == "path") :
                            thisLine, lastText = getStringEntre(lastText, '<path' , "/>")
                            thisLine = thisLine.replace("\n","").replace("\t", "").replace(" ","")
                        elif (category == "ellipse") :
                            thisLine, lastText = getStringEntre(lastText, '<ellipse' , "/>")
                        else : 
                            print("Chelou ton truc là, t'es sûr du : " + filename) 
                            break 
                        thisLine = "\t" + thisLine 
                        thisGroup = thisGroup + "\n" + thisLine
                    groups[i] = thisGroup # on met à jour le groupe et on passe au suivant 
                    thisGroup = thisGroup + "\n" + "</g>" # on ferme le groupe 
                    svg += "\n" + thisGroup
                
                svg += "\n" + "</svg>"
                bprint(svg)