import omni.ext
import omni.ui as ui

from .lego_info import LegoInfo

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class LegoLiveCreatorExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[lego.live.creator] lego live creator startup")

        self._window = ui.Window("Lego Anim Creator", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                self.lego_root_ui = ui.StringField(height=20, style={ "margin_height": 2})
                self.lego_root_ui.model.set_value("/World/house")
                ui.Button("Set Lego Anim", clicked_fn=self.set_lego_anim)
                ui.Button("Debug", clicked_fn=self.debug)

    def set_lego_anim(self):
        print("set_lego_anim")
        self.lego_info = LegoInfo(self.lego_root_ui.model.get_value_as_string())
        print("add rigid bodies")
        self.lego_info.add_rigid_body()        
        self.lego_info.randomize_rigid_body_enable()

        

    def debug(self):
        print("debug")
        import omni
        curve_plugin = omni.anim.curve.acquire_interface()

        from pxr import AnimationSchema, Usd
        stage = omni.usd.get_context().get_stage()
        prim_path = "/World/Cube"
        prim = stage.GetPrimAtPath(prim_path)

        
        (result, err) = omni.kit.commands.execute("SetAnimCurveKeys", 
                                                  paths=["/World/Cube.physics:rigidBodyEnabled"], 
                                                  value = False, time=Usd.TimeCode(10))

        anim_data = AnimationSchema.AnimationData.Get(stage, "/World/Cube/animationData")
        print("anim_data", bool(anim_data))

    def on_shutdown(self):
        print("[lego.live.creator] lego live creator shutdown")

