
from math import ceil
from imagehash import hex_to_hash


  
def similarity(songs: list,feature_hash: list):
    
    hammingDifferences  = []       # List contains the hamming distance of spectrogram hashes of all the songs and the mix
    feature1Differences = []       # List contains the hamming distance of feature 1 hashes of all the songs and the mix
    feature2Differences = []       # List contains the hamming distance of feature 2 hashes of all the songs and the mix
    feature3Differences = []       # List contains the hamming distance of feature 3 hashes of all the songs and the mix
    differences_list =[hammingDifferences,feature1Differences,feature2Differences,feature3Differences]
    avgSimilaritiesAll  = []        # List contains the similarity percentage of all the songs and the mix (Using average hash of Spectrogram and all the features)

    
    for i in range(len(songs)):
        sum=0
        for j in range(len(differences_list)):
            differences_list[j].append(getHammingDistance(hash1=songs[i][j+1], hash2=feature_hash[j]))
        
        for j in range(len(differences_list)):
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
