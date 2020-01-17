import bpy
from sniper_utils import *
from target_camera import *




# operators
#############################

		
class TextToNameOperator(bpy.types.Operator):
	bl_idname = "sniper.text_to_name"
	bl_label = "Text to Name"
	bl_description = "Rename all text objects to their content."
	
	def execute(self, context):
		textToName()
		return{"FINISHED"}
		
class SeperateTextOperator(bpy.types.Operator):
	bl_idname = "sniper.seperate_text"
	bl_label = "Seperate Text"
	bl_description = "Create new text object for every line in active text object."
	
	def execute(self, context):
		active = getActive()
		if isTextObject(active):
			seperateTextObject(active)
			delete(active)
		
		return{"FINISHED"}
			

		
class AddTargetCamera(bpy.types.Operator):
	bl_idname = "sniper.insert_target_camera"
	bl_label = "Add Target Camera"
	bl_description = "Create new active camera and create targets from selection."
	
	@classmethod
	def poll(self, context):
		return not targetCameraSetupExists()
		
	def execute(self, context):
		insertTargetCamera()
		return{"FINISHED"}
		
class SetupTargetObject(bpy.types.Operator):
	bl_idname = "sniper.new_target_object"
	bl_label = "New Targets From Selection"
	bl_description = "Use selected objects as targets."
	
	def execute(self, context):
		newTargetsFromSelection()
		return{"FINISHED"}
		
class DeleteTargetOperator(bpy.types.Operator):
	bl_idname = "sniper.delete_target"
	bl_label = "Delete Target"
	bl_description = "Delete the target from the list."
	currentIndex: bpy.props.IntProperty()
	
	def execute(self, context):
		deleteTarget(self.currentIndex)
		return{"FINISHED"}
		
class RecalculateAnimationOperator(bpy.types.Operator):
	bl_idname = "sniper.recalculate_animation"
	bl_label = "Recalculate Animation"
	bl_description = "Regenerates most of the constraints, drivers and keyframes."
	
	def execute(self, context):
		createFullAnimation(getTargetList())
		return{"FINISHED"}
		
class MoveTargetUp(bpy.types.Operator):
	bl_idname = "sniper.move_target_up"
	bl_label = "Move Target Up"
	currentIndex: bpy.props.IntProperty()
	
	def execute(self, context):
		moveTargetUp(self.currentIndex)
		return{"FINISHED"}
		
class MoveTargetDown(bpy.types.Operator):
	bl_idname = "sniper.move_target_down"
	bl_label = "Move Target Down"
	currentIndex: bpy.props.IntProperty()
	
	def execute(self, context):
		moveTargetDown(self.currentIndex)
		return{"FINISHED"}		
		
class SelectTarget(bpy.types.Operator):
	bl_idname = "sniper.select_target"
	bl_label = "Select Target"
	bl_description = "Select that target."
	currentIndex: bpy.props.IntProperty()
	
	def execute(self, context):
		selectTarget(self.currentIndex)
		return{"FINISHED"}

class GoToNextTarget(bpy.types.Operator):		
	bl_idname = "sniper.go_to_next_target"
	bl_label = "Go To Next Target"
	bl_description = "Change frame to show next target."
	
	def execute(self, context):
		goToNextTarget()
		return{"FINISHED"}
		
class GoToPreviousTarget(bpy.types.Operator):		
	bl_idname = "sniper.go_to_previous_target"
	bl_label = "Go To Previous Target"
	bl_description = "Change frame to show previous target."
	
	def execute(self, context):
		goToPreviousTarget()
		return{"FINISHED"}
		
class CopyInterpolationPropertiesToAll(bpy.types.Operator):
	bl_idname = "sniper.copy_interpolation_properties_to_all"
	bl_label = "Copy Interpolation Properties"
	bl_description = "All targets will have these interpolation values."
	currentIndex: bpy.props.IntProperty()
	
	def execute(self, context):
		copyInterpolationProperties(self.currentIndex)
		return{"FINISHED"}
		
class OpenDopeSheet(bpy.types.Operator):
	bl_idname = "sniper.open_dope_sheet"
	bl_label = "Open Dope Sheet"
	bl_description = "Open dope sheet to manipulate the timing."
	
	@classmethod
	def poll(self, context):
		return not areaTypeExists("DOPESHEET_EDITOR")
	
	def execute(self, context):
		openDopeSheet()
		return{"FINISHED"}


		
# User Interface
#############################


class CAMERATOOLS_PT_view3d_panel(bpy.types.Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Animation"
	bl_label = "Sniper"
	bl_context = "objectmode"
	
	def draw(self, context):
		layout = self.layout
		
		col = layout.column(align = True)
		col.operator("sniper.insert_target_camera", icon = "OUTLINER_DATA_CAMERA")
		if targetCameraSetupExists(): col.label(text = "Settings are in 'Sniper' tab.", icon = "INFO")
		
		col = layout.column(align = True)
		col.operator("sniper.seperate_text")
		col.operator("sniper.text_to_name")
	


class TARGETCAMERA_PT_view3d_panel(bpy.types.Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Sniper"
	bl_label = "Sniper"
	bl_context = "objectmode"
	
	@classmethod
	def poll(self, context):
		return targetCameraSetupExists()
	
	def draw(self, context):		
		layout = self.layout
		
		camera = getTargetCamera()
		movement = getMovementEmpty()
		dataEmpty = getDataEmpty()
		targetList = getTargetList()
		
		col = layout.column(align = True)
		col.operator("sniper.recalculate_animation", text = "Recalculate", icon = "ACTION_TWEAK")
		col.operator("sniper.open_dope_sheet", text = "Manipulate Timing", icon = "ACTION")
			
		row = layout.row(align = True)
		row.operator("sniper.go_to_previous_target", icon = 'TRIA_LEFT', text = "")
		row.label(text = "Travel: " + str(getTravelValue()))
		row.operator("sniper.go_to_next_target", icon = 'TRIA_RIGHT', text = "")
		
		box = layout.box()
		col = box.column(align = True)
		
		for i in range(len(targetList)):
			row = col.split(factor = 0.6, align = True)
			row.scale_y = 1.35
			name = row.operator("sniper.select_target", text = getTargetObjectFromTarget(targetList[i]).name)
			name.currentIndex = i
			up = row.operator("sniper.move_target_up", icon = 'TRIA_UP', text = "")
			up.currentIndex = i
			down = row.operator("sniper.move_target_down", icon = 'TRIA_DOWN', text = "")
			down.currentIndex = i
			delete = row.operator("sniper.delete_target", icon = 'X', text = "")
			delete.currentIndex = i
			if useListSeparator: col.separator()
		box.operator("sniper.new_target_object", icon = 'PLUS')
		
		selectedTargets = getSelectedTargets(targetList)
		selectedTargets.reverse()
		for target in selectedTargets:
			box = layout.box()
			box.label(text = target.parent.name + "  (" + str(targetList.index(target) + 1) + ")")
			
			col = box.column(align = True)
			col.prop(target, slowInDataPath, slider = False, text = "Ease In")
			col.prop(target, slowOutDataPath, slider = False, text = "Ease Out")
			copyToAll = col.operator("sniper.copy_interpolation_properties_to_all", text = "Copy to All", icon = "COPYDOWN")
			copyToAll.currentIndex = targetList.index(target)			
			
		col = layout.column(align = True)
		col.label(text = "Camera Wiggle")
		col.prop(dataEmpty, wiggleStrengthDataPath, text = "Strength")
		col.prop(dataEmpty, wiggleScaleDataPath, text = "Time Scale")
		
		layout.prop(dataEmpty, '["'+ inertiaStrengthPropertyName +'"]', text = "Inertia Strength")
		
		if getCurrentSettingsHash() != oldHash:
			layout.label(text = "You should recalculate the animation", icon = 'ERROR')
		
