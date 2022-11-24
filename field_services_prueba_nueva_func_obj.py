# -*- coding: utf-8 -*-
"""field_services_prueba_nueva func obj.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nk4El8M_cYh6xj1Wg6-w2VJk1AZSF49e
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
        self.nombres_variables = []

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

      # Restricción una orden se puede hacer en un único turno y día (equivalencia de gammas y epsilon).

      for n in range(len(data.ordenes)):
        variables_epsilon = []
        for d in range(data.dias):
          for t in range(data.turnos):
            variables_gamma = []
            variables_gamma.append('gamma'+'_'+str(n))
            variables_epsilon.append('e'+'_'+str(d)+'_'+str(t)+'_'+str(n))
            values = [1]*len(variables_gamma) + [-1]*len(variables_epsilon)
        row = [variables_gamma + variables_epsilon, values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=['E'], rhs=[0.0])

      
      # Restricción: No se pueden realizar varias ordenes en un mismo turno si comparten trabajadores             

     
      for j in range(data.cantidad_trabajadores):
        for d in range(data.dias):
          for t in range(data.turnos):
            variables_restriccion = []
            for n in range(len(data.ordenes)):
              variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
              values = [1]*len(variables_restriccion)
            row = [variables_restriccion, values]
            my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[1.0])


      for t in range(data.turnos):
        for d in range(data.dias):
          for n in range(len(data.ordenes)):
            variables_epsilon = []
            variables_restriccion = []
            for j in range(data.cantidad_trabajadores):
              variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
              values_restriccion = [1]*len(variables_restriccion)
            variables_epsilon.append('e'+'_'+str(d)+'_'+str(t)+'_'+str(n))
            values_epsilon = [(-1) * (data.ordenes[n].trabajadores_necesarios) * len(variables_epsilon)]
            row = [variables_restriccion + variables_epsilon, values_restriccion + values_epsilon]
            my_problem.linear_constraints.add(lin_expr=[row], senses=['E'], rhs=[0.0])


      # Restricción "Una orden de trabajo debe tener asignada sus To trabajadores en un mismo turno para poder ser resuelta"      


      for n in range(len(data.ordenes)):
        variables_restriccion = []
        variables_gamma = []
        for j in range(data.cantidad_trabajadores):
          for d in range(data.dias):
            for t in range(data.turnos):
              variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
              values_restriccion = [1] * len(variables_restriccion)
        variables_gamma.append('gamma'+'_'+str(n))
        values_gamma = [(-1) * (data.ordenes[n].trabajadores_necesarios) * len(variables_gamma)]
        row = [variables_restriccion + variables_gamma, values_restriccion + values_gamma]
        my_problem.linear_constraints.add(lin_expr=[row], senses=['E'], rhs=[0.0])


      # Restricción "Ninǵun trabajador puede trabajar los 6 días de la semana"

      for j in range(data.cantidad_trabajadores):
        variables_restriccion_z = []
        for d in range(data.dias):
          variables_restriccion_z.append('z'+'_'+str(j)+'_'+str(d))
          values = [1]*len(variables_restriccion_z)
        row = [variables_restriccion_z, values]
        my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[5.0])

      for j in range(data.cantidad_trabajadores):
        for d in range(data.dias):
          variables_restriccion = []
          variables_z = []
          for t in range(data.turnos):
            for n in range(len(data.ordenes)):
              variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
              values_restriccion = [1]*len(variables_restriccion)
          variables_z.append('z'+'_'+str(j)+'_'+str(d))
          values_z = [-5] * len(variables_z)
          row = [variables_restriccion + variables_z, values_restriccion + values_z]
          my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[0.0])        


     # Restricción "Ninǵun trabajador puede trabajar los 5 turnos de un día"

      for j in range(data.cantidad_trabajadores):
        for d in range(data.dias):
          variables_restriccion = []
          for t in range(data.turnos):
            for n in range(len(data.ordenes)):
              variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
              values_restriccion = [1]*len(variables_restriccion)
          row = [variables_restriccion, values_restriccion]
          my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[4.0])


    # Restricción “Existen algunos pares de  ́ordenes de trabajo correlativas” 
      for d in range(data.dias):
        for t in range(data.turnos-1):
          for n in range(len(data.ordenes_correlativas)):
            variables_epsilon_1 = []
            variables_epsilon_1.append('e'+'_'+str(d)+'_'+str(t)+'_'+str(data.ordenes_correlativas[n][0]))
            values_epsilon_1 = [1]*len(variables_epsilon_1)
            variables_epsilon_2 = []
            variables_epsilon_2.append('e'+'_'+str(d)+'_'+str(t+1)+'_'+str(data.ordenes_correlativas[n][1]))
            values_epsilon_2 = [-1]*len(variables_epsilon_2)
            row = [variables_epsilon_1 + variables_epsilon_2, values_epsilon_1 + values_epsilon_2]
            my_problem.linear_constraints.add(lin_expr=[row], senses=["E"], rhs=[0.0])
            
      # La orden correlativa nro 1 no se puede realizar el último de un día
        variables_epsilon_1 = []
        variables_epsilon_1.append('e'+'_'+str(d)+'_'+str(data.turnos-1)+'_'+str(data.ordenes_correlativas[n][0]))
        values_epsilon_1 = [1]*len(variables_epsilon_1)
        row = [variables_epsilon_1,values_epsilon_1]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["E"], rhs=[0.0])

      # La orden correlativa nro 2 no se puede realizar en el primer turno del día  

        variables_epsilon_2 = []
        variables_epsilon_2.append('e'+'_'+str(d)+'_'+str(0)+'_'+str(data.ordenes_correlativas[n][1]))
        values_epsilon_2 = [1]*len(variables_epsilon_2)  
        row = [variables_epsilon_2,values_epsilon_2]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["E"], rhs=[0.0])


      # Restricción “Hay pares de órdenes de trabajo que no pueden ser satisfechas en turnos consecutivos de un mismo trabajador”

      for j in range(data.cantidad_trabajadores):
        for d in range(data.dias):
          for t in range(data.turnos-1):
            for n in range(len(data.ordenes_conflictivas)):
              variables_restriccion_1 = []
              variables_restriccion_1.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(data.ordenes_conflictivas[n][0]))
              values_1 = [1] * len(variables_restriccion_1)
              variables_restriccion_2 = []
              variables_restriccion_2.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t+1)+'_'+str(data.ordenes_conflictivas[n][1]))
              values_2 = [-1] * len(variables_restriccion_2)
            row = [variables_restriccion_1 + variables_restriccion_2, values_1 + values_2]
            my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[1])

          for t in range(data.turnos - 1,0,-1):
            for n in range(len(data.ordenes_conflictivas)):
              variables_restriccion_1 = []
              variables_restriccion_1.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(data.ordenes_conflictivas[n][0]))
              values_1 = [1] * len(variables_restriccion_1)
              variables_restriccion_2 = []
              variables_restriccion_2.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t-1)+'_'+str(data.ordenes_conflictivas[n][1]))
              values_2 = [-1] * len(variables_restriccion_2)
            row = [variables_restriccion_1 + variables_restriccion_2, values_1 + values_2]
            my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[1])



      #Equivalencia entre x y v

      for j in range(data.cantidad_trabajadores):
        variables_x_j = []
        variables_restriccion = []
        for t in range(data.turnos):
          for d in range(data.dias):
            for n in range(len(data.ordenes)):
              variables_restriccion.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
              values_restriccion = [1] * len(variables_restriccion)
        variables_x_j.append('x'+'_'+str(j))
        values_x_j = [-1] * len(variables_x_j)        
        row = [variables_restriccion + variables_x_j, values_restriccion + values_x_j]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["E"], rhs=[0.0])

      for j in range(data.cantidad_trabajadores):
        variables_x_j = []
        variables_x_j_k = []
        for k in range(len(data.costos)):
          variables_x_j_k.append('x'+'_'+str(j)+'_'+str(k))
          values_x_j_k = [1] * len(variables_x_j_k)
        variables_x_j.append('x'+'_'+str(j))
        values_x_j = [-1] * len(variables_x_j)
        row = [variables_x_j_k + variables_x_j, values_x_j_k + values_x_j]
        my_problem.linear_constraints.add(lin_expr=[row], senses=["E"], rhs=[0.0])


    #1er tramo
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
          values_1 = [1,-1]
          row_1 = [[variables_w[1], variables_w[0]], values_1]
          my_problem.linear_constraints.add(lin_expr=[row_1], senses=['L'], rhs=[0.0])
          values_2 = [1,-1]
          row_2 = [[variables_w[2], variables_w[1]], values_2]
          my_problem.linear_constraints.add(lin_expr=[row_2], senses=['L'], rhs=[0.0])
          values_3 = [1,-1]
          row_3 = [[variables_w[3], variables_w[2]], values_3]
          my_problem.linear_constraints.add(lin_expr=[row_3], senses=['L'], rhs=[0.0])


       # Restriccion deseable: Conflictos entre trabajadores

      for t in range(data.turnos):
        for d in range(data.dias):
          for n in range(len(data.ordenes)):
            for j in range(len(data.conflictos_trabajadores)): 
              variables_restriccion_0 = []
              variables_restriccion_1 = []
              variables_restriccion_0.append('v'+'_'+str(data.conflictos_trabajadores[j][0])+'_'+str(d)+'_'+str(t)+'_'+str(n))
              variables_restriccion_1.append('v'+'_'+str(data.conflictos_trabajadores[j][1])+'_'+str(d)+'_'+str(t)+'_'+str(n))
              values_0 = [1] * len(variables_restriccion_0)
              values_1 = [1] * len(variables_restriccion_1)
              row = [variables_restriccion_0 + variables_restriccion_1,values_0 + values_1]
              my_problem.linear_constraints.add(lin_expr=[row], senses=["L"], rhs=[1])


       # Restriccion deseable: Hay pares de  ́ordenes de trabajo que son repetitivas por lo que ser ́ıa bueno que un mismo trabajador no sea asignado a ambas. 

      for n in range(len(data.ordenes_repetitivas)):  
        for j in range(data.cantidad_trabajadores):
          variables_restriccion_0 = []
          variables_restriccion_1 = []
          for d in range(data.dias):
            for t in range(data.turnos):
              variables_restriccion_0.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(data.ordenes_repetitivas[n][0]))
              variables_restriccion_1.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(data.ordenes_repetitivas[n][1]))
              values = [1]*len(variables_restriccion_0) + [1] * len(variables_restriccion_1)
              row = [variables_restriccion_0 + variables_restriccion_1, values]
              my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[1.0])      



      # Restricción “Diferencia entre el trabajador con más órdenes asignadas y el trabajador con menos órdenes no puede ser mayor a 10"

      for j in range(data.cantidad_trabajadores):
        variables_costos = []
        variables_costos.append('x'+'_'+str(j))
        for jj in range(data.cantidad_trabajadores):
          if j != jj:
            variables_costos_2 = []
            variables_costos_2.append('x'+'_'+str(jj))
            values = [1]*len(variables_costos) + [-1]*len(variables_costos_2)
            row = [variables_costos + variables_costos_2, values]
            my_problem.linear_constraints.add(lin_expr=[row], senses=['L'], rhs=[10])
            my_problem.linear_constraints.add(lin_expr=[row], senses=['G'], rhs=[-10])
          else:
            continue

def populate_by_row(my_problem, data):

    # Definimos y agregamos las variables.

    coeficientes_beneficio = []
#    for j in range(data.cantidad_trabajadores): 
#      for d in range(data.dias):
#        for t in range(data.turnos):
    for n in range(len(data.ordenes)):
      coeficientes_beneficio.append(data.ordenes[n].beneficio)
    #coeficientes_costo = list(np.tile(data.costos, data.cantidad_trabajadores))
    coeficientes_funcion_objetivo = coeficientes_beneficio 
    #+ coeficientes_costo

    variables_gamma = []
    for n in range(len(data.ordenes)):
      data.nombres_variables.append('gamma'+'_'+str(n))
      variables_gamma.append('gamma'+'_'+str(n))
    
    

        
#    my_problem.variables.add(obj = coeficientes_funcion_objetivo, lb =[0]*len(coeficientes_beneficio) + [0]*len(coeficientes_costo), ub = [1]*len(coeficientes_beneficio) + list(np.tile(data.trozos, data.cantidad_trabajadores))
#                             , types=['B']*len(coeficientes_beneficio) + ['I']*len(coeficientes_costo), names = (variables_gamma + variables_costos))
    


    my_problem.variables.add(obj = coeficientes_funcion_objetivo, lb =[0]*len(coeficientes_beneficio), ub = [1]*len(coeficientes_beneficio)
                             , types=['B']*len(coeficientes_beneficio), names = variables_gamma)
    





    # Columna para v_j_d_t_n
    variables_beneficios = []
    for j in range(data.cantidad_trabajadores): 
      for d in range(data.dias):
        for t in range(data.turnos):
          for n in range(len(data.ordenes)):
            data.nombres_variables.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))
            variables_beneficios.append('v'+'_'+str(j)+'_'+str(d)+'_'+str(t)+'_'+str(n))


    my_problem.variables.add(obj = [0.0] * len(variables_beneficios), lb =[0]*len(variables_beneficios) , ub = [1]*len(variables_beneficios)
                             , types=['B']*len(variables_beneficios), names = variables_beneficios)




    




    # Columna para epsilon_d_t_n

    variables_epsilon = []
    for d in range(data.dias):
      for t in range(data.turnos):
        for n in range(len(data.ordenes)):
          data.nombres_variables.append('e'+'_'+str(d)+'_'+str(t)+'_'+str(n))
          variables_epsilon.append('e'+'_'+str(d)+'_'+str(t)+'_'+str(n))

    my_problem.variables.add([0.0] * len(variables_epsilon), lb = [0] * len(variables_epsilon), ub = [1]*len(variables_epsilon), types= ['B']*len(variables_epsilon), names = variables_epsilon)


    # Columna para Z_j_d
    variable_z = []
    for j in range(data.cantidad_trabajadores):
      for d in range(data.dias):
        data.nombres_variables.append('z'+'_'+str(j)+'_'+str(d))
        variable_z.append('z'+'_'+str(j)+'_'+str(d))

    my_problem.variables.add(obj = [0.0] * len(variable_z), lb = [0]*len(variable_z), ub = [1]*len(variable_z), types= ['B']*len(variable_z), names = variable_z)



    # Columna para x_j_k (cantidad de ordenes por trabajador y tramo)  
    variables_costos = []
    for j in range(data.cantidad_trabajadores):
      for k in range(len(data.costos)):
        data.nombres_variables.append('x'+'_'+str(j)+'_'+str(k))
        variables_costos.append('x'+'_'+str(j)+'_'+str(k))

    coeficientes_costo = list(np.tile(data.costos, data.cantidad_trabajadores)) 
    my_problem.variables.add(obj = coeficientes_costo, lb = [0]*len(coeficientes_costo), ub = list(np.tile(data.trozos, data.cantidad_trabajadores))
                            , types= ['I']*len(coeficientes_costo), names = variables_costos)


    # Columna para x_j (suma de ordenes por trabajador)

    variables_x_j = []
    for j in range(data.cantidad_trabajadores):
        data.nombres_variables.append('x'+'_'+str(j))
        variables_x_j.append('x'+'_'+str(j))


    my_problem.variables.add(obj = [0.0] * len(variables_x_j), lb = [0]*len(variables_x_j), ub = [data.cantidad_ordenes] * data.cantidad_trabajadores
                            , types= ['I']*len(variables_x_j), names = variables_x_j)
    

    # Columna para w_j_k
    
    variables_w = []
    for j in range(data.cantidad_trabajadores):
      for k in range(len(data.costos)):
        data.nombres_variables.append('w'+'_'+str(j)+'_'+str(k))
        variables_w.append('w'+'_'+str(j)+'_'+str(k))
        
    my_problem.variables.add([0.0] * len(variables_w), lb = [0]*len(variables_w), ub = [1]*len(variables_w), types= ['B']*len(variables_w), names = variables_w)

    # Seteamos direccion del problema
    my_problem.objective.set_sense(my_problem.objective.sense.maximize)
    # ~ my_problem.objective.set_sense(my_problem.objective.sense.minimize)

    # Definimos las restricciones del modelo. Encapsulamos esto en una funcion. 
    add_constraint_matrix(my_problem, data)

    # Exportamos el LP cargado en myprob con formato .lp. 
    # Util para debug.
    my_problem.write('field_services_prueba.lp')

def solve_lp(my_problem, data):
    
    # Resolvemos el ILP.
    
    my_problem.solve()

    # Obtenemos informacion de la solucion. Esto lo hacemos a traves de 'solution'. 
    #x_variables = my_problem.solution.get_values()
    
    objective_value = my_problem.solution.get_objective_value()
    status = my_problem.solution.get_status()
    status_string = my_problem.solution.get_status_string(status_code = status)

    print('Funcion objetivo: ',objective_value)
    print('Status solucion: ',status_string,'(' + str(status) + ')')

    x = my_problem.solution.get_values(0, my_problem.variables.get_num()-1)
    for j in range(my_problem.variables.get_num()):
      print(j, x[j])

    # Imprimimos las variables usadas.
#    for i in range(len(x_variables)):
        # Tomamos esto como valor de tolerancia, por cuestiones numericas.
        #if x_variables[i] > TOLERANCE:
            #print('x_' + str(data.items[i].index) + ':' , x_variables[i])
#      print(prob_lp.variables.get_num() + ':', x_variables[i])
            #print(x_variables[i])

    with open("resultado.txt","w") as archivo:
      for i in range(len(x_variables)):
            # Tomamos esto como valor de tolerancia, por cuestiones numericas.
        if x_variables[i] > TOLERANCE:
          archivo.write(f"{data.nombres_variables[i]}:{x_variables[i]}\n")
                # print(str(data.names[i]) + ':' , x_variables[i])        

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