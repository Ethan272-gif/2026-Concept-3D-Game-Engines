from panda3d.core import PandaNode, Loader, NodePath, CollisionNode,CollisionSphere,CollisionInvSphere,CollisionCapsule,Vec3,BitMask32

class PlaceObject(PandaNode):
    def __init__(self,loader:Loader,modelPath:str,parentNode:NodePath,nodeName:str):
        self.modelNode:NodePath=loader.loadModel(modelPath)# type: ignore


        if not isinstance(self.modelNode,NodePath):
            raise AssertionError("PlaceObject loader.loadModel("+ modelPath+")did not return a proper PandaNodel=!")
        self.collisionNode=self.modelNode.attachNewNode(CollisionNode(nodeName+'_cNode'))
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setName(nodeName)

class CollidableObject(PlaceObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str):
        super(CollidableObject,self).__init__(loader,modelPath,parentNode,nodeName)
        self.collisionNode.node().setFromCollideMask(BitMask32.bit(1))
        self.collisionNode.node().setIntoCollideMask(BitMask32.bit(1))
        self.collisionNode.show()
        
class InverseGphereCollideObject(CollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,colPositionVec: Vec3, colRadius: float):
        super(InverseGphereCollideObject,self).__init__(loader,modelPath,parentNode,nodeName)
        self.collisionNode.node().clearSolids()
        self.collisionNode.node().addSolid(CollisionInvSphere(colPositionVec, colRadius))
        self.collisionNode.show()


class CapsuleCollidableObject(CollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,nodeName:str,ax:float,ay:float,az:float,bx:float,by:float,
                 bz:float,r:float):
        super(CapsuleCollidableObject,self).__init__(loader,modelPath,parentNode,nodeName)
        self.collisionNode.node().addSolid(CollisionCapsule(ax,ay,az,bx,by,bz,r))
        self.collisionNode.show()

class SphereCollideObject(CollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,nodeName: str, colPositionVec: Vec3, colRadius: float):
        super(SphereCollideObject,self).__init__(loader,modelPath,parentNode,nodeName)
        collision_sphere = CollisionSphere(colPositionVec, colRadius)
        self.collisionNode.node().addSolid(collision_sphere)
        self.collisionNode.show()

class InverseSphereCollideObject(InverseGphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,nodeName: str, colPositionVec: Vec3, colRadius: float):
        super(InverseSphereCollideObject,self).__init__(loader,modelPath,parentNode,nodeName,colPositionVec, colRadius)
        # self.collisionNode.node().addSolid(CollisionSphere(colPositionVec,colRadius))
        self.collisionNode.show()