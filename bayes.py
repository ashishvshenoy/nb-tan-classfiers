import math
import sys
import random

vertex_list = list()
edges_list = list()
parent_list = dict()
attributeList=[]
probability_distributions = dict()
probability_distributions_tan = dict()
weights = dict()

class Attribute:
    index = 0
    values = list()
    def __init__(self):
        self.setName("")
        self.setType("")
    def __str__(self):
        return str(self.Name)
    def setName(self, val):
        self.Name = val
    def setType(self, val):
        self.Type = val
    def setValues(self, val):
        self.values = val
    def getName(self):
        return str(self.Name)
    def getType(self):
        return str(self.Type)
    def getIndex(self):
        return self.index
    
    
def readArff(filename):
    global attributeList
    arrfFile = open(filename)
    lines = [line.rstrip('\n') for line in arrfFile]
    data = [[]]
    index = 0
    for line in lines :
        if(line.startswith('@attribute')) :
            attributeLine = line
            attributeLineSplit = attributeLine.split(' ',2)
            if "{" not in attributeLineSplit[2] :
                attr = Attribute()
                attr.setName(attributeLineSplit[1].replace('\'',''))
                attr.setType("real")
                attr.index = index
                attributeList.append(attr)
            else : 
                attr = Attribute()
                attr.setName(attributeLineSplit[1].replace('\'',''))
                attr.setType("class")
                attr.index = index
                attributeValueList = attributeLineSplit[2].replace('{',"")
                attributeValueList = attributeValueList.replace('}',"")
                attributeValues = [x.strip(" ") for x in attributeValueList.split(",")]
                attr.setValues(attributeValues)
                attributeList.append(attr)
            index+=1
        elif(not line.startswith('@data') and not line.startswith('@relation') and not line.startswith('%')) :
            data.append(line.split(','))
    del data[0]
    return data

def readTestArff(filename):
    arrfFile = open(filename)
    lines = [line.rstrip('\n') for line in arrfFile]
    data = [[]]
    index = 0
    for line in lines :
        if(line.startswith('@attribute')) :
            index+=1
        elif(not line.startswith('@data') and not line.startswith('@relation') and not line.startswith('%')) :
            data.append(line.split(','))
    del data[0]
    return data

def getInstances(attributeIndex, attributeValue):
    count = 0
    for line in data : 
        if(line[attributeIndex]==attributeValue) :
            count+=1
    return count
            
    
def getInstancesConditional(attribute1Index, attribute1Value, attribute2Index, attribute2Value):
    global data
    count = 0
    for line in data :
        if(line[attribute1Index] == attribute1Value and line[attribute2Index] == attribute2Value) :
            count+=1
    return count

def getInstancesConditionalTAN(attribute1Index, attribute1Value, attribute2Index, attribute2Value, attribute3Index, attribute3Value):
    global data
    count = 0
    for line in data :
        if(line[attribute1Index] == attribute1Value and line[attribute2Index] == attribute2Value
           and line[attribute3Index] == attribute3Value) :
            count+=1
    return count

def getProbability(instance_count, total_instances):
    return float(instance_count)/total_instances

def calculateProbabilitiesForNB():
    global data
    global attributeList
    global probability_distributions
    y1 = attributeList[-1].values[0]
    y2 = attributeList[-1].values[1]
    no_of_y1 = getInstances(len(attributeList)-1, y1)
    no_of_y2 = getInstances(len(attributeList)-1, y2)
    p_of_y1 = getProbability(no_of_y1+1, len(data)+2)
    p_of_y2 = getProbability(no_of_y2+1, len(data)+2)
    probability_distributions[y1] = p_of_y1
    probability_distributions[y2] = p_of_y2
    countList = list()
    for attr in attributeList :
        totalCount1 = 0
        for value in attr.values :
            n1 = getInstancesConditional(attr.getIndex(), value, len(attributeList)-1, y1)
            n2 = getInstancesConditional(attr.getIndex(), value, len(attributeList)-1, y2)
            countList.append([value,n1+1,n2+1])
            totalCount1+=1
        for c in countList :
            p_of_x_y1 = getProbability(c[1], no_of_y1+totalCount1)
            p_of_x_y2 = getProbability(c[2], no_of_y2+totalCount1)
            index1 = attr.Name+"="+c[0]+"|"+y1
            probability_distributions[index1] = p_of_x_y1
            index2 = attr.Name+"="+c[0]+"|"+y2
            probability_distributions[index2] = p_of_x_y2
        countList = list()
            

def naiveBayes():
    global data
    global test_data
    global probability_distributions
    calculateProbabilitiesForNB()
    for attr in attributeList :
        if(attr.index == len(attributeList)-1):
            print ""
            break
        print attr.Name + " " + attributeList[-1].Name
    y1 = attributeList[-1].values[0]
    y2 = attributeList[-1].values[1]
    correctClassified = 0
    incorrectlyClassified = 0
    for line in test_data :
        numerator = probability_distributions[y1]
        denominator = probability_distributions[y2]
        index = 0
        for l in line :
            if(index==len(attributeList)-1):
                break
            keyString1 = attributeList[index].Name+"="+l+"|"+y1
            numerator*= probability_distributions[keyString1]
            keyString2 = attributeList[index].Name+"="+l+"|"+y2
            denominator*= probability_distributions[keyString2]
            index+=1
        p_of_y1_line = getProbability(numerator, numerator+denominator)
        p_of_y2_line = getProbability(denominator, numerator+denominator)
        if(p_of_y2_line > p_of_y1_line):
            print y2 + " "+line[-1] + " ",
            print("%.16f" % p_of_y2_line)
            if(y2 == line[-1]):
                correctClassified+=1
            else :
                incorrectlyClassified+=1
        else :
            print y1 + " "+line[-1] + " ",
            print("%.16f" % p_of_y1_line)
            if(y1 == line[-1]):
                correctClassified+=1
            else : 
                incorrectlyClassified+=1
    print ""
    print correctClassified
    return float(correctClassified)/(incorrectlyClassified+correctClassified) 



def computeWeights():
    global data
    global attributeList
    global weights
    global probability_distributions
    y1 = attributeList[-1].values[0]
    y2 = attributeList[-1].values[1]
    no_of_y1 = getInstances(len(attributeList)-1, y1)
    no_of_y2 = getInstances(len(attributeList)-1, y2)
    summation = 0
    for attr1 in attributeList :
        if(attr1.index == len(attributeList)-1):
            continue
        for attr2 in attributeList :
            if(attr2.index == len(attributeList)-1):
                continue
            if(attr1.Name == attr2.Name):
                continue
            else :
                for value1 in attr1.values :
                    for value2 in attr2.values :
                        no_x1_x2_y1 = getInstancesConditionalTAN(attr1.index, value1, attr2.index, value2, len(attributeList)-1, y1)
                        p_no_x1_x2_y1 = getProbability(no_x1_x2_y1+1,len(data) + (len(attr1.values)*len(attr2.values)*2)) 
                        p_x1_x2_given_y1 = getProbability(no_x1_x2_y1+1,no_of_y1 + (len(attr1.values)*len(attr2.values)))
                        
                        no_x1_x2_y2 = getInstancesConditionalTAN(attr1.index, value1, attr2.index, value2, len(attributeList)-1, y2)
                        p_no_x1_x2_y2 = getProbability(no_x1_x2_y2+1,len(data) + (len(attr1.values)*len(attr2.values)*2))
                        p_x1_x2_given_y2 = getProbability(no_x1_x2_y2+1,no_of_y2 + (len(attr1.values)*len(attr2.values)))
                         
                        keyIndex = attr1.Name+"="+value1+"|"+y1
                        p_x1_y1 = probability_distributions[keyIndex]
                        keyIndex = attr2.Name+"="+value2+"|"+y2
                        p_x2_y2 = probability_distributions[keyIndex]
                        keyIndex = attr1.Name+"="+value1+"|"+y2
                        p_x1_y2 = probability_distributions[keyIndex]
                        keyIndex = attr2.Name+"="+value2+"|"+y1
                        p_x2_y1 = probability_distributions[keyIndex]
                        
                        sum1 = p_no_x1_x2_y1 * math.log(float(p_x1_x2_given_y1)/(p_x1_y1*p_x2_y1),2)
                        sum2 = p_no_x1_x2_y2 * math.log(float(p_x1_x2_given_y2)/(p_x1_y2*p_x2_y2),2)
                        summation+=sum1+sum2
                keyString = attr1.Name+","+attr2.Name+"|Y"
                weights[keyString] = summation
                summation = 0

def getMaximumWeightEdge(vertex_list):
    weight_list = list()
    for v in vertex_list :
        for attr in attributeList :
            if(attr.Name == v.Name or attr.Name=="class" or v.Name=="class" or attr.Name=="Class" or v.Name=="Class"):
                continue
            indexStr = v.Name+","+attr.Name+"|Y"
            if(attr not in vertex_list) :
                weight_list.append([weights[indexStr], v, attr])
    weight_list.sort(key=lambda x: x[0])
    highest_weight = weight_list[-1][0]
    for w in weight_list :
        if(w[0] == highest_weight):
            return w

def prims():
    global vertex_list
    global edges_list
    global parent_list
    vertex_list.append(attributeList[0])
    while(len(vertex_list)<len(attributeList)-1):
        edge = getMaximumWeightEdge(vertex_list)
        vertex_list.append(edge[2])
        edges_list.append(edge)
        parent_list[edge[2].Name] = edge[1]
    for attr in attributeList : 
        if(attr.Name.lower()=="class"):
            print ""
            break
        if(parent_list.has_key(attr.Name)):
            print attr.Name+ " " + parent_list[attr.Name].Name+ " "+ attributeList[-1].Name
        else  :
            print attr.Name+ " " + attributeList[-1].Name

def calculateProbabilitiesForTAN():
    y1 = attributeList[-1].values[0]
    y2 = attributeList[-1].values[1]
    for attr in attributeList :
        for value1 in attr.values : 
            if(parent_list.has_key(attr.Name)):
                parent_of_x = parent_list[attr.Name]
                for value2 in parent_of_x.values :
                    no_x1_parentx1_y1 = getInstancesConditionalTAN(attr.index,value1, parent_of_x.index, value2, len(attributeList)-1, y1)
                    no_x1_parentx1_y2 = getInstancesConditionalTAN(attr.index,value1, parent_of_x.index, value2, len(attributeList)-1, y2)
                    no_parentx1_y1 = getInstancesConditional(parent_of_x.index, value2, len(attributeList)-1, y1)
                    no_parentx1_y2 = getInstancesConditional(parent_of_x.index, value2, len(attributeList)-1, y2)
                    p_x1_given_parentx1_y1 = getProbability(no_x1_parentx1_y1+1, no_parentx1_y1+len(attr.values))
                    indexString = attr.Name+"="+value1+"|"+parent_of_x.Name+"="+value2+",Y="+y1
                    probability_distributions_tan[indexString] = p_x1_given_parentx1_y1
                    p_x1_given_parentx1_y2 = getProbability(no_x1_parentx1_y2+1, no_parentx1_y2+len(attr.values))
                    indexString = attr.Name+"="+value1+"|"+parent_of_x.Name+"="+value2+",Y="+y2
                    probability_distributions_tan[indexString] = p_x1_given_parentx1_y2
        
def tan():
    global data
    global attributeList
    global probability_distributions
    y1 = attributeList[-1].values[0]
    y2 = attributeList[-1].values[1]
    calculateProbabilitiesForNB()
    computeWeights()
    prims()
    calculateProbabilitiesForTAN()
    correctClassified=0
    incorrectlyClassified=0
    for line in test_data : 
        numerator = probability_distributions[y1]
        denominator = probability_distributions[y2]
        index = 0
        for l in line :
            if(index==len(attributeList)-1):
                break
            if(parent_list.has_key(attributeList[index].Name)):
                parent = parent_list[attributeList[index].Name]
                parent_value = line[parent.index]
                key1 = attributeList[index].Name+"="+l+"|"+parent.Name+"="+parent_value+",Y="+y1
                key2 = attributeList[index].Name+"="+l+"|"+parent.Name+"="+parent_value+",Y="+y2
                numerator*=probability_distributions_tan[key1]
                denominator*=probability_distributions_tan[key2]
            else :
                key1 = attributeList[index].Name+"="+l+"|"+y1
                key2 = attributeList[index].Name+"="+l+"|"+y2
                numerator*=probability_distributions[key1]
                denominator*=probability_distributions[key2]
            index+=1
        p_of_y1_x = getProbability(numerator, numerator+denominator)
        p_of_y2_x = getProbability(denominator, numerator+denominator)
        
        if(p_of_y1_x >=p_of_y2_x):
            print y1+" "+line[-1]+ " ",
            print("%.16f" % p_of_y1_x)
            if(y1==line[-1]):
                correctClassified+=1
            else : 
                incorrectlyClassified +=1
        else :
            print y2+" "+line[-1]+ " ",
            print("%.16f" % p_of_y2_x)
            if(y2==line[-1]):
                correctClassified+=1
            else : 
                incorrectlyClassified +=1
    print ""
    print correctClassified
    return float(correctClassified)/(correctClassified+incorrectlyClassified)
        
        
        
def learningCurve():
    global data
    global test_data
    listOfSampleSizes = [100]
    list1 = random.sample(data,50)
    data = list1
    print naiveBayes()
    #print accuracy1
    

def main():
    global data
    global test_data
    trainingSet = sys.argv[1]
    testSet = sys.argv[2]
    learningType = sys.argv[3]
    #trainingSet = "lymph_train.arff"
    #testSet = "lymph_test.arff"
    #learningType="t"
    data = readArff(trainingSet)
    test_data = readTestArff(testSet)
    if(learningType == "n"):  
        naiveBayes()
    elif(learningType == "t"):
        tan()
    else :
        print "Usage: bayes <train-set-file> <test-set-file> <n|t>"
        
main()
