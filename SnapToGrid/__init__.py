import bpy

bl_info = {
    "name": "Snap to Grid (Maya)",
    "location": "View3D > 3D View (Global)",
    "description": "Snap To Grid shortcut like Maya (Hold X)",
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

class SnapToGrid(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.snap_to_grid"
    bl_label = "Snap To Grid (Hold X)"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        global firstPress,oldTarget,oldSnap

        tool_settings = bpy.context.scene.tool_settings
        if firstPress :
            oldSnap = tool_settings.snap_elements
            tool_settings.use_snap = True
            tool_settings.snap_elements = {'GRID'}
            firstPress = False
        else:
            tool_settings.use_snap = False
            tool_settings.snap_elements = oldSnap
            firstPress = True

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SnapToGrid.bl_idname, text=SnapToGrid.bl_label)

addon_keymaps = []

def register():
    bpy.utils.register_class(SnapToGrid)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(SnapToGrid.bl_idname, type='X', value='PRESS')
        addon_keymaps.append((km, kmi))

        km2 = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi2 = km2.keymap_items.new(SnapToGrid.bl_idname, type='X', value='RELEASE')
        addon_keymaps.append((km2, kmi2))

def unregister():
    bpy.utils.unregister_class(SnapToGrid)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
