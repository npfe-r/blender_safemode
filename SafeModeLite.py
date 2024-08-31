bl_info = {
    "name" : "SafeModeLite",
    "description" : "",
    "blender" : (3, 6, 14),
    "version" : (1, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "Render" 
}

import bpy
import addon_utils

# 白名单
whitelist = ["mmd_tools","cycles"]

def disable_addons():
    # 获取所有已启用的插件
    enabled_addons = bpy.context.preferences.addons.keys()

    # 遍历并检查插件是否在白名单中
    for addon in list(enabled_addons):
        if addon not in whitelist and addon != 'SafeMode':
            # 禁用插件
            addon_utils.disable(addon)

def enable_addons():
    # 启用插件
    for addon in bpy.context.preferences.addons.keys():
        addon_utils.enable(addon)

class safemodeEnable(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "safemode.enable"
    bl_label = "Safe Mode Enable"

    def execute(self, context):
        disable_addons()
        return {'FINISHED'}

class safemodeDisable(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "safemode.disable"
    bl_label = "Safe Mode Disable"

    def execute(self, context):
        enable_addons()
        return {'FINISHED'}

class safemodePanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Safe Mode"
    bl_idname = "safemodePanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        row = layout.row(align=True)
        row.scale_y = 1
        row.operator("safemode.enable")
        row.scale_y = 1
        row.operator("safemode.disable")
      
def register():
    bpy.utils.register_class(safemodePanel)
    bpy.utils.register_class(safemodeEnable)
    bpy.utils.register_class(safemodeDisable)

def unregister():
    bpy.utils.unregister_class(safemodePanel)
    bpy.utils.unregister_class(safemodeEnable)
    bpy.utils.unregister_class(safemodeDisable)

if __name__ == "__main__":
    register()
