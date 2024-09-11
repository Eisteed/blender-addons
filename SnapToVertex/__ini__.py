import bpy

bl_info = {
    "name": "Snap to Vertex",
    "location": "View3D > 3D View (Global)",
    "description": "Snap To Vertex shortcut like Maya (Hold V)",
    "author": "Eisteed",
    "tracker_url": "https://github.com/Eisteed/blender/",    
    "doc_url": "https://www.eisteed.com/",
    "version": (1, 0),
    "blender": (4, 2, 1),
    "category": "3D View",
}

firstPress = True
oldTarget = None
oldSnap = None
oldAlign = None
class SnapToVertex(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.snape_to_vertex"
    bl_label = "Snap To Vertex (Hold V)"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        global firstPress,oldTarget,oldSnap,oldAlign
        if firstPress : 
            oldTarget = bpy.context.scene.tool_settings.snap_target
            oldSnap = bpy.context.scene.tool_settings.snap_elements
            oldAlign = bpy.context.scene.tool_settings.use_snap_align_rotation
            bpy.context.scene.tool_settings.use_snap = True
            bpy.context.scene.tool_settings.use_snap_align_rotation = False
            bpy.context.scene.tool_settings.snap_target = 'ACTIVE'
            bpy.context.scene.tool_settings.snap_elements = {'VERTEX'}
            firstPress = True
        else:
            bpy.context.scene.tool_settings.use_snap = False
            bpy.context.scene.tool_settings.snap_target = oldTarget
            bpy.context.scene.tool_settings.snap_elements = oldSnap
            bpy.context.scene.tool_settings.use_snap_align_rotation = oldAlign
            firstPress = False

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)


addon_keymaps = []

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(SnapToVertex)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    # Add the hotkey
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(SnapToVertex.bl_idname, type='V', value='PRESS')
        addon_keymaps.append((km, kmi))

        km2 = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi2 = km2.keymap_items.new(SnapToVertex.bl_idname, type='V', value='RELEASE')
        addon_keymaps.append((km2, kmi2))

def unregister():
    bpy.utils.unregister_class(SnapToVertex)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
    # Remove the hotkey
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
