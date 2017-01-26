# Opis działania programu

Program zaczyna swoje działanie od pobrania pliku wejściowego oraz nazwy pliku, do którego zostanie zapisany wynik działania programu.
``` python
filename = sys.argv[1]
outputFileName = sys.argv[2]
```

Inicjalizujemy vtkStructuredPointsReader i wczytujemy plik

``` python
reader = vtk.vtkStructuredPointsReader()
reader.SetFileName(filename)
reader.Update()

structuredPoints = reader.GetOutput()
```

Tworzymy tablicę do przechowywania indeksów punktów, których wartośc jest większa od 0

```python
indexes = []
for i in range(0, structuredPoints.GetNumberOfPoints() - 1):
    if (structuredPoints.GetPointData().GetScalars().GetTuple(i)[0] > 0):
```

Tworzymy tablicę do przechowywanie wartości punktów z tablicy indexes

```python
degree  = vtk.vtkFloatArray()
degree.SetNumberOfComponents(1)
degree.SetName("value")
degree.SetNumberOfTuples(len(indexes))
for i in range(0, len(indexes)):
    degree.SetValue(i, structuredPoints.GetPointData().GetScalars().GetTuple(indexes[i])[0])
    
```
 
Tworzymy strukturę vtkPoints do której insertujemy punkty z tablicy indexes
```python
Points = vtk.vtkPoints()

for i in range(0, len(indexes) - 1):
    Points.InsertNextPoint(structuredPoints.GetPoint(indexes[i]))
```
 
Inicjujemy tablicę komórek, a następnie wywołujemy funkcje
``` python
line = vtk.vtkCellArray()

visualize(Points)
createGraph(Points)
```

Algorytm łączenia punktów w obu funkcjach jest identyczny pod względem logicznym, różni się jedynie dodawaniem punktów do struktur

## Działanie algorytmu łączenia punktów na przykładzie funkcji tworzącej graf 2D

Tworzymy strukturę vtkMutableDirectedGraph oraz dwie tablice:
  - vertexes - do przechowywania węzłów grafu
  - alreadyConnected - do przechowywania informacji o istniejących połączeniach

``` python

g = vtk.vtkMutableDirectedGraph()
vertexes = []
alreadyConnected = []
    
```

Wypełniamy tablice domyślnymi danymi

``` python

for i in range(0, points.GetNumberOfPoints()):
    vertexes.append(g.AddVertex())
    alreadyConnected.append(i)
```

### Część odpowiadająca za wyszukiwanie połączeń

``` python
    for i in range(0, points.GetNumberOfPoints()):
        index = -1
        distance = float("inf")
        distanceOrder = 0
        record = float("inf")

        for j in range(0, points.GetNumberOfPoints()):
            distance = math.sqrt(vtk.vtkMath.Distance2BetweenPoints(points.GetPoint(i), points.GetPoint(j)))
            if (distance > 0 and distance < record and alreadyConnected[j] != i and alreadyConnected[alreadyConnected[j]] != i):
                record = distance
                index = j
            elif (distance > 0 and distance < record):
                distanceOrder += 1
        if (index != -1 and distanceOrder < 2):
            alreadyConnected[i] = index
            g.AddGraphEdge(vertexes[i], vertexes[index])

    for i in range(0, points.GetNumberOfPoints()):
        index = -1
        distance = float("inf")
        distanceOrder = 0
        record = float("inf")

        for j in range(0, points.GetNumberOfPoints()):
            distance = math.sqrt(vtk.vtkMath.Distance2BetweenPoints(points.GetPoint(i), points.GetPoint(j)))
            if (distance > 0 and distance < record and alreadyConnected[j] != i and alreadyConnected[i] != j
                and alreadyConnected[alreadyConnected[j]] != alreadyConnected[alreadyConnected[i]]):
                record = distance
                index = j
            elif (distance > 0 and distance < record):
                distanceOrder += 1
        if (index != -1 and distanceOrder < 2):
            alreadyConnected[i] = index
            g.AddGraphEdge(vertexes[i], vertexes[index])
            
```

Algorytm składa się z dwóch przebiegów, gdzie w każdym iterujemy po całej tablicy.

W pierwszym przebiegu, dla każdego punktu przechodzimy przez wszystkie punkty, w celu znalezienia punktu leżącego najbliżej, który jednocześnie nie jest już połączony z punktem, który obecnie rozważamy (points.GetPoint(i)), oraz punkt z którym znaleziony punkt jest połączony nie jest połączony z obecnie rozważanym punktem.

Jeżeli znajdziemy taki punkt, to zapisujemy jego indeks oraz dystans do obecnie rozważanego punktu.

Po przejsciu przez wszystkie punkty, jeżeli znaleźliśmy punkt oraz distanceOrder < 2, łączymy roważany punkt z najlepiej dopasowanym innym punktem.

W drugim przebiegu dodajemy warunki, aby nie tworzyć niepotrzebnych połączeń.
