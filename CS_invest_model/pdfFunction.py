import copy
import random

def calcu(front,a,b,c,price):
    return fronter*(a**-(price/b))+c

def initGene():
    gene = []
    #103.5099661855971, 8249.079528885146, 26.000133264694576, 3859.1811983850303
    gene.append(random.normalvariate(103.5099661855971,0.2))
    gene.append(random.normalvariate(8249.079528885146,500.0))
    gene.append(random.normalvariate(26.000133264694576,0.2))
    
    return gene
    
def cross(oris):
    chil = []
    for i in range(3):
        sel  = random.randint(0,1)
        chil.append(oris[sel][i])
    
    return chil
    
def muta(ori):
    mute = ori[0:3]
    sel = random.randint(0,2)
    mute[sel] = random.normalvariate(ori[sel],0.2)
    
    return mute

def evalVal(gene):
    return gene[3]
    
pdfFile = open("./pdf.txt")
listPDF = pdfFile.readlines()
listData = []
for eachLine in listPDF:
    splitData = eachLine.split(',')
    splitData = [float(e) for e in splitData]
    listData.append(splitData)

stop = True
fronter = 6000.0
genes = [initGene() for _ in range(50)]
preGene = genes[0]
counter = 0
while stop:
    
    for gene in genes:
        sum = 0.0
        #print gene
        for data in listData:
            
            result = abs(calcu(fronter,gene[0],gene[1],gene[2],data[0])-data[1])
            #print data[0], data[1], result
            sum += result
        gene.append(sum)
        
    genes.sort(key=evalVal)
    
    genes = genes[:500]
    nextGenes = [gene[0:3] for gene in genes[:500]]
    for _ in range(250):
        nextGenes.append(cross(random.sample(genes,2)))
        nextGenes.append(muta(random.choice(genes)))
    
    
    
    print "PRE", preGene
    print "NOW", genes[0]
    print 
    if preGene[3] == genes[0][3]:
        counter += 1
        if counter > 50:
            stop = False
    else:
        counter = 0
    preGene = genes[0]
    genes = nextGenes
    
    #$D$1*POWER($F$1,-C2/$G$1)