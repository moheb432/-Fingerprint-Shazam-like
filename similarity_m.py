
from math import ceil
from imagehash import hex_to_hash


  
def similarity(songs: list,feature_hash: list):
    
    hammingDifferences  = []      
    feature1Differences = []   
    feature2Differences = []       
    feature3Differences = []       
    differences_list =[hammingDifferences,feature1Differences,feature2Differences,feature3Differences]
    avgSimilaritiesAll  = []        

    
    for i in range(len(songs)):
        sum=0
        for j in range(len(differences_list)):
            differences_list[j].append(getHammingDistance(hash1=songs[i][j+1], hash2=feature_hash[j]))
        
            sum =sum + differences_list[j][i]
        avg=sum/4
        avgMap = mapRanges(avg, 0, 255, 0, 1)  
        result = (1 - avgMap) * 100
        avgSimilaritiesAll.append(result) # list of similarity index have the same index of he song
    return avgSimilaritiesAll
        
def getHammingDistance(hash1: str, hash2: str) ->int :
    try:
        return hex_to_hash(hash1) - hex_to_hash(hash2)
    except:
        return 255
def mapRanges(inputValue: float, inMin: float, inMax: float, outMin: float, outMax: float):
    slope = (outMax-outMin) / (inMax-inMin)
    return outMin + slope*(inputValue-inMin)
