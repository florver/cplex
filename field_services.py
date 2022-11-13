# -*- coding: utf-8 -*-
"""field_services.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dBWo9JSgaHVaM_gUj938-L90alE7s7kQ
"""

import sys
import cplex
import numpy as np

TOLERANCE =10e-6 

class Orden:
    def __init__(self):
        self.id = 0
        self.beneficio = 0
        self.trabajadores_necesarios = 0
    
    def load(self, row):
        self.id = int(row[0])
        self.beneficio = int(row[1])
        self.trabajadores_necesarios = int(row[2])
        

class FieldWorkAssignment:
    def __init__(self):
        self.cantidad_trabajadores = 0
        self.cantidad_ordenes = 0
        self.ordenes = []
        self.conflictos_trabajadores = []
        self.ordenes_correlativas = []
        self.ordenes_conflictivas = []
        self.ordenes_repetitivas = []
        self.dias = 6
        self.turnos = 5
        self.costos = [-1000.0,-1200.0,-1400.0,-1500.0]
        self.trozos = [5.0,5.0,5.0,35.0]

    def load(self,filename):
        # Abrimos el archivo.
        f = open(filename)


        # Leemos la cantidad de trabajadores
        self.cantidad_trabajadores = int(f.readline())
        
        # Leemos la cantidad de ordenes
        self.cantidad_ordenes = int(f.readline())
        
        # Leemos cada una de las ordenes.
        self.ordenes = []
        for i in range(self.cantidad_ordenes):
            row = f.readline().split(' ')
            orden = Orden()
            orden.load(row)
            self.ordenes.append(orden)
        
        # Leemos la cantidad de conflictos entre los trabajadores
        cantidad_conflictos_trabajadores = int(f.readline())
        
        # Leemos los conflictos entre los trabajadores
        self.conflictos_trabajadores = []
        for i in range(cantidad_conflictos_trabajadores):
            row = f.readline().split(' ')
            self.conflictos_trabajadores.append(list(map(int,row)))
            
        # Leemos la cantidad de ordenes correlativas
        cantidad_ordenes_correlativas = int(f.readline())
        
        # Leemos las ordenes correlativas
        self.ordenes_correlativas = []
        for i in range(cantidad_ordenes_correlativas):
            row = f.readline().split(' ')
            self.ordenes_correlativas.append(list(map(int,row)))
            
        # Leemos la cantidad de ordenes conflictivas
        cantidad_ordenes_conflictivas = int(f.readline())
        
        # Leemos las ordenes conflictivas
        self.ordenes_conflictivas = []
        for i in range(cantidad_ordenes_conflictivas):
            row = f.readline().split(' ')
            self.ordenes_conflictivas.append(list(map(int,row)))
        
        
        # Leemos la cantidad de ordenes repetitivas
        cantidad_ordenes_repetitivas = int(f.readline())
        
        # Leemos las ordenes repetitivas
        self.ordenes_repetitivas = []
        for i in range(cantidad_ordenes_repetitivas):
            row = f.readline().split(' ')
            self.ordenes_repetitivas.append(list(map(int,row)))
        
        # Cerramos el archivo.
        f.close()


def get_instance_data():
    file_location = sys.argv[1].strip()
    instance = FieldWorkAssignment()
    instance.load(file_location)
    return instance
    

def add_constraint_matrix(my_problem, data):
    
    # Restriccion generica
    #indices = 
    #values = []
    #row = [indices,values]
    #my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[])

    # Restricción que no se haga 2 ordenes en mismo turno y día

    for n in range(len(data.ordenes)):
      variables_restriccion = []
      for j in range(data.cantidad_trabajadores):
        for d in range(data.dias):
          for t in range(data.turnos):
            variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
            values = [1]*len(variables_restriccion)
            row = [variables_restriccion, values]
            my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[1.0])


     # Restricción "Ninǵun trabajador puede trabajar los 5 turnos de un día"

    #for j in range(trabajadores):
      #for d in range(dias):
       # variables_restriccion = []
        #for n in range(ordenes):
         # for t in range(turnos):
          #  variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
           # values = [1]*len(variables_restriccion)
           # row = [variables_restriccion, values]
            #my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[4.0])

      for j in range(data.cantidad_trabajadores):
            for d in range(data.dias):
              variables_restriccion = []
              variables_restriccion_z = []
              variables_restriccion_z.append('z'+'_'+str(j)+'_'+str(d))        
              for n in range(len(data.ordenes)):
                for t in range(data.turnos):
                  variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
                  values = [1]*len(variables_restriccion) + [-4]*len(variables_restriccion_z)
                  row = [variables_restriccion + variables_restriccion_z, values]
                  my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[0.0])


      # Restricción "Ninǵun trabajador puede trabajar los 6 días de la semana"

      for j in range(data.cantidad_trabajadores):
        variables_restriccion_z = []
        for d in range(data.dias):
          variables_restriccion_z.append('z'+'_'+str(j)+'_'+str(d))
          values = [1]*len(variables_restriccion_z)
          row = [variables_restriccion_z, values]
          my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[5.0])                  



      # Restricción una orden no se puede hacer 2 veces

    for n in range(len(data.ordenes)):
      for j in range(data.cantidad_trabajadores):
        variables_restriccion = []
        for d in range(data.dias):
          for t in range(data.turnos):
            variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
            values = [1]*len(variables_restriccion)
            row = [variables_restriccion, values]
            my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[1.0])             

      
      # Restricción "Una orden de trabajo debe tener asignada sus To trabajadores en un mismo turno para poder ser resuelta"

    for n in range(len(data.ordenes)):
      variables_restriccion = []
      for j in range(data.cantidad_trabajadores):
        for d in range(data.dias):
          for t in range(data.turnos):
            variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
            values = [1]*len(variables_restriccion)
            row = [variables_restriccion, values]
            my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[data.ordenes[n].trabajadores_necesarios])


      # Restricción “Diferencia entre el trabajador con más órdenes asignadas y el trabajador con menos órdenes no puede ser mayor a 10"

      for j in range(data.cantidad_trabajadores):
        variables_costos = []
        for k in range(len(data.costos)):
          variables_costos.append('x'+'_'+str(j)+'_'+str(k))
          for jj in range(data.cantidad_trabajadores):
            if j != jj:
              variables_costos_2 = []
              for kk in range(len(data.costos)):
                variables_costos_2.append('x'+'_'+str(jj)+'_'+str(kk))
                values = [1]*len(variables_costos) + [-1]*len(variables_costos_2)
                #variables_costos_final = [variables_costos, variables_costos_2]
                row = [variables_costos + variables_costos_2, values]
                my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[10])
                my_problem.linear_constraints.add(lin_expr=[row], senses=['G'], rhs=[-10])
              else:
                continue


       # Restricción “Existen algunos pares de  ́ordenes de trabajo correlativas”  


#      for n in range(len(data.ordenes_correlativas)):
#        for d in range(data.dias):
#          variables_restriccion = []
#          for j in range(data.cantidad_trabajadores):
#            variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(4)+'_'+str(data.ordenes_correlativas[n][0]))
#            values = [1]*len(variables_restriccion) 
#            row = [variables_restriccion, values]
#            my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[0.0])


#      for n in range(len(data.ordenes_correlativas)):
#        for d in range(data.dias):
#          for t in range(data.turnos):
#            variables_restriccion_delta = []
#            variables_restriccion_delta.append('delta'+'_'+str(data.ordenes_correlativas[n][0])+'_'+str(d)+'_'+str(t))
#            variables_restriccion = []
#            for j in range(data.cantidad_trabajadores):
#              variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(data.ordenes_correlativas[n][0]))
#              values = [1]*len(variables_restriccion) + [-1.0] * data.ordenes[data.ordenes_correlativas[n][0]].trabajadores_necesarios * len(variables_restriccion_delta)
#              row = [variables_restriccion + variables_restriccion_delta, values]
#              my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[0.0])


#      for n in range(len(data.ordenes_correlativas)):
#        for d in range(data.dias):
#          for t in range(data.turnos):
#            variables_restriccion_delta = []
#            variables_restriccion_delta.append('delta'+'_'+str(data.ordenes_correlativas[n][0])+'_'+str(d)+'_'+str(t))
#            variables_restriccion = []
#            for j in range(data.cantidad_trabajadores):
#              variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t+1)+'_'+str(data.ordenes_correlativas[n][1]))
#              values = [1]*len(variables_restriccion) + [-1.0] * data.ordenes[data.ordenes_correlativas[n][1]].trabajadores_necesarios * len(variables_restriccion_delta)
#              row = [variables_restriccion + variables_restriccion_delta, values]
#              my_problem.linear_constraints.add(lin_expr=[row], senses=['G'], rhs=[0.0])

      
      # Restricción “Hay pares de órdenes de trabajo que no pueden ser satisfechas en turnos consecutivos de un trabajador”

      for n in range(len(data.ordenes_conflictivas)):
        for d in range(data.dias):
          for t in range(data.turnos):
            for j in range(data.cantidad_trabajadores):
              variables_restriccion = []
              variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(data.ordenes_conflictivas[n][0]))
              variables_restriccion_lambda = []
              variables_restriccion_lambda.append('lambda'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(data.ordenes_conflictivas[n][0]))
              values = [1]*len(variables_restriccion) + [-1]*len(variables_restriccion_lambda)
              row = [variables_restriccion + variables_restriccion_lambda, values]
              my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[0.0])


      for n in range(len(data.ordenes_conflictivas)):
              for d in range(data.dias):
                for t in range(data.turnos):
                  for j in range(data.cantidad_trabajadores):
                    if t < data.turnos-1:
                      variables_restriccion = []
                      variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t+1)+'_'+str(ordenes_conflictivas[n][1]))
                      variables_restriccion_lambda = []
                      variables_restriccion_lambda.append('lambda'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(ordenes_conflictivas[n][0]))
                      values = [1]*len(variables_restriccion) + [-0.5]*len(variables_restriccion_lambda)
                      row = [variables_restriccion + variables_restriccion_lambda, values]
                      my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[0.0])
                    else:
                      continue        

      # Restricciones necesarias para salario de los trabajadores
    

    #1er tramo
      for j in range(data.cantidad_trabajadores):
        variables_costos = []
        variables_costos.append('x'+'_'+str(j)+'_'+str(0))
        variables_restriccion = [] 
        for d in range(data.dias):
          for t in range(data.turnos):
            for n in range(len(data.ordenes)):
              variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
              values = [1]*len(fdfvariables_restriccion) + [-1]*len(variables_costos)
              row = [variables_restriccion + variables_costos, values]
              my_problem.linear_constraints.add(lin_expr=[row], senses=['E'], rhs=[0.0])


        for j in range(data.cantidad_trabajadores):
                variables_costos = []
                variables_costos.append('x'+'_'+str(j)+'_'+str(0))
                variables_w = []
                variables_w.append('w'+'_'+str(j)+'_'+str(0))
                values_1 = [1]*len(variables_costos)
                row_1 = [variables_costos, values_1]
                my_problem.linear_constraints.add(lin_expr=[row_1], senses=['L'], rhs=[5.0])
                values_2 = [5]*len(variables_w) + [-1]*len(variables_costos)
                row_2 = [variables_w + variables_costos, values_2]
                my_problem.linear_constraints.add(lin_expr=[row_2], senses=['L'], rhs=[0.0])


      #2do tramo
        for j in range(data.cantidad_trabajadores):
                variables_costos_0 = []
                variables_costos_0.append('x'+'_'+str(j)+'_'+str(0))
                variables_costos_1 = []
                variables_costos_1.append('x'+'_'+str(j)+'_'+str(1))
                variables_restriccion = [] 
                for d in range(data.dias):
                  for t in range(data.turnos):
                    for n in range(len(data.ordenes)):
                      variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
                      values = [1]*len(variables_restriccion) + [-1]*len(variables_costos_0) + [-1]*len(variables_costos_1)
                      row = [variables_restriccion + variables_costos_0 + variables_costos_1, values]
                      my_problem.linear_constraints.add(lin_expr=[row], senses=['E'], rhs=[0.0])


        for j in range(data.cantidad_trabajadores):
                        variables_costos = []
                        variables_costos.append('x'+'_'+str(j)+'_'+str(1))
                        variables_w_0 = []
                        variables_w_0.append('w'+'_'+str(j)+'_'+str(0))
                        variables_w_1 = []
                        variables_w_1.append('w'+'_'+str(j)+'_'+str(1))
                        values_1 = [1]*len(variables_costos) + [-5]*len(variables_w_0)
                        row_1 = [variables_costos + variables_w_0, values_1]
                        my_problem.linear_constraints.add(lin_expr=[row_1], senses=['L'], rhs=[0.0])
                        values_2 = [5]*len(variables_w_1) + [-1]*len(variables_costos)
                        row_2 = [variables_w_1 + variables_costos, values_2]
                        my_problem.linear_constraints.add(lin_expr=[row_2], senses=['L'], rhs=[0.0])                                      


      #3er tramo
        for j in range(data.cantidad_trabajadores):
                variables_costos_0 = []
                variables_costos_0.append('x'+'_'+str(j)+'_'+str(0))
                variables_costos_1 = []
                variables_costos_1.append('x'+'_'+str(j)+'_'+str(1))
                variables_costos_2 = []
                variables_costos_2.append('x'+'_'+str(j)+'_'+str(2))
                variables_restriccion = [] 
                for d in range(data.dias):
                  for t in range(data.turnos):
                    for n in range(len(data.ordenes)):
                      variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
                      values = [1]*len(variables_restriccion) + [-1]*len(variables_costos_0) + [-1]*len(variables_costos_1)+ [-1]*len(variables_costos_2)
                      row = [variables_restriccion + variables_costos_0 + variables_costos_1 + variables_costos_2, values]
                      my_problem.linear_constraints.add(lin_expr=[row], senses=['E'], rhs=[0.0])


        for j in range(data.cantidad_trabajadores):
                        variables_costos = []
                        variables_costos.append('x'+'_'+str(j)+'_'+str(2))
                        variables_w_1 = []
                        variables_w_1.append('w'+'_'+str(j)+'_'+str(1))
                        variables_w_2 = []
                        variables_w_2.append('w'+'_'+str(j)+'_'+str(2))
                        values_1 = [1]*len(variables_costos) + [-5]*len(variables_w_1)
                        row_1 = [variables_costos + variables_w_1, values_1]
                        my_problem.linear_constraints.add(lin_expr=[row_1], senses=['L'], rhs=[0.0])
                        values_2 = [5]*len(variables_w_2) + [-1]*len(variables_costos)
                        row_2 = [variables_w_2 + variables_costos, values_2]
                        my_problem.linear_constraints.add(lin_expr=[row_2], senses=['L'], rhs=[0.0])

      #4to tramo
        for j in range(data.cantidad_trabajadores):
                variables_costos_0 = []
                variables_costos_0.append('x'+'_'+str(j)+'_'+str(0))
                variables_costos_1 = []
                variables_costos_1.append('x'+'_'+str(j)+'_'+str(1))
                variables_costos_2 = []
                variables_costos_2.append('x'+'_'+str(j)+'_'+str(2))
                variables_costos_3 = []
                variables_costos_3.append('x'+'_'+str(j)+'_'+str(3))
                variables_restriccion = [] 
                for d in range(data.dias):
                  for t in range(data.turnos):
                    for n in range(len(data.ordenes)):
                      variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
                      values = [1]*len(variables_restriccion) + [-1]*len(variables_costos_0) + [-1]*len(variables_costos_1) + [-1]*len(variables_costos_2) + [-1]*len(variables_costos_3)
                      row = [variables_restriccion + variables_costos_0 + variables_costos_1 + variables_costos_2 + variables_costos_3, values]
                      my_problem.linear_constraints.add(lin_expr=[row], senses=['E'], rhs=[0.0])


        for j in range(data.cantidad_trabajadores):
                        variables_costos = []
                        variables_costos.append('x'+'_'+str(j)+'_'+str(3))
                        variables_w_2 = []
                        variables_w_2.append('w'+'_'+str(j)+'_'+str(2))
                        variables_w_3 = []
                        variables_w_3.append('w'+'_'+str(j)+'_'+str(3))
                        values_1 = [1]*len(variables_costos) + [-15]*len(variables_w_2)
                        row_1 = [variables_costos + variables_w_2, values_1]
                        my_problem.linear_constraints.add(lin_expr=[row_1], senses=['L'], rhs=[0.0])
                        values_2 = [1]*len(variables_costos)
                        row_2 = [variables_costos, values_2]
                        my_problem.linear_constraints.add(lin_expr=[row_2], senses=['G'], rhs=[0.0])


          #Restricciones de w_j_k
      
      for j in range(data.cantidad_trabajadores):
        variables_w = []
        for k in range(len(data.costos)):
          variables_w.append('w'+'_'+str(j)+'_'+str(k))
          values_1 = [1]*len(variables_w[1]) + [-1]*len(variables_w[0])
          row_1 = [variables_w[1] + variables_w[0], values_1]
          my_problem.linear_constraints.add(lin_expr=[row_1], senses=['L'], rhs=[0.0])
          values_2 = [1]*len(variables_w[2]) + [-1]*len(variables_w[1])
          row_2 = [variables_w[2] + variables_w[1], values_2]
          my_problem.linear_constraints.add(lin_expr=[row_2], senses=['L'], rhs=[0.0])
          values_3 = [1]*len(variables_w[3]) + [-1]*len(variables_w[2])
          row_3 = [variables_w[3] + variables_w[2], values_3]
          my_problem.linear_constraints.add(lin_expr=[row_3], senses=['L'], rhs=[0.0])


def populate_by_row(my_problem, data):

    # Definimos y agregamos las variables.
    coeficientes_beneficio = []
    for j in range(data.cantidad_trabajadores): 
      for d in range(data.dias):
        for t in range(data.turnos):
          for n in range(len(data.ordenes)):
            coeficientes_beneficio.append(data.ordenes[n].beneficio)
    coeficientes_costo = list(np.tile(data.costos, data.cantidad_trabajadores))
    coeficientes_funcion_objetivo = (coeficientes_beneficio + coeficientes_costo)
    
    variables_beneficios = []
    for j in range(data.cantidad_trabajadores): 
      for d in range(data.dias):
        for t in range(data.turnos):
          for n in range(len(data.ordenes)):
            variables_beneficios.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
    
    variables_costos = []
    for j in range(data.cantidad_trabajadores):
      for k in range(len(data.costos)):
        variables_costos.append('x'+'_'+str(j)+'_'+str(k))
        
    my_problem.variables.add(obj = coeficientes_funcion_objetivo, lb =[0]*len(coeficientes_beneficio) + [0]*len(coeficientes_costo), ub = [1]*len(coeficientes_beneficio) + list(np.tile(data.trozos, data.cantidad_trabajadores))
                             , types=['B']*len(coeficientes_beneficio) + ['I']*len(coeficientes_costo), names = (variables_beneficios + variables_costos))


    # Columna para Z_j_d
    variable_z = []
    for j in range(data.cantidad_trabajadores):
      for d in range(data.dias):
        variable_z.append('z'+'_'+str(j)+'_'+str(d))

    my_problem.variables.add(obj = [0.0] * len(variable_z), lb = [0]*len(variable_z), ub = [1]*len(variable_z), types= ['B']*len(variable_z), names = variable_z)


    # Columna para delta_n_d_t
    variable_delta = []
    for n in range(len(data.ordenes_correlativas)):
      for d in range(data.dias):
        for t in range(data.turnos):
          variable_delta.append('delta'+'_'+str(data.ordenes_correlativas[n][0])+'_'+str(d)+'_'+str(t))

    my_problem.variables.add(obj = [0.0] * len(variable_delta), lb = [0]*len(variable_delta), ub = [1]*len(variable_delta), types= ['B']*len(variable_delta), names = variable_delta)


    # Columna para lambda_n_d_t_j
    variable_lambda = []
    for n in range(len(data.ordenes_conflictivas)):
      for d in range(data.dias):
        for t in range(data.turnos):
          for j in range(data.cantidad_trabajadores):
            variable_lambda.append('lambda'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(data.ordenes_conflictivas[n][0]))

    my_problem.variables.add(obj = [0.0] * len(variable_lambda), lb = [0]*len(variable_lambda), ub = [1]*len(variable_lambda), types= ['B']*len(variable_lambda), names = variable_lambda)
    
    # Columna para w_j_k
    variables_w = []
    for j in range(data.cantidad_trabajadores):
      for k in range(len(data.costos)):
        variables_w.append('w'+'_'+str(j)+'_'+str(k))
        
    my_problem.variables.add([0.0] * len(variables_w), lb = [0]*len(variables_w), ub = [1]*len(variables_w), types= ['B']*len(variables_w), names = variables_w)

    # Seteamos direccion del problema
    # ~ my_problem.objective.set_sense(my_problem.objective.sense.maximize)
    # ~ my_problem.objective.set_sense(my_problem.objective.sense.minimize)

    # Definimos las restricciones del modelo. Encapsulamos esto en una funcion. 
    add_constraint_matrix(my_problem, data)

    # Exportamos el LP cargado en myprob con formato .lp. 
    # Util para debug.
    my_problem.write('field_services_1.lp')

def solve_lp(my_problem, data):
    
    # Resolvemos el ILP.
    
    my_problem.solve()

    # Obtenemos informacion de la solucion. Esto lo hacemos a traves de 'solution'. 
    x_variables = my_problem.solution.get_values()
    objective_value = my_problem.solution.get_objective_value()
    status = my_problem.solution.get_status()
    status_string = my_problem.solution.get_status_string(status_code = status)

    print('Funcion objetivo: ',objective_value)
    print('Status solucion: ',status_string,'(' + str(status) + ')')

    # Imprimimos las variables usadas.
    for i in range(len(x_variables)):
        # Tomamos esto como valor de tolerancia, por cuestiones numericas.
        if x_variables[i] > TOLERANCE:
            print('x_' + str(data.items[i].index) + ':' , x_variables[i])

def main():
    
    # Obtenemos los datos de la instancia.
    data = get_instance_data()
    # ~ print(vars(data))
    # ~ for orden in data.ordenes:
        # ~ print(vars(orden))
    #return
    
    # Definimos el problema de cplex.
    prob_lp = cplex.Cplex()
    
    # Armamos el modelo.
    populate_by_row(prob_lp,data)

    # Resolvemos el modelo.
    solve_lp(prob_lp,data)


if __name__ == '__main__':
    main()