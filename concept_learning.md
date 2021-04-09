# Introduccion.

Un sistema que aprende tiene 4 aspectos:

1. Datos (obtencion de datos, que sirvan para aprender, con una buena representacion)
2. Un tipo de funcion que va a tratar de aprender (tipicamente llamada hipotesis),
	el conjunto de estas funciones se llama espacio de hipotesis.
3. El tipo de busqueda que voy a hacer (como voy a encontrar la solucion, ej. polinomios). Por lo tanto, aprender
	es de una manera encontrar una buena solucion para el espacio de datos (minimos cuadrados para los polinomios).
4. Evitar el problema de sobreajuste, como elegir la mejor solucion sobre la sobreajustada.

# Concept learning:
Metodos para inferir funciones booleanas, a partir del ejemplos de entrenamiento. Por ejemplo determinar dado
ciertos atributos (numero de patas, pelo, etc.) si es un gato o no.

El concepto (booleano) es el que queremos adivinar.

- El espacio de hipostesis:
Se puede representar como conjuncion de ands de todas las variables.
Tambien se puede determinar que algunas variables no son irrelevantes: ?.

Por ejemplo: h = (? , Cold, High ~, ?) ; 
	? indica que cualquier valor es aceptable (el atributo no es relevante.)
	~ indica que no es verdadero, no acepta valores en ese atributo.
* h(x) = 1 si x satisface todas las restricciones, 0 en otro caso.
* La hipotesis mas general es: (?, ?, ..., ?) y la mas especifica (~,~, ..., ~)

Notacion:
- X es el conjunto de datos medidos.
- c es el concepto objetivo.
- {x, c(x)}, conjunto de ejemplos de entrenamientos.
- D contenido en X x {0,1}, conjunto de datos (universo)
- H es el conjunto de todas las posibles hipotesis.
- h \in H h: X -> {0, 1}.

El objetivo es encontrar h / h(x) = c(x).
Para aprender de esta manera, estamos haciendo induccion.

- Una hipotesis h aproxima bien al objetivo c, ajusta a c en el conjunto de datos que tengo, mientras mas grande
sea el espacio de instancias, mejor es el ajuste.

Se deben ordenar las hipotesis, de lo mas general a lo mas especifico.

Encontrando la hipotesis mas especifica que sea compatible con nuestros datos. Algoritmo Find-S.

De esta manera, conseguimos corverger a un concepto correcto? Encontramos una hipotesis final que 
es lo mas especifica posible y clasifica todos los ejemplos positivos son positivos.

Porque preferir la hipotesis especifica? No, no hay nada que diga que una h mas especifica sea
mejor que la mejor.

Los ejemplos de entrenamientos, son consistentes? No podemos saberlo, ya que la hipotesis no garantiza que los 
ejemplos negativos den negativo. 

Un algoritmo mejor es el: Version Spaces & Candidate-Elimination Algorithm, que mantiene un conjunto de hiposesis
consistentes con nuestros ejemplos. 

h hipotesis es consistente con el dataset si para todos los puntos (negativos o positivos) la clase que le asigna
la hipotesis al concepto. Consistent(h,D) === \forall {x, c(x)} \in D h(x) = c(x)

El espacion de versiones es el conjunto de todas las hipotesis h que son consistentes con nuestro dataset.

Eliminamos las hipotesis todas las hipotesis que no son consistentes, pero no es una solucion elegante.

Una solucion mejor es mantener el espacio de versiones por sus limites. Limite mas general y limite mas especifico.
Conjunto de h mas generales consistentes y conjunto de h mas especificos consistentes. 

Este algoritmo, en principio es mejor que el anterior.
- Converge a la respuesta correcta, si los datos son correctos y la respuesta está dentro de los datos. Si, el concepto 
original no estaba en los ejemplos entonces entonces va a converger al conjunto vacio.

- El ejemplo que mas informacion tiene es el mejor ejemplo para aprender (el que elimina mas hipotesis).

- Los conceptos "parcialmente aprendido" sirve para estimar una probabilidad.

Un bías es la forma en la cual representamos nuestro espacio de conceptos. Al elegir un bias puede que estemos dejando
conceptos afuera, como oucrre al usar el bias de las conjunciones contra el de las disyunciones.
 
El unbiased, espacio de conceptos mas general posible. Se obtiene calculando el conjunto de partes de X.


