import TreeMaster as dt
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate age-adjusted risk
def age_adj_risk(maternal_age):
    risk = (1/(1+np.exp(7.330-(4.211/(1+np.exp(-0.282*(maternal_age-37.23)))))))
    return risk

# class to build tree
class PrenatalTree:

    PRM = .0022 # probability that a CVS diagnostic test will result in a Procedure Related Miscarriage
    SFL= .43    # probability that a Trisomy 21 pregnancy will result in a Spontaneous Fetal Loss
    TOP = .8    # probability that a positive CVS diagnosis of a Trisomy 21 pregnancy will result in the Termination of the Pregnancy

    ULB_cost = 0        #   cost of Unaffected Live Birth $0
    TLB_cost = 427577   # 	cost of Trisomy Live Birth $427,577
    SFL_cost = 0        # 	cost of Spontaneous Fetal Loss $0
    PRM_cost = 0        # 	cost of Procedure Related Miscarriage $0
    TOP_cost = 581      # 	cost of Termination of Pregnancy $581
    CVS_cost = 1010     # 	cost of chorionic villus sampling $1,010

    def __init__(self, age):
        self._age = age

        # dictionary for decision nodes
        #               // key: cost, utility, [future nodes]
        dictDecisions = {'d1': [0,     0,       ['Diagnostic Test', 'No Diagnostic Test']]};

        # dictionary for chance nodes
        #           // key: cost,   utility,  [future nodes],  [probabilities]
        dictChances = {'Diagnostic Test': [self.CVS_cost,   0,       ['c3', 'c4'],    [age_adj_risk(age), 1-age_adj_risk(age)]],
                       'No Diagnostic Test': [0,          0,       ['c5', 't9'],    [age_adj_risk(age), 1-age_adj_risk(age)]],
                       'c3': [0,          0,       ['c6', 't4'],    [1-self.PRM, self.PRM]],
                       'c4': [0,          0,       ['t5', 't6'],    [1-self.PRM, self.PRM]],
                       'c5': [0,          0,       ['t7', 't8'],    [self.SFL, 1-self.SFL]],
                       'c6': [0,          0,       ['t1', 'c7'],    [self.TOP, 1-self.TOP]],
                       'c7': [0,          0,       ['t2', 't3'],    [self.SFL, 1-self.SFL]]};

        # dictionary for terminal nodes
        #               //key: cost, utility
        dictTerminals = {'t1': [self.TOP_cost,       0],
                         't2': [self.SFL_cost,       0],
                         't3': [self.TLB_cost,       0],
                         't4': [self.PRM_cost,       0],
                         't5': [self.ULB_cost,       0],
                         't6': [self.PRM_cost,       0],
                         't7': [self.SFL_cost,       0],
                         't8': [self.TLB_cost,       0],
                         't9': [self.ULB_cost,       0]};

        # initiates tree
        self.myDT = dt.DecisionNode('d1', 1, dictDecisions, dictChances, dictTerminals)

    # gets costs of Diagnostis Test and No Diagnostic Test
    def get_cost(self):
        return self.myDT.get_cost()

# empty lists to gather age and costs for graph
age_list = []
diagnostic_costs = []
no_diagnostic_costs = []

#loop to initiate tree with ages
for age in range(16,56):
    mytree = PrenatalTree(age)
    age_list.append(age-1)
    diagnostic_costs.append(mytree.get_cost()['Diagnostic Test'][0])
    no_diagnostic_costs.append(mytree.get_cost()['No Diagnostic Test'][0])
print ("Data for Maternal Age by Cost")
print (age_list)
print (diagnostic_costs)
print (no_diagnostic_costs)


# plot (age, cost) for each age
plt.plot((age_list), (diagnostic_costs), label = "Diagnostic Test")
plt.plot((age_list), (no_diagnostic_costs), label = "No Diagnostic Test")
plt.legend(loc='upper left')
plt.xlabel('age')
plt.ylabel('cost')
plt.show()
