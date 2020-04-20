# Copyright 2010-2018 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Integer programming examples that show how to use the APIs."""

# capacity 25% doesn't work !!!

# [START program]
# [START import]
from __future__ import print_function
from ortools.linear_solver import pywraplp
# [END import]

def sumy(A, col=-1, row=-1):
    
    s=0
    if col != -1:
        for i in range(len(A)):
            s += A[i][col]
        return s
    if row != -1:
        for i in range(len(A[0])):
            s += A[row][i]
        return s

def sumproduct(A,B, dir='v', col=-1):
    s = 0
    
    if col != -1:
        for i in range(len(A)):
            s += A[i][col]*B[i]
        return s
    
    if type(A) is not list and type(B) is not list:
        return A*B
    elif type(A) is list and type(B) is not list:
        for i in A:
            s += i*B
        return s
    elif type(B) is list and type(A) is not list:
        for i in B:
            s += i*A
        return s
   
    if type(B[0]) is list and type(A[0]) is not list:
        A, B = B, A
    A_y = len(A)
    B_y = len(B)
    if type(A[0]) is list and type(B[0]) is not list:
        A_x = len(A[0])
        if (B_y == A_y and A_x != A_y) or (B_y == A_x and A_y == A_x and dir == 'v'):
            for i in range(A_y):
                for j in range(A_x):
                    s += A[i][j]*B[i]
            return s
        elif (B_y == A_x and A_x != A_y) or (B_y == A_x and A_y == A_x and dir == 'h'):
            for i in range(A_y):
                for j in range(A_x):
                    s += A[i][j]*B[j]
            return s
    elif type(A[0]) is list and type(B[0]) is list:
        A_x = len(A[0])    
        for i in range(A_y):
            for j in range(A_x):
                s += A[i][j]*B[i][j]
        return s
    elif type(A[0]) is not list and type(B[0]) is not list and A_y == B_y:
        for i in range(A_y):
            s += A[i]*B[i]
        return s
            
    
    
    return "dimension not matching"
    

def main():
    # [START solver]
    # Create the mip solver with the CBC backend.
    solver = pywraplp.Solver('simple_mip_program',
                             pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    # [END solver]

    # [START variables]
    infinity = solver.infinity()
    # x and y are integer non-negative variables.
    # X_i_j is the quantity produced from i sent to j
    
    X = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    for i in range(len(X)):
        for j in range(len(X[0])):
            X[i][j] = solver.IntVar(0.0, infinity, 'X_'+str(i)+'_'+str(j))
    
    Y = [[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]]
    
    Y_x = len(Y[0])
    Y_y = len(Y)
    for i in range(len(Y)):
        for j in range(len(Y[0])):
            Y[i][j] = solver.BoolVar('Y_'+str(i)+'_'+str(j))
    
    U = [0, 0, 0]
    V = [0, 0, 0, 0, 0]
    for i in range(len(X)):
        U[i] = solver.BoolVar( 'U_'+str(i))
    
    for i in range(len(X[0])):
        V[i] = solver.BoolVar( 'V_'+str(i))
    
        D_f_w = [[4836, 3338.4, 2568.8, 2347.8, 3650.4, 4411.2],
[3894.8, 1058.2, 6008.6, 2709.2, 1008.8, 4043.6],
[1313, 2620.8, 5605.6, 1354.6, 2147.6, 7352]]

    D_w_c =[[6305, 4271.8, 5777.2, 5207.8, 8039.2, 5051.8, 4123.6, 5142.8, 7233.2, 7329.4, 2756, 8309.6],
[2883.4, 1853.8, 3299.4, 1911, 4609.8, 2563.6, 2017.6, 2311.4, 3824.6, 5514.6, 1066, 4875],
[5402.8, 3135.6, 1921.4, 6234.8, 8130.2, 2670.2, 2953.6, 3008.2, 6328.4, 1924, 4877.6, 8725.6],
[1354.6, 1783.6, 3291.6, 3502.2, 6198.4, 2563.6, 1635.4, 2665, 5756.4, 4841.2, 6575.4, 6466.2],
[3491.8, 2431, 3876.6, 2269.8, 4997.2, 3140.8, 2555.8, 2888.6, 4417.4, 5990.4, 1071.2, 5262.4]]
    
    Demand = [1185, 1100, 800, 150, 475, 110, 238, 193, 173, 1180, 1038, 710]
    
    CostFac = [2000000]*3
    CostWarehouse = [6000000]*5
    for i in range(len(Y)):
        for j in range(len(Y[0])):
            D_w_c[i][j] *= Demand[j]
    
    
    totalDemand = sum(Demand)
    C_f = [totalDemand*0.6,totalDemand*0.55,totalDemand]
    WarCapRatio = 0.25
    C_w = [totalDemand*WarCapRatio,totalDemand*WarCapRatio,totalDemand*WarCapRatio,totalDemand*WarCapRatio,totalDemand*WarCapRatio]
    #print(X[1][3])
    #print(Y)
    #print(Y[1][3])
    print('Number of variables =', solver.NumVariables())
    
    
    # [END variables]

    # [START constraints]
    # x + 7 * y <= 17.5.
    
    #s = solver.IntVar(0, infinity, 'temp')
    
    # One warehous per client
    for i in range(Y_x):
        solver.Add(sumy(Y, col=i) == 1)
    
    #Y[0][i]+Y[1][i]+Y[2][i]+Y[3][i]+Y[4][i]
    #print(sumy(D_f_w,col = 2))
    
    # consevation du flux
    for i in range(Y_y):
        solver.Add(sumy(X, col=i) == sumproduct(Y[i],Demand))
    
    
    for i in range(len(X)):
        solver.Add( sum(X[i]) <= C_f[i]*U[i])
        print(C_f[i])
    
    solver.Add( sum(X[0]) >= C_f[0]*U[0]*0.3)
    solver.Add( sum(X[1]) >= C_f[1]*U[1]*0.3)
    
    # x <= 3.5.
    #solver.Add(x <= 3.5)
    for i in range(Y_y):
        solver.Add(sumy(X, col=i) <= C_w[i]*V[i])
        print(C_w[i])
    
    solver.Add( sum(U) >= 2)
    solver.Add( sum(V) >= 3)
    
    print('Number of constraints =', solver.NumConstraints())
    # [END constraints]


    # [START objective]
    # Maximize x + 10 * y.
    solver.Minimize(sumproduct(X,D_f_w)+sumproduct(Y,D_w_c)+sumproduct(U,CostFac)+sumproduct(V,CostWarehouse))
    # [END objective]

    # [START solve]
    status = solver.Solve()
    # [END solve]

    # [START print_solution]
    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        print("U:")
        for i in range(len(X)):
            print(U[i].solution_value())
        print("V:")
        for i in range(len(X[0])):
            print(V[i].solution_value())
        for i in range(len(X)):
            s=""
            for j in range(len(X[0])):
                s += str(X[i][j].solution_value())+ "\t"
            print(s)
        for i in range(len(Y)):
            s=""
            for j in range(len(Y[0])):
                s += str(Y[i][j].solution_value())+ "\t" # *Demand[j]
            print(s)
        
        #print('x =', x.solution_value())
        #print('y =', y.solution_value())
    else:
        print('The problem does not have an optimal solution.')
    # [END print_solution]
    print(C_f[0]*0.3,C_f[1]*0.3)
    # [START advanced]
    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
    # [END advanced]


if __name__ == '__main__':
    main()
# [END program]
