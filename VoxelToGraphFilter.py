#!/usr/bin/env python

import vtk
from vtk import *
import datetime

filename = "sample_data/miednica_2_5.vtk"

reader = vtk.vtkStructuredPointsReader()
reader.SetFileName(filename)
reader.Update()

structuredPoints = reader.GetOutput()

indexes = []
for i in range(0, structuredPoints.GetNumberOfPoints() - 1):
    if (structuredPoints.GetPointData().GetScalars().GetTuple(i)[0] == 1.0):
        indexes.append(i)

degree  = vtk.vtkIntArray()
degree.SetNumberOfComponents(1)
degree.SetName("value")
degree.SetNumberOfTuples(len(indexes))
for i in range(0, len(indexes)):
    degree.SetValue(i, 1)



Points = vtk.vtkPoints()

for i in range(0, len(indexes) - 1):
    Points.InsertNextPoint(structuredPoints.GetPoint(indexes[i]))
line = vtk.vtkCellArray()

for i in range(0, len(indexes) - 1):
    index = -1
    distance = float("inf")
    record = float("inf")
    for j in range(0, len(indexes) - 1):
        distance = vtk.vtkMath.Distance2BetweenPoints(Points.GetPoint(i), Points.GetPoint(j))
        if (distance > 0 and distance < record):
            record = distance
            index = j
    if (index != -1):
        line.InsertNextCell(2)
        line.InsertCellPoint(i)
        line.InsertCellPoint(index)

G = vtk.vtkUnstructuredGrid()
G.GetPointData().SetScalars(degree)
G.SetPoints(Points)
G.SetCells(vtk.VTK_LINE, line)

gw = vtk.vtkXMLUnstructuredGridWriter()
gw.SetFileName("vertex.vtu")
gw.SetInputData(G)
gw.Write()

g = vtk.vtkMutableDirectedGraph()
vertexes = []
for i in range(0, len(indexes) - 1):
    vertexes.append(g.AddVertex())

for i in range(0, len(indexes) - 1):
    index = -1
    distance = float("inf")
    record = float("inf")
    for j in range(0, len(indexes) - 1):
        distance = vtk.vtkMath.Distance2BetweenPoints(Points.GetPoint(i), Points.GetPoint(j))
        if (distance > 0 and distance < record):
            record = distance
            index = j
    if (index != -1):
        g.AddGraphEdge(vertexes[i], vertexes[index])

graphLayoutView = vtk.vtkGraphLayoutView()
graphLayoutView.AddRepresentationFromInput(g)
graphLayoutView.SetLayoutStrategy("Simple 2D")
graphLayoutView.ResetCamera()
graphLayoutView.Render()

graphLayoutView.GetLayoutStrategy().SetRandomSeed(0)

graphLayoutView.GetInteractor().Start()

