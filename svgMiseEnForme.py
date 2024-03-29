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
                endNextGroup = False  

                # style
                styleText, lastText = getStringEntre(contents, "<style" , "</style>")
                svg += "\n" + styleText 

                """ idée de features : 
                        - regarder si le st apparait > 1 fois sinon inutile """

                # différents groupes (couleurs, contours, bouttons des fois)
                while ((len(lastText) > 10) or lastText.replace(" ", "").replace("\n","").replace("\t","") != "</svg>") : 
                    groupeText, lastText = getStringEntre(lastText, '<g id="' , "</g>")
                    groups.append(groupeText)

                # histoire de valider le groupe et d'enlever les groupes vides 
                validGroups = []
                for i in range(len(groups)) : 
                    if groups[i] != "" : validGroups.append(groups[i])

                groups = validGroups      

                # traitement des groupes 
                for i in range(len(groups)) : 
                    thisGroup, lastText = getStringEntre(groups[i], '<g id="' , ">") 
                    nbLignes = lastText.count("<g") + lastText.count("<path") + lastText.count("<linearGradient") + lastText.count("<ellipse") # on compte le nombre d'élements  
                    #_, lastText = getStringEntre(lastText, '<g' , '>')
                    for j in range(nbLignes):
                        category, _ = getStringEntre(lastText, '<' , ' ') # on chope le category (path, linear, ellipse) 
                        category = category[1:].replace(" ","")
                        if (category == "g") :
                            thisLine, lastText = getStringEntre(lastText, '<g' , ">")
                        elif (category == "linearGradient") : 
                            thisLine, lastText = getStringEntre(lastText, '<linearGradient' , "</linearGradient>") # on récupère le bloc linearGradient 
                            thisLine = functionLinear(thisLine) # on le remet de belle manière 
                        elif (category == "path") :
                            thisLine, lastText = getStringEntre(lastText, '<path' , "/>")
                            thisLine = thisLine.replace("\n","").replace("\t", "").replace(" ","").replace("<path", "<path ")
                        elif (category == "ellipse") :
                            thisLine, lastText = getStringEntre(lastText, '<ellipse' , "/>")
                        else : 
                            print("Chelou ton truc là, t'es sûr du : " + filename) 
                            continue 
                        thisLine = "\t" + thisLine 
                        thisGroup = thisGroup + "\n" + thisLine
                    # groups[i] = thisGroup # je suis pas sur de l'interet de ceci 
                    thisGroup = thisGroup + "\n" + "</g>" # on ferme le groupe 
                    if (endNextGroup) : thisGroup = thisGroup + "\n" + "</g>" # on ferme le groupe une seconde fois 
                    if (groups[i].count("<g") == 2) : endNextGroup = True # pour dire qu'au prochain tour on doit fermer 2 groupes 
                    else : endNextGroup = False
                    #bprint(thisGroup)
                    
                    svg += "\n" + thisGroup
                
                svg += "\n" + "</svg>"
                svg = svg.replace('"d="','" d="').replace('"style="','" style="').replace('"class="', '" class="')
                #bprint(svg)
            
                
                with open(directory + "/new/"+filename, 'x') as finalSvg:
                    # finalSvg.write(contents)
                    finalSvg.write(svg)
                    finalSvg.close()
                

