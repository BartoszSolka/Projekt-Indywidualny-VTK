#!/usr/bin/env python

import vtk
from vtk import *

filename = "sample_data/skel.vtk"

reader = vtk.vtkStructuredPointsReader()
reader.SetFileName(filename)
reader.Update()

structuredPoints = reader.GetOutput()
print structuredPoints
