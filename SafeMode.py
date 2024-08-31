bl_info = {
    "name" : "SafeMode",
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
whitelist = ["cycles"]

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

        row = layout.row()
        row.template_list("AddonList", "", scene, "whitelist_items", scene, "whitelist_index")

        col = row.column(align=True)
        col.operator("safemode.add_to_whitelist", icon='ADD', text="")
        col.operator("safemode.remove_from_whitelist", icon='REMOVE', text="")
        col.operator("safemode.refresh_whitelist", icon='FILE_REFRESH', text="")  # 添加刷新按钮

class AddonList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=item.name)

class WhitelistItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Addon Name")

class AddToWhitelist(bpy.types.Operator):
    """Add an addon to the whitelist"""
    bl_idname = "safemode.add_to_whitelist"
    bl_label = "Add to Whitelist"

    addon_name: bpy.props.StringProperty(name="Addon Name")

    def execute(self, context):
        if self.addon_name not in whitelist:
            whitelist.append(self.addon_name)
            # 添加到白名单集合中
            item = context.scene.whitelist_items.add()
            item.name = self.addon_name
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class RemoveFromWhitelist(bpy.types.Operator):
    """Remove an addon from the whitelist"""
    bl_idname = "safemode.remove_from_whitelist"
    bl_label = "Remove from Whitelist"

    def execute(self, context):
        index = context.scene.whitelist_index
        if index >= 0 and index < len(context.scene.whitelist_items):
            addon_name = context.scene.whitelist_items[index].name
            if addon_name in whitelist:
                whitelist.remove(addon_name)
                # 从白名单集合中移除
                context.scene.whitelist_items.remove(index)
        return {'FINISHED'}

class RefreshWhitelist(bpy.types.Operator):
    """Refresh the whitelist"""
    bl_idname = "safemode.refresh_whitelist"
    bl_label = "Refresh Whitelist"

    def execute(self, context):
        # 清空白名单集合
        context.scene.whitelist_items.clear()
        # 重新添加白名单中的插件
        for addon_name in whitelist:
            item = context.scene.whitelist_items.add()
            item.name = addon_name
        return {'FINISHED'}

def register():
    bpy.utils.register_class(safemodePanel)
    bpy.utils.register_class(safemodeEnable)
    bpy.utils.register_class(safemodeDisable)
    bpy.utils.register_class(AddonList)
    bpy.utils.register_class(WhitelistItem)
    bpy.utils.register_class(AddToWhitelist)
    bpy.utils.register_class(RemoveFromWhitelist)
    bpy.utils.register_class(RefreshWhitelist)  # 注册刷新操作类
    bpy.types.Scene.whitelist_items = bpy.props.CollectionProperty(type=WhitelistItem)
    bpy.types.Scene.whitelist_index = bpy.props.IntProperty()

def unregister():
    bpy.utils.unregister_class(safemodePanel)
    bpy.utils.unregister_class(safemodeEnable)
    bpy.utils.unregister_class(safemodeDisable)
    bpy.utils.unregister_class(AddonList)
    bpy.utils.unregister_class(WhitelistItem)
    bpy.utils.unregister_class(AddToWhitelist)
    bpy.utils.unregister_class(RemoveFromWhitelist)
    bpy.utils.unregister_class(RefreshWhitelist)  # 注销刷新操作类
    del bpy.types.Scene.whitelist_items
    del bpy.types.Scene.whitelist_index

if __name__ == "__main__":
    register()
