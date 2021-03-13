import pandas as pd #to import excel file -dataset
import xlrd  #to read row by row from excel
import random
from sklearn import preprocessing
import matplotlib.pyplot as plt
import numpy as np

class GA:
    def __init__(self, dietary_num, budget_num, calories_num): 
        self.dietary_num = dietary_num
        self.budget_num = budget_num
        self.calories_num = calories_num

        loc = ("dataset.xlsx")
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        populationArray = []
        for i in range(1, sheet.nrows): #it starts with the col names => do not read row no. 0
            populationArray.append(sheet.row_values(i))
        combination_array = []
        #initialzing randomly
        for i in range(0, len(populationArray)): 
            random_ndx = random.randint(0, len(populationArray)-1)
            combination_array.append(populationArray[random_ndx])

        all_populations_array = []
        all_total_fittness_arr = []
        all_avg_array = []
        for n in range(20): #Runs: Run your GA 20 times and report the average fitness.
            fittness_array = []
            temp_fittness_array = []
            new_temp_fittness_array = []
            new_population = []
            new_fittness_array = 0
            
                #fittness_array              
            for i in range(0, len(combination_array)): 
                temp_fittness_array.append(self.fitness(combination_array[i][2], combination_array[i][3], combination_array[i][4]))         
            
                # 0 - 1: normalize fitness       
            fittness_array = [float(i)/max(temp_fittness_array) for i in temp_fittness_array]
            
            
                #select
            selected_individuals = self.roulette_select(combination_array, fittness_array, len(combination_array))
            
                #crossover
            for k in range(0, len(selected_individuals)-1): 
                selected_individuals[k], selected_individuals[k + 1] = self.crossover(selected_individuals[k],selected_individuals[k + 1])
                    
                #mutation
            mutated_individuals = self.mutation(selected_individuals)
             
                #replacement
            for i in range(0, len(mutated_individuals)):
                combination_array = self.Replacement(mutated_individuals)
            
                #fitness for replaced population
            for i in range(0, len(combination_array)): 
                new_temp_fittness_array.append(self.fitness(combination_array[i][2], combination_array[i][3], combination_array[i][4]))
                        
                #new_fittness_array
            new_fittness_array = [float(i)/max(new_temp_fittness_array) for i in new_temp_fittness_array]

                #summation of all fittness for one generation => all_fitness_array stores all of the generation fitnesses
            all_total_fittness_arr.append(sum(new_fittness_array))
            
                 #avg_fitness
            avg = sum(new_fittness_array) / len(new_fittness_array)
                #array of the fitness avgs only
            all_avg_array.append(avg)
            
                #all_population_array stores all generations
            all_populations_array.append(combination_array)
                
                #termination condition
            if len(all_populations_array) > 3:
                termination_condition = self.terminate(all_avg_array)
                if termination_condition == True:
                    break;
                    
             # 0 - 1: normalize fitness       
        all_fittness_array = [float(i)/max(all_total_fittness_arr) for i in all_total_fittness_arr]
        all_avg_fitt = sum(all_fittness_array) / len(all_fittness_array)    #find avg of all generations = runs
        self.combinations(all_fittness_array, all_populations_array) 
        #max fitness of last genertion
        max_fittness = max(new_fittness_array)
        pop_index = new_fittness_array.index(max_fittness)
        print("*************** OUTPUT ********************")   
        print("MAX FITTNESS")    
        print(max(all_fittness_array))          
        print("AVERAGE FITTNESS")
        print(all_avg_fitt)
        print("BEST MEAL!")
        print(combination_array[pop_index])
     
            
    def combinations(self, all_fit_arr, all_pop_arr):
        
        indexArray = []
        for i in range(0, len(all_pop_arr)):
            indexArray.append(i)
            
        figure = plt.figure(figsize=(8,4))
            
        plt.plot(indexArray, all_fit_arr)
        plt.title("GA Performance")
        plt.xlabel("Population", fontweight="bold")
        plt.ylabel("Fittness", fontweight="bold")
        plt.show()
    
    def roulette_select(self, population, fittness_array, population_size):
        total_fitness = float(sum(fittness_array))
        rel_fitness = [f/total_fitness for f in fittness_array]
        #generate probability intervals for each individual
        probs = [sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]
        #select individuals
        new_population = []
        for n in range(population_size):
            r = random.random()
            for (i, individual) in enumerate(population):
                if r <= probs[i]:
                    if self.dietary_num == 1:
                        new_population.append(individual)
                        break
                    if self.dietary_num == 2:
                        if "Vegan" == individual[3] or  "Vegetarian" == individual[3]:
                            new_population.append(individual)
                            break
                    if self.dietary_num == 3:
                        if "Vegan" == individual[3]:
                            new_population.append(individual)
                            break

        return new_population

    
    def terminate(self, avg_array):# avg_array has many popultion 
        termination = False
        for i in range(0, len(avg_array)):
            if i < len(avg_array) - 3:
                a1 = avg_array[i]
                a2 = avg_array[i+1]
                a3 = avg_array[i+2]
                if a1 == a2 and a2 == a3:
                    termination = True
                    print("No improvement in the population!")
                    return termination
                    break
        return termination
            
         
    def crossover(self, gene1, gene2): 
        crossover_rate = 0.9
        crossover_point = random.randrange(0, 4) 
        crossover_random = random.randrange(0, 1)
        if crossover_random <= crossover_rate:
                return gene1[:crossover_point] + gene2[crossover_point:], gene2[:crossover_point] + gene1[crossover_point:]
            
            
    def mutation(self, genes):
        random_num = random.uniform(0, 1)
        mutation_rate = 0.01
        string_meal_random = 5
        for index in range(0, len(genes)):
            if random_num < mutation_rate:    
                index = int(random.uniform(0, len(genes)-1))
                value = int(random.uniform(0, 100))
                meal = random.randint(0, 4)
                if meal == 2 or meal == 4:
                    value = -1 * int(value)
                    genes[index][meal] = abs(genes[index][meal] + value)
                else:
                    string_meal = ["", "up", "down"]
                    string_meal_random = random.randint(0, 2)
                    if string_meal_random == 0:
                        genes[index][meal] = "" #empty
                    elif string_meal_random == 1: #up
                        if index != 0:
                            genes[index][meal] = genes[index-1][meal]
                        else:
                            genes[index][meal] = genes[index+1][meal]               
                    elif string_meal_random == 2: #up
                        if index != len(genes)-1:
                            genes[index][meal] = genes[index+1][meal]  
                        else:
                            genes[index][meal] = genes[index-1][meal]  
        return genes

            
    def avePopultion(self, population):
        averageFitness=0
        totalFitness=0
        for i in range(0, len(population)):
            totalFitness = totalFitness + self.fitness(population[i][2], population[i][3], population[i][4])
        averageFitness= totalFitness / len(population)
        return  averageFitness          

        
    def Replacement(self, pop_arr):        
            first_index = random.randint(0,len(pop_arr)-1)
            second_index = random.randint(0,len(pop_arr)-1)            
            if (first_index == second_index):
                first_index = first_index + 1 % len(pop_arr)-1
            p1=pop_arr[first_index]
            p2=pop_arr[second_index]
            ch1,ch2 = self.crossover(p1 ,p2)
            chf1= self.fitness(ch1[2],ch1[3],ch1[4])
            chf2= self.fitness(ch2[2],ch2[3],ch2[4])
            pf1= self.fitness(p1[2],p1[3],p1[4])
            pf2= self.fitness(p2[2],p2[3],p2[4])
            wp=[]
            wp.append(chf1)
            wp.append(chf2)
            wp.append(pf1)
            wp.append(pf2)                
            max1 = max(wp)
            wp.remove(max1)
            max2 = max(wp)
            counter_no_repeat = 0
            flag_p1 = True
            flag_p2 = True
            #step5 
            if(p1 == max1 or p1 == max2):
                counter_no_repeat += 1
            else: 
                flag_p1 = False    
            if(p2 == max1 or p2 == max2):
                counter_no_repeat += 1
            else: 
                flag_p2 = False    
            if(ch1 == max1 or ch1 == max2 and counter_no_repeat < 3):
                if(flag_p1 == False):
                    pop_arr[first_index] = ch1
                else:
                    pop_arr[second_index] = ch1
            if(ch2 == max1 or ch2 == max2 and counter_no_repeat < 3):
                if(flag_p1 == False):
                    pop_arr[first_index] = ch2
                else:
                    pop_arr[second_index] = ch2        
            return pop_arr

      
       
                
                
    def fitness(self, calories, item_type, budget):
        fittness_value = 0
        type_fittness, budget_fittness, calories_fittness = 0, 0, 0
        if self.dietary_num == 1:
                type_fittness = 2
                
        if self.dietary_num == 2:
            if "Vegan" == item_type or  "Vegetarian" == item_type:
                type_fittness = 2
                
                
        if self.dietary_num == 3:
           if "Vegan" == item_type:
              type_fittness = 2
           
        if type_fittness != 0:
            budget_diff = self.budget_num - int(budget)
            if budget_diff >= 0:
                budget_fittness = 2 + budget_diff

            calories_diff = self.calories_num - float(calories)
            if calories_diff >= 0:
               calories_fittness = 2 + calories_diff    
           
        gene_fittness = 0.4*type_fittness + 0.4*budget_fittness + 0.2*calories_fittness
        
        return gene_fittness


dietary = input("Choose the number of your dietary preference:\n"
                +"1. Regular\n"
                +"2. Vegetarian\n"
                +"3. Vegan\n") 
    
dietary_num = int(dietary)
    
if  dietary_num==1:
    dietary = "Regular"
if  dietary_num==2:
    dietary = "Vegetarian"
if  dietary_num==3:
    dietary = "Vegan"
        
#User enters their budget
budget = input("Enter your budget:\n")
budget_num = int(budget)
        
        
#User enters their choise of calories
calories = input("Enter the number of calories:\n")
calories_num = int(calories)
    
app = GA(dietary_num, budget_num, calories_num)
