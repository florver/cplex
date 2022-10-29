import sys
import cplex
from recordclass import recordclass

Item = recordclass('Item', 'index value weight')

TOLERANCE =10e-6 

class KnapsackInstance:
    def __init__(self):
        self.n = 0
        self.b = 0
        self.items = []

    def load(self,filename):

        # Abrimos el archivo.
        f = open(filename)

        # Leemos la primera linea con los parametros generales.
        row = f.readline().split(' ')
        self.n = int(row[0])
        self.b = int(row[1])
        self.items = []

        # Leemos informacion de los items.
        for i in range(self.n):
            row = f.readline().split(' ')
            self.items.append(Item(i, int(row[0]), int(row[1])))
            
        # Ordenamos los items por su relacion peso/beneficio.
        self.items = sorted(self.items,key=lambda Item: Item.weight/Item.value)
        
        # Cerramos el archivo.
        f.close()


def get_instance_data():
    file_location = sys.argv[1].strip()
    instance = KnapsackInstance()
    instance.load(file_location)
    return instance
    

def add_constraint_matrix(my_problem, data):
    # De manera analoga a las variables, usamos linear_constraints y el correspondiente
    # metodo 'add' para agregarlas. 
    # Para las restricciones ax <= b necesitamos indicar:
    # - el vector de coeficientes a. Esto se hace con dos vectores: uno de indices (ind)
    #   y otro de valores (val). Una fila, entonces, es una lista de listas [ind,val].
    #   El parametro en este caso es 'lin_expr'.
    # - el sentido de la desigualdad: <= (L), >= (G), = (E). El parametro es 'sense'. 
    # - el valor 'b'. el parametro es 'rhs'. 
    # Observacion: notar que cplex expera "una matriz de restricciones", es decir, una
    # lista de restricciones del tipo ax <= b, [ax <= b]. Por lo tanto, aun cuando
    # agreguemos una unica restriccion, tenemos que hacerlo como una lista de un unico
    # elemento.
    
    # Agregamos restriccion de capacidad.
    indices = ...
    values = ...
    
    row = [indices,values]
    my_problem.linear_constraints.add(lin_expr=[row], senses=[...], rhs=[...])

def populate_by_row(my_problem, data):

    # Primero: definir y agregar las variables. Para eso se utiliza la
    # funcion 'add' de la interfaz 'variables', que permite modificar
    # esta informacion.
    # una forma simple es definirlas en funcion de vector de coeficientes 
    # con los costos de la funcion objetivo (obj = c), el de cotas inferiores (lb = 0),
    # y el de cotas superiores (ub = maxp).
    coeficientes_funcion_objetivo = ...
    my_problem.variables.add(obj = coeficientes_funcion_objetivo, lb = [0]*data.n, ub = [1]*data.n, types=['B']*data.n) 

    # Seteamos problema de minimizacion.
    my_problem.objective.set_sense(my_problem.objective.sense.maximize)

    # Segundo: definir las restricciones del modelo. Encapsulamos esto en una funcion. 
    add_constraint_matrix(my_problem, data)

    # Exportamos el LP cargado en myprob con formato .lp. 
    # Util para debug.
    my_problem.write('knapsack.lp')

def solve_lp(my_problem, data):
    
    # Tercero: resolvemos el LP.
    # Definimos los parametros del solver
    
    my_problem.parameters.mip.tolerances.mipgap.set(1e-10)
    
    # Parametros para definir un branch-and-bound puro sin cortes ni heuristicas
    my_problem.parameters.mip.limits.cutpasses.set(-1)
    my_problem.parameters.mip.strategy.heuristicfreq.set(-1)
    
    # Parametro para definir que algoritmo de lp usar
    # ~ my_problem.parameters.lpmethod.set(my_problem.parameters.lpmethod.values.primal)
    
    # Parametro para definir la eleccion de nodo
    # ~ my_problem.parameters.mip.strategy.nodeselect.set(1)
    
    # Parametros para definir la eleccion de variables a branchear
    # ~ my_problem.parameters.mip.strategy.variableselect.set(1)
    # ~ my_problem.parameters.parameters.mip.ordertype.set(1)
    
    
    my_problem.solve()

    # Cuarto: obtenemos informacion de la solucion. Esto lo hacemos a traves de 'solution'. 
    # - los valores de las variables. Usamos las funcion get_values().
    # - el valor del funcional. Usamos get_objective_value()
    # - el status de la solucion. Usamos get_status() 
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
    
    # Definimos el problema de cplex.
    prob_lp = cplex.Cplex()
    
    # Armamos el modelo.
    populate_by_row(prob_lp,data)

    # Resolvemos el modelo.
    solve_lp(prob_lp,data)


if __name__ == '__main__':
    main()
