import string
import random

sampleChars=string.ascii_letters+string.digits+' '

class Genome:
    chromosome: str
    fitness: int

    def __init__(self, text):
        self.chromosome = text

    def FitnessSelf(self, text):
        fitness = 0
        for i in range(len(text)):
            if self.chromosome[i] == text[i]: fitness += 1
        self.fitness = fitness


def randomString(size):
    return ''.join(random.choice(sampleChars) for i in range(size))

def replaceOneChar(origin,char,index):
    return origin[:index]+char+origin[index+1:]

class GAFindText:
    targetSize: int
    target: str
    populationSize: int
    maxGeneration: int
    mutationRate: float
    printStatus: bool

    def __init__(self, target, populationSize, maxGeneration, mutationRate,printStatus):
        self.targetSize = len(target)
        self.target = target
        self.populationSize = populationSize
        self.maxGeneration = maxGeneration
        self.mutationRate = mutationRate
        self.printStatus = printStatus

    def run(self):
        population = self.InitPopulation(self.populationSize, self.targetSize)
        generation=1
        while True:
            self.FitnessPopulation(self.target, population)
            population.sort(key=lambda g: g.fitness, reverse=True)

            currentMaxFitness = population[0].fitness
            self.printStatus and self.status(generation, population)
            if  currentMaxFitness == self.targetSize:
                print(f'{generation}세대 종료\n')
                break

            population=self.TopSelection(population)
            population=self.ProducePopulation(self.populationSize,population,self.targetSize)
            self.mutate(population,self.mutationRate,self.targetSize)
            generation+=1
        return generation

    def InitPopulation(self, populationSize, targetSize):
        return [Genome(randomString(targetSize)) for _ in range(populationSize)]

    def FitnessPopulation(self, target, population):
        [g.FitnessSelf(target) for g in population]

    def ProducePopulation(self,populationSize,population,targetSize):
        population.append(Genome(self.crossover(population[0], population[1], targetSize//2)))
        for i in range(populationSize-len(population)+1):
            parent1=random.choice(population)
            parent2 = random.choice(population)
            index=random.randint(1,targetSize-1)
            population.append(Genome(self.crossover(parent1,parent2,index)))
        return population

    def crossover(self,parent1,parent2,index):
        return parent1.chromosome[:index]+parent2.chromosome[index:]

    def TopSelection(self,population,topRate=0.01):
        lastIndex=int(len(population)*topRate)
        return population[:lastIndex]

    def mutate(self,population,mutationRate,targetSize):
        for i in range(len(population)):
            if random.random()<mutationRate:
                index=random.randint(0,targetSize-1)
                targetGenome = population[i]
                randomChar=random.choice(sampleChars)
                targetGenome.chromosome=replaceOneChar(targetGenome.chromosome,randomChar,index)

    def status(self, generation,population):
        topGenome=population[0]
        print(f'{generation}세대 유전자:{topGenome.chromosome} 적합도: {topGenome.fitness}')

records=[]
for _ in range(50):
    records.append(GAFindText('h1llo wo2ld my name is Python3',1000,500,1,False).run())
print(f'평균 {sum(records)/len(records)}세대')