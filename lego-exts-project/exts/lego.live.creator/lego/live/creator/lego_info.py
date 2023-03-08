# class to tell the lego information behavior
import omni.usd
from omni.physx.scripts.utils import setCollider, setRigidBody, setStaticCollider, removeCollider
from pxr import UsdPhysics, Usd
import random

class LegoInfo():
    def __init__(self, prim_path) -> None:
        # init 
        self.root_prim_path = prim_path
        self.stage = omni.usd.get_context().get_stage()

        # find node root
        self.root_prim = self.stage.GetPrimAtPath(self.root_prim_path)
        # for prim in self.prim.GetChildren():
        #     if prim.GetTypeName() == "Xform":
        #         self.node_prim = prim
        #         break
        
        # assert hasattr(self, "node_prim"), f"Node root is not found at {prim_path}"


    def add_rigid_body(self, dat_num = "3742"):
        """
        Add rigid body to all lego dat pieces
        """ 
        prim_list = self.stage.TraverseAll()
        self.dat_list = []
        for prim in prim_list: 
            prim_path = prim.GetPath().pathString   
            print("prim_path", prim_path, prim.GetTypeName())
            if prim.GetTypeName() == "Xform":
                prim_path_end = prim_path.split("/")[-1]
                if prim_path_end.split("_")[-1] == "dat" and dat_num in prim_path_end:
                    self.dat_list.append(prim_path)

                    if not prim.HasAPI(UsdPhysics.RigidBodyAPI):
                        setRigidBody(prim, "convexHull", False)
        
                    # disable rigid body
                    physicsAPI = UsdPhysics.RigidBodyAPI(prim)
                    physicsAPI.GetRigidBodyEnabledAttr().Set(False)

    def randomize_rigid_body_enable(self):
        random.shuffle(self.dat_list)
        
        from omni.timeline import get_timeline_interface
        timeline_iface = get_timeline_interface()

        timeline_iface.set_current_time(0)
        for i, prim_path in enumerate(self.dat_list[:50]):
            (result, err) = omni.kit.commands.execute("SetAnimCurveKeys", 
                                                    paths=[f"{prim_path}.physics:rigidBodyEnabled"], 
                                                    value = False)
        
        # timeline_iface.set_current_time(0)
        for i, prim_path in enumerate(self.dat_list[:50]):
            (result, err) = omni.kit.commands.execute("SetAnimCurveKeys", 
                                                    paths=[f"{prim_path}.physics:rigidBodyEnabled"], 
                                                    value = False, time=Usd.TimeCode(2 * i))
            (result, err) = omni.kit.commands.execute("SetAnimCurveKeys", 
                                                    paths=[f"{prim_path}.physics:rigidBodyEnabled"], 
                                                    value = True, time=Usd.TimeCode(2 * i + 1))
            print("random:", i, "\n", prim_path, "\n", result, err)
