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

print("==========================================================================================================================================================================================================================================================================================================================================")

directory = 'test'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if (f.endswith(".svg")) : 
        bprint(f) 
        if os.path.isfile(f):
            with open(f, 'rb') as svgf:
                groups = []
                lastText = ""
                contents = svgf.read()
                contents = contents.decode('utf8').replace("'", '"')

                # style
                styleText, lastText = getStringEntre(contents, "<style" , "</style>")
                #bprint(styleText)
                """ idée de features : 
                        - regarder si le st apparait > 1 fois sinon inutile """

                # différents groupes (couleurs, contours, bouttons des fois)
                while ((len(lastText) > 10) or lastText.replace(" ", "").replace("\n","").replace("\t","") != "</svg>") : 
                    groupeText, lastText = getStringEntre(lastText, '<g id="' , "</g>")
                    groups.append(groupeText)
                #tprint(groups)

                # traitement des groupes 

                """ Trucs à gérer : 
                            - Path 
                            - Linear Gradient 
                            - ellipse 
                            - autre ? 
                    """
                
                for i in range(len(groups)) : 
                    thisGroup, lastText = getStringEntre(groups[i], '<g id="' , ">") 
                    nbLignes = groups[i].count("<path") + groups[i].count("<linearGradient") + groups[i].count("<ellipse") # on compte le nombre d'élements  
                    _, lastText = getStringEntre(lastText, '<g' , '>')
                    for j in range(nbLignes):
                        category, _ = getStringEntre(lastText, '<' , ' ') # on chope le category (path, linear, ellipse) 
                        category = category[1:].replace(" ","")
                        if (category == "linearGradient") : 
                            print("linear")
                            thisLine, lastText = getStringEntre(lastText, '<linearGradient' , "</linearGradient>") 
                        elif (category == "path") :
                            print("path")
                            thisLine, lastText = getStringEntre(lastText, '<path' , "/>") 
                        elif (category == "ellipse") :
                            print("ellipse")
                            thisLine, lastText = getStringEntre(lastText, '<ellipse' , "/>")
                        else : 
                            print("Chelou ton truc là, t'es sûr du : " + filename) 
                            break 
                        thisGroup = thisGroup + "\n" + thisLine
                    groups[i] = thisGroup # on met à jour le groupe et on passe au suivant 
                    bprint(thisGroup)

