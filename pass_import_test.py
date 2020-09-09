import c4d
from c4d import gui
from csv import reader
import os
import glob
from os.path import basename
from c4d import gui,storage,documents
import random
# Welcome to the world of Python
import math
c4d.CallCommand(13957, 13957) # Clear Console

  
def calculateDistance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist  

def active():
    return doc.GetFirstObject()

# Main function
def main():
    # gui.MessageDialog('Hello World!')
    txt_fpath = "/Users/DML/OneDrive/Soccer Python/passing-networks-in-python-master/player_info.csv"
    txt_fpath_pass_values = "/Users/DML/OneDrive/Soccer Python/passing-networks-in-python-master/pair_pass_values.csv"

    # Nulls Names
    names = c4d.BaseObject(c4d.Onull)
    names[c4d.ID_BASELIST_NAME] = "Player Names"
    doc.InsertObject(names)
    c4d.EventAdd()
    
    # Nulls Circles
    circles = c4d.BaseObject(c4d.Onull)
    circles[c4d.ID_BASELIST_NAME] = "Player Circles"
    doc.InsertObject(circles)
    c4d.EventAdd()

    with open(txt_fpath, 'r') as read_obj:
        csv_reader = reader(read_obj)
        next(csv_reader)
        for row in csv_reader:
            c4d.CallCommand(5164, 5164) # Disc
            selected = doc.GetActiveObject()
            selected[c4d.PRIM_DISC_ORAD] = float(row[3]) *10
            selected[c4d.PRIM_DISC_IRAD] =  float(row[3]) *10 - 10 - float(row[3]) *3 
            selected[c4d.ID_BASELIST_NAME] = row[0]
            selected[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = 10500*float(row[1]) - 10500/2
            selected[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = 6800*float(row[2]) - 6800/2
          
            selected.InsertUnder(circles) # place in Spline Null Object

            c4d.CallCommand(1019268, 1019268) # MoText
            selected = doc.GetActiveObject()
            selected[c4d.PRIM_TEXT_TEXT] = row[0]
            selected[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X] = -1.571
            selected[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = -1.571
            selected[c4d.PRIM_TEXT_ALIGN] = 1
            selected[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = 10500*float(row[1]) - 10500/2
            selected[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = 6800*float(row[2]) - 6800/2
            selected[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = 200
            selected[c4d.PRIM_TEXT_HEIGHT] = 100
            selected[c4d.MGTEXTOBJECT_SPLINEMOVE] = 0
            selected.InsertUnder(names) # place in Spline Null Object
  
    pointCount = 3
    
    with open(txt_fpath_pass_values, 'r') as read_obj:
        csv_reader = reader(read_obj)
        next(csv_reader)
        
        # Null Passes Low
        spline_null_low = c4d.BaseObject(c4d.Onull)
        spline_null_low[c4d.ID_BASELIST_NAME] = "Null_Spline_Low"
        doc.InsertObject(spline_null_low)
        c4d.EventAdd()
        
        # Null Passes High
        spline_null_high = c4d.BaseObject(c4d.Onull)
        spline_null_high[c4d.ID_BASELIST_NAME] = "Null_Spline_High"
        doc.InsertObject(spline_null_high)
        c4d.EventAdd()
        
        for line in csv_reader:
            
            # PASSES LOW             
            if line[2] > 0:
                for i in range(int(round(float(line[2])))):
                    Spline = c4d.SplineObject(pointCount,0)
            
                    Spline[c4d.SPLINEOBJECT_TYPE] = 3
                    Spline[c4d.SPLINEOBJECT_ANGLE] = 0
                    n = 0
            
                    # start point
                    pos = c4d.Vector()
                    pos.x = float(line[4]) *10500 - 10500/2 
                    pos.y = 0
                    pos.z = float(line[5]) *6800 - 6800/2
                    Spline.SetPoint(n,pos)
                
                    # distance between points 
                    
                    # middle point
                    pos2 = c4d.Vector()
                    pos2.x = ((float(line[4]) + float(line[6])) / 2) *10500 - 10500/2 + random.randint(-100, 100) 
                    pos2.y = 20
                    # pos2.y =  (line[10]*100) +  ((line[10]*100)*0.9) - (52.5 - line[5]) # + random.randint(-100, 200)
                    # pos2.y = ((line[7]+line[10])/2) *100 # (line[10]*100) +  ((line[10]*100)*0.9)
                    pos2.z =  ((float(line[5]) + float(line[7])) / 2) *6800 - 6800/2 + random.randint(-100, 100)   
                    Spline.SetPoint(n+1,pos2)
                    
                    # end point
                    Spline.SetPoint(n,pos)
                    pos3 = c4d.Vector()
                    pos3.x = float(line[6]) *10500 - 10500/2
                    pos3.y = 0
                    pos3.z = float(line[7]) *6800 - 6800/2
                    Spline.SetPoint(n+2,pos3)
                    n+=1
                    
                    # distance between points
                    dist_btw = calculateDistance(pos.x, pos.y, pos3.x, pos3.y)                   
                    doc.InsertObject(Spline,checknames=True)
                    myobject = doc.GetFirstObject()
                    active().InsertUnder(spline_null_low) # place in Spline Null Object
  
            if line[2] > 0:
                
                for i in range(int(round(float(line[3])))):
                    Spline = c4d.SplineObject(pointCount,0)
            
                    Spline[c4d.SPLINEOBJECT_TYPE] = 3
                    Spline[c4d.SPLINEOBJECT_ANGLE] = 0
                    n = 0
                    
                    pos1x = float(line[4]) *10500 - 10500/2
                    pos1z = float(line[5]) *6800 - 6800/2
                    pos3x = float(line[6]) *10500 - 10500/2
                    pos3z = float(line[7]) *6800 - 6800/2
                    
                    
                    # start point
                    pos = c4d.Vector()
                    pos.x =  pos1x
                    pos.y = 0
                    pos.z =  pos1z
                    Spline.SetPoint(n,pos)
                
                    # distance between points 
                    dist_btw = calculateDistance(pos.x, pos.y, pos3.x, pos3.y)
                    # middle point
                    pos2 = c4d.Vector()
                    pos2.x = ((float(line[4]) + float(line[6])) / 2) *10500 - 10500/2 + random.randint(-100, 100) 
                    pos2.y = dist_btw/3 + random.randint(-100, 100)
                    # pos2.y =  (line[10]*100) +  ((line[10]*100)*0.9) - (52.5 - line[5]) # + random.randint(-100, 200)
                    # pos2.y = ((line[7]+line[10])/2) *100 # (line[10]*100) +  ((line[10]*100)*0.9)
                    pos2.z =  ((float(line[5]) + float(line[7])) / 2) *6800 - 6800/2 + random.randint(-100, 100)   
                    Spline.SetPoint(n+1,pos2)
                    
                    
                    
                    
                    # end point
                    Spline.SetPoint(n,pos)
                    pos3 = c4d.Vector()
                    
                    pos3.x = pos3x
                    pos3.y = 0
                    pos3.z = pos3z
                    Spline.SetPoint(n+2,pos3)
                    n+=1
                    
                   
                    
                    

                    
                    
    
                    doc.InsertObject(Spline,checknames=True)
                    myobject = doc.GetFirstObject()

                   
                    active().InsertUnder(spline_null_high) # place in Spline Null Object
                                

                
        # combine null spline low 
        selected = doc.SearchObject("Null_Spline_Low")
        doc.SetActiveObject(selected)
        c4d.CallCommand(100004768, 100004768) # Select Children
        c4d.CallCommand(16768, 16768) # Connect Objects + Delete
        selected = doc.GetActiveObject()
        selected[c4d.SPLINEOBJECT_ANGLE] = 0
        selected[c4d.ID_BASELIST_NAME] = "Null_Spline_Low" 
        
        # combine null spline high 
        selected = doc.SearchObject("Null_Spline_High")
        doc.SetActiveObject(selected)
        c4d.CallCommand(100004768, 100004768) # Select Children
        c4d.CallCommand(16768, 16768) # Connect Objects + Delete
        selected = doc.GetActiveObject()
        selected[c4d.SPLINEOBJECT_ANGLE] = 0
        selected[c4d.ID_BASELIST_NAME] = "Null_Spline_High"   
        
        
        # Nulls Sweep Low
        sweep_low = c4d.BaseObject(c4d.Osweep)
        sweep_low[c4d.ID_BASELIST_NAME] = "Sweep Low"
        doc.InsertObject(sweep_low)
        c4d.EventAdd()
        
        # Nulls Sweep High
        sweep_high = c4d.BaseObject(c4d.Osweep)
        sweep_high[c4d.ID_BASELIST_NAME] = "Sweep High"
        doc.InsertObject(sweep_high)
        c4d.EventAdd()
        
        # Sweep rectangle low
        sweep_rect = c4d.BaseObject(c4d.Osplinerectangle)
        sweep_rect[c4d.PRIM_RECTANGLE_WIDTH] = 4
        sweep_rect[c4d.PRIM_RECTANGLE_HEIGHT] = 4
        sweep_rect[c4d.ID_BASELIST_NAME] = "Sweep Rect"
        doc.InsertObject(sweep_rect)
        c4d.EventAdd()
        
        # Sweep rectangle high
        sweep_rect_high = c4d.BaseObject(c4d.Osplinerectangle)
        sweep_rect_high[c4d.PRIM_RECTANGLE_WIDTH] = 4
        sweep_rect_high[c4d.PRIM_RECTANGLE_HEIGHT] = 4
        sweep_rect_high[c4d.ID_BASELIST_NAME] = "Sweep Rect High"
        doc.InsertObject(sweep_rect_high)
        c4d.EventAdd()
        
        # combine null sweep & rect
        selected = doc.SearchObject("Null_Spline_Low")
        doc.SetActiveObject(selected)
        selected.InsertUnder(sweep_low)

        selected = doc.SearchObject("Sweep Rect")
        doc.SetActiveObject(selected)
        selected.InsertUnder(sweep_low)
        
        selected = doc.SearchObject("Null_Spline_High")
        doc.SetActiveObject(selected)
        selected.InsertUnder(sweep_high)

        selected = doc.SearchObject("Sweep Rect High")
        doc.SetActiveObject(selected)
        selected.InsertUnder(sweep_high)


        


         



# Execute main()
if __name__=='__main__':
    main()
    print('script successful')