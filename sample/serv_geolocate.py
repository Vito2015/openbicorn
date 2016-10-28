#!/usr/bin/env python
# coding: utf-8
import os
import sys
sys.path.append('./gen-py')

from geolocate import Geolocate
from geolocate.ttypes import *


class GeolocateHandler:

  def calculatePosition(self, arr_cell, arr_wifi):
    arr_cell = arr_cell or []
    arr_wifi = arr_wifi or []
    len_cell = len(arr_cell)
    len_wifi = len(arr_wifi)
    avg_lng, avg_lat = 0, 0
    for cell in arr_cell:
      avg_lng += cell.lng
      avg_lat += cell.lat

    avg_lng /= len_cell
    avg_lat /= len_cell

    return Location(lat=avg_lat, lng=avg_lng)


service = Geolocate.Processor(GeolocateHandler())
