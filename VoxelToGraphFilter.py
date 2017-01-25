#!/usr/bin/env python

import vtk
from vtk import *
import math
import datetime


def createGraph(points):
    g = vtk.vtkMutableDirectedGraph()
    vertexes = []
    alreadyConnected = []

    for i in range(0, points.GetNumberOfPoints()):
        vertexes.append(g.AddVertex())
        alreadyConnected.append(i)

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

    graphLayoutView = vtk.vtkGraphLayoutView()
    graphLayoutView.AddRepresentationFromInput(g)
    graphLayoutView.SetLayoutStrategy("Simple 2D")
    graphLayoutView.ResetCamera()
    graphLayoutView.Render()

    graphLayoutView.GetLayoutStrategy().SetRandomSeed(0)

    graphLayoutView.GetInteractor().Start()

def visualize(points):
    alreadyConnected = []

    for i in range(0, points.GetNumberOfPoints()):
        alreadyConnected.append(i)

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
            line.InsertNextCell(2)
            line.InsertCellPoint(i)
            line.InsertCellPoint(index)

    for i in range(0, points.GetNumberOfPoints()):
        index = -1
        distance = float("inf")
        distanceOrder = 0
        record = float("inf")

        for j in range(0, points.GetNumberOfPoints()):
            distance = vtk.vtkMath.Distance2BetweenPoints(points.GetPoint(i), points.GetPoint(j))
            if (distance > 0 and distance < record and alreadyConnected[j] != i and alreadyConnected[i] != j
                and alreadyConnected[alreadyConnected[j]] != alreadyConnected[alreadyConnected[i]]):
                record = distance
                index = j
            elif (distance > 0 and distance < record):
                distanceOrder += 1
        if (index != -1 and distanceOrder < 2):
            alreadyConnected[i] = index
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

filename = "sample_data/miednica_2_5.vtk"

reader = vtk.vtkStructuredPointsReader()
reader.SetFileName(filename)
reader.Update()

structuredPoints = reader.GetOutput()

indexes = []
for i in range(0, structuredPoints.GetNumberOfPoints() - 1):
    if (structuredPoints.GetPointData().GetScalars().GetTuple(i)[0] > 0):
        indexes.append(i)

degree  = vtk.vtkFloatArray()
degree.SetNumberOfComponents(1)
degree.SetName("value")
degree.SetNumberOfTuples(len(indexes))
for i in range(0, len(indexes)):
    degree.SetValue(i, structuredPoints.GetPointData().GetScalars().GetTuple(indexes[i])[0])



Points = vtk.vtkPoints()

for i in range(0, len(indexes) - 1):
    Points.InsertNextPoint(structuredPoints.GetPoint(indexes[i]))
line = vtk.vtkCellArray()

visualize(Points)
createGraph(Points)