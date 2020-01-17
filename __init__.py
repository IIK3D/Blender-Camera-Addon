'''
Copyright (C) 2014 Jacques Lucke
mail@jlucke.com

Created by Jacques Lucke

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys, os, bpy
sys.path.append(os.path.dirname(__file__)) 
import target_camera
from interface import *


bl_info = {
	"name":        "Sniper",
	"description": "Professional camera animations for motion graphics.",
	"author":      "Jacques Lucke, IK3D",
	"version":     (1, 4, 0),
	"blender":     (2, 81, 0),
	"location":    "View 3D > Tool Shelf > Animation/Sniper",
	"category":    "Animation"
	}
	


classes = (
	TextToNameOperator,
	SeperateTextOperator,
	AddTargetCamera,
	SetupTargetObject,
	DeleteTargetOperator,
	RecalculateAnimationOperator,
	MoveTargetUp,
	MoveTargetDown,
	SelectTarget,
	GoToNextTarget,
	GoToPreviousTarget,
	CopyInterpolationPropertiesToAll,
	OpenDopeSheet,

	CAMERATOOLS_PT_view3d_panel,
	TARGETCAMERA_PT_view3d_panel,
)




#registration

def register():
	from bpy.utils import register_class
	for clss in classes:
		try:
			register_class(clss)
		except Exception as e:
			print(clss)



def unregister():    
	from bpy.utils import unregister_class
	for clss in reversed(classes):
		try:
			unregister_class(clss)
		except Exception as e:
			print(clss)

if __name__ == "__main__":
	register()
