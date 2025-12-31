bl_info = {
    "name": "CharacterRebuilder",
    "author": "Manfred Aabye",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Tool Shelf",
    "description": "Knochen umbenennen und gewichten für Second Life und OpenSim.",
    "category": "Object",
    "type": "ADDON",
}

import bpy # type: ignore
import collections
import functools
import json
import os

class CHARACTERREBUILDER_Preferences(bpy.types.AddonPreferences):
    bl_idname = "CharacterRebuilder"

    crc_path = bpy.props.StringProperty(
        name="Voreingestellter .crc-Pfad",
        subtype='DIR_PATH',
        default=os.path.dirname(os.path.realpath(__file__)) if os.path.isfile(__file__) else ""
    )

    def draw(self, context):
        layout = self.layout
        # Zeigt den voreingestellten .crc-Pfad in den Addon-Preferences an
        layout.prop(self, "crc_path")

# Vollständiges SL/OpenSim-Bone-Mapping (Beispiel, ggf. erweitern)
SL_BONE_MAP = {
    # Body
    "mPelvis": "mPelvis",
    "mTorso": "mTorso",
    "mChest": "mChest",
    "mChest2": "mChest2",
    "mNeck": "mNeck",
    "mHead": "mHead",
    # Arms Left
    "mCollarLeft": "mCollarLeft",
    "mShoulderLeft": "mShoulderLeft",
    "mElbowLeft": "mElbowLeft",
    "mWristLeft": "mWristLeft",
    "mHandLeft": "mHandLeft",
    "mThumb0Left": "mThumb0Left",
    "mThumb1Left": "mThumb1Left",
    "mThumb2Left": "mThumb2Left",
    "mThumb3Left": "mThumb3Left",
    "mIndexFinger0Left": "mIndexFinger0Left",
    "mIndexFinger1Left": "mIndexFinger1Left",
    "mIndexFinger2Left": "mIndexFinger2Left",
    "mIndexFinger3Left": "mIndexFinger3Left",
    "mMiddleFinger0Left": "mMiddleFinger0Left",
    "mMiddleFinger1Left": "mMiddleFinger1Left",
    "mMiddleFinger2Left": "mMiddleFinger2Left",
    "mMiddleFinger3Left": "mMiddleFinger3Left",
    "mRingFinger0Left": "mRingFinger0Left",
    "mRingFinger1Left": "mRingFinger1Left",
    "mRingFinger2Left": "mRingFinger2Left",
    "mRingFinger3Left": "mRingFinger3Left",
    "mPinkyFinger0Left": "mPinkyFinger0Left",
    "mPinkyFinger1Left": "mPinkyFinger1Left",
    "mPinkyFinger2Left": "mPinkyFinger2Left",
    "mPinkyFinger3Left": "mPinkyFinger3Left",
    # Arms Right
    "mCollarRight": "mCollarRight",
    "mShoulderRight": "mShoulderRight",
    "mElbowRight": "mElbowRight",
    "mWristRight": "mWristRight",
    "mHandRight": "mHandRight",
    "mThumb0Right": "mThumb0Right",
    "mThumb1Right": "mThumb1Right",
    "mThumb2Right": "mThumb2Right",
    "mThumb3Right": "mThumb3Right",
    "mIndexFinger0Right": "mIndexFinger0Right",
    "mIndexFinger1Right": "mIndexFinger1Right",
    "mIndexFinger2Right": "mIndexFinger2Right",
    "mIndexFinger3Right": "mIndexFinger3Right",
    "mMiddleFinger0Right": "mMiddleFinger0Right",
    "mMiddleFinger1Right": "mMiddleFinger1Right",
    "mMiddleFinger2Right": "mMiddleFinger2Right",
    "mMiddleFinger3Right": "mMiddleFinger3Right",
    "mRingFinger0Right": "mRingFinger0Right",
    "mRingFinger1Right": "mRingFinger1Right",
    "mRingFinger2Right": "mRingFinger2Right",
    "mRingFinger3Right": "mRingFinger3Right",
    "mPinkyFinger0Right": "mPinkyFinger0Right",
    "mPinkyFinger1Right": "mPinkyFinger1Right",
    "mPinkyFinger2Right": "mPinkyFinger2Right",
    "mPinkyFinger3Right": "mPinkyFinger3Right",
    # Legs Left
    "mHipLeft": "mHipLeft",
    "mKneeLeft": "mKneeLeft",
    "mAnkleLeft": "mAnkleLeft",
    "mFootLeft": "mFootLeft",
    "mToeLeft": "mToeLeft",
    # Legs Right
    "mHipRight": "mHipRight",
    "mKneeRight": "mKneeRight",
    "mAnkleRight": "mAnkleRight",
    "mFootRight": "mFootRight",
    "mToeRight": "mToeRight",
    # Eyes
    "mEyeLeft": "mEyeLeft",
    "mEyeRight": "mEyeRight",
    # Bento Face
    "mFaceJaw": "mFaceJaw",
    "mFaceJawShaper": "mFaceJawShaper",
    "mFaceChin": "mFaceChin",
    "mFaceChinShaper": "mFaceChinShaper",
    "mFaceCheekLeft": "mFaceCheekLeft",
    "mFaceCheekRight": "mFaceCheekRight",
    "mFaceNose": "mFaceNose",
    "mFaceNoseShaper": "mFaceNoseShaper",
    "mFaceForehead": "mFaceForehead",
    "mFaceBrowLeft": "mFaceBrowLeft",
    "mFaceBrowRight": "mFaceBrowRight",
    "mFaceLipUpper": "mFaceLipUpper",
    "mFaceLipLower": "mFaceLipLower",
    "mFaceLipCornerLeft": "mFaceLipCornerLeft",
    "mFaceLipCornerRight": "mFaceLipCornerRight",
    # Bento Wings
    "mWing1Left": "mWing1Left",
    "mWing2Left": "mWing2Left",
    "mWing3Left": "mWing3Left",
    "mWing4Left": "mWing4Left",
    "mWing1Right": "mWing1Right",
    "mWing2Right": "mWing2Right",
    "mWing3Right": "mWing3Right",
    "mWing4Right": "mWing4Right",
    # Bento Tail
    "mTail1": "mTail1",
    "mTail2": "mTail2",
    "mTail3": "mTail3",
    "mTail4": "mTail4",
    "mTail5": "mTail5",
    # Bento Extra Limbs
    "mExtraArmLeft": "mExtraArmLeft",
    "mExtraForearmLeft": "mExtraForearmLeft",
    "mExtraHandLeft": "mExtraHandLeft",
    "mExtraArmRight": "mExtraArmRight",
    "mExtraForearmRight": "mExtraForearmRight",
    "mExtraHandRight": "mExtraHandRight",
}

RIGIFY_BONE_MAP = {
    # Realistische Zuordnung für Rigify Human Meta-Rig (Bento-kompatibel)
    "root": "mPelvis",
    "spine": "mTorso",
    "spine.001": "mChest",
    "spine.002": "mChest2",
    "neck": "mNeck",
    "head": "mHead",
    "shoulder.L": "mShoulderLeft",
    "upper_arm.L": "mElbowLeft",
    "forearm.L": "mWristLeft",
    "hand.L": "mHandLeft",
    "thumb.01.L": "mThumb0Left",
    "thumb.02.L": "mThumb1Left",
    "thumb.03.L": "mThumb2Left",
    "f_index.01.L": "mIndexFinger0Left",
    "f_index.02.L": "mIndexFinger1Left",
    "f_index.03.L": "mIndexFinger2Left",
    "f_middle.01.L": "mMiddleFinger0Left",
    "f_middle.02.L": "mMiddleFinger1Left",
    "f_middle.03.L": "mMiddleFinger2Left",
    "f_ring.01.L": "mRingFinger0Left",
    "f_ring.02.L": "mRingFinger1Left",
    "f_ring.03.L": "mRingFinger2Left",
    "f_pinky.01.L": "mPinkyFinger0Left",
    "f_pinky.02.L": "mPinkyFinger1Left",
    "f_pinky.03.L": "mPinkyFinger2Left",
    "shoulder.R": "mShoulderRight",
    "upper_arm.R": "mElbowRight",
    "forearm.R": "mWristRight",
    "hand.R": "mHandRight",
    "thumb.01.R": "mThumb0Right",
    "thumb.02.R": "mThumb1Right",
    "thumb.03.R": "mThumb2Right",
    "f_index.01.R": "mIndexFinger0Right",
    "f_index.02.R": "mIndexFinger1Right",
    "f_index.03.R": "mIndexFinger2Right",
    "f_middle.01.R": "mMiddleFinger0Right",
    "f_middle.02.R": "mMiddleFinger1Right",
    "f_middle.03.R": "mMiddleFinger2Right",
    "f_ring.01.R": "mRingFinger0Right",
    "f_ring.02.R": "mRingFinger1Right",
    "f_ring.03.R": "mRingFinger2Right",
    "f_pinky.01.R": "mPinkyFinger0Right",
    "f_pinky.02.R": "mPinkyFinger1Right",
    "f_pinky.03.R": "mPinkyFinger2Right",
    "thigh.L": "mHipLeft",
    "shin.L": "mKneeLeft",
    "foot.L": "mFootLeft",
    "toe.L": "mToeLeft",
    "thigh.R": "mHipRight",
    "shin.R": "mKneeRight",
    "foot.R": "mFootRight",
    "toe.R": "mToeRight",
    "eye.L": "mEyeLeft",
    "eye.R": "mEyeRight",
}


AVASTAR_BONE_MAP = {
    # Vollständige Zuordnung für Avastar (Bento-kompatibel)
    "mPelvis": "mPelvis", "mTorso": "mTorso", "mChest": "mChest", "mChest2": "mChest2", "mNeck": "mNeck", "mHead": "mHead",
    "mCollarLeft": "mCollarLeft", "mShoulderLeft": "mShoulderLeft", "mElbowLeft": "mElbowLeft", "mWristLeft": "mWristLeft", "mHandLeft": "mHandLeft",
    "mThumb0Left": "mThumb0Left", "mThumb1Left": "mThumb1Left", "mThumb2Left": "mThumb2Left", "mThumb3Left": "mThumb3Left",
    "mIndexFinger0Left": "mIndexFinger0Left", "mIndexFinger1Left": "mIndexFinger1Left", "mIndexFinger2Left": "mIndexFinger2Left", "mIndexFinger3Left": "mIndexFinger3Left",
    "mMiddleFinger0Left": "mMiddleFinger0Left", "mMiddleFinger1Left": "mMiddleFinger1Left", "mMiddleFinger2Left": "mMiddleFinger2Left", "mMiddleFinger3Left": "mMiddleFinger3Left",
    "mRingFinger0Left": "mRingFinger0Left", "mRingFinger1Left": "mRingFinger1Left", "mRingFinger2Left": "mRingFinger2Left", "mRingFinger3Left": "mRingFinger3Left",
    "mPinkyFinger0Left": "mPinkyFinger0Left", "mPinkyFinger1Left": "mPinkyFinger1Left", "mPinkyFinger2Left": "mPinkyFinger2Left", "mPinkyFinger3Left": "mPinkyFinger3Left",
    "mCollarRight": "mCollarRight", "mShoulderRight": "mShoulderRight", "mElbowRight": "mElbowRight", "mWristRight": "mWristRight", "mHandRight": "mHandRight",
    "mThumb0Right": "mThumb0Right", "mThumb1Right": "mThumb1Right", "mThumb2Right": "mThumb2Right", "mThumb3Right": "mThumb3Right",
    "mIndexFinger0Right": "mIndexFinger0Right", "mIndexFinger1Right": "mIndexFinger1Right", "mIndexFinger2Right": "mIndexFinger2Right", "mIndexFinger3Right": "mIndexFinger3Right",
    "mMiddleFinger0Right": "mMiddleFinger0Right", "mMiddleFinger1Right": "mMiddleFinger1Right", "mMiddleFinger2Right": "mMiddleFinger2Right", "mMiddleFinger3Right": "mMiddleFinger3Right",
    "mRingFinger0Right": "mRingFinger0Right", "mRingFinger1Right": "mRingFinger1Right", "mRingFinger2Right": "mRingFinger2Right", "mRingFinger3Right": "mRingFinger3Right",
    "mPinkyFinger0Right": "mPinkyFinger0Right", "mPinkyFinger1Right": "mPinkyFinger1Right", "mPinkyFinger2Right": "mPinkyFinger2Right", "mPinkyFinger3Right": "mPinkyFinger3Right",
    "mHipLeft": "mHipLeft", "mKneeLeft": "mKneeLeft", "mAnkleLeft": "mAnkleLeft", "mFootLeft": "mFootLeft", "mToeLeft": "mToeLeft",
    "mHipRight": "mHipRight", "mKneeRight": "mKneeRight", "mAnkleRight": "mAnkleRight", "mFootRight": "mFootRight", "mToeRight": "mToeRight",
    "mEyeLeft": "mEyeLeft", "mEyeRight": "mEyeRight",
}

BENTOBUDDY_BONE_MAP = {
    # Vollständige Zuordnung für Bento Buddy (Bento-kompatibel)
    "mPelvis": "mPelvis", "mTorso": "mTorso", "mChest": "mChest", "mChest2": "mChest2", "mNeck": "mNeck", "mHead": "mHead",
    "mCollarLeft": "mCollarLeft", "mShoulderLeft": "mShoulderLeft", "mElbowLeft": "mElbowLeft", "mWristLeft": "mWristLeft", "mHandLeft": "mHandLeft",
    "mThumb0Left": "mThumb0Left", "mThumb1Left": "mThumb1Left", "mThumb2Left": "mThumb2Left", "mThumb3Left": "mThumb3Left",
    "mIndexFinger0Left": "mIndexFinger0Left", "mIndexFinger1Left": "mIndexFinger1Left", "mIndexFinger2Left": "mIndexFinger2Left", "mIndexFinger3Left": "mIndexFinger3Left",
    "mMiddleFinger0Left": "mMiddleFinger0Left", "mMiddleFinger1Left": "mMiddleFinger1Left", "mMiddleFinger2Left": "mMiddleFinger2Left", "mMiddleFinger3Left": "mMiddleFinger3Left",
    "mRingFinger0Left": "mRingFinger0Left", "mRingFinger1Left": "mRingFinger1Left", "mRingFinger2Left": "mRingFinger2Left", "mRingFinger3Left": "mRingFinger3Left",
    "mPinkyFinger0Left": "mPinkyFinger0Left", "mPinkyFinger1Left": "mPinkyFinger1Left", "mPinkyFinger2Left": "mPinkyFinger2Left", "mPinkyFinger3Left": "mPinkyFinger3Left",
    "mCollarRight": "mCollarRight", "mShoulderRight": "mShoulderRight", "mElbowRight": "mElbowRight", "mWristRight": "mWristRight", "mHandRight": "mHandRight",
    "mThumb0Right": "mThumb0Right", "mThumb1Right": "mThumb1Right", "mThumb2Right": "mThumb2Right", "mThumb3Right": "mThumb3Right",
    "mIndexFinger0Right": "mIndexFinger0Right", "mIndexFinger1Right": "mIndexFinger1Right", "mIndexFinger2Right": "mIndexFinger2Right", "mIndexFinger3Right": "mIndexFinger3Right",
    "mMiddleFinger0Right": "mMiddleFinger0Right", "mMiddleFinger1Right": "mMiddleFinger1Right", "mMiddleFinger2Right": "mMiddleFinger2Right", "mMiddleFinger3Right": "mMiddleFinger3Right",
    "mRingFinger0Right": "mRingFinger0Right", "mRingFinger1Right": "mRingFinger1Right", "mRingFinger2Right": "mRingFinger2Right", "mRingFinger3Right": "mRingFinger3Right",
    "mPinkyFinger0Right": "mPinkyFinger0Right", "mPinkyFinger1Right": "mPinkyFinger1Right", "mPinkyFinger2Right": "mPinkyFinger2Right", "mPinkyFinger3Right": "mPinkyFinger3Right",
    "mHipLeft": "mHipLeft", "mKneeLeft": "mKneeLeft", "mAnkleLeft": "mAnkleLeft", "mFootLeft": "mFootLeft", "mToeLeft": "mToeLeft",
    "mHipRight": "mHipRight", "mKneeRight": "mKneeRight", "mAnkleRight": "mAnkleRight", "mFootRight": "mFootRight", "mToeRight": "mToeRight",
    "mEyeLeft": "mEyeLeft", "mEyeRight": "mEyeRight",
    # Optional: Face, Wings, Tail, Extra Limbs falls vorhanden
    "mFaceJaw": "mFaceJaw", "mFaceJawShaper": "mFaceJawShaper", "mFaceChin": "mFaceChin", "mFaceChinShaper": "mFaceChinShaper",
    "mFaceCheekLeft": "mFaceCheekLeft", "mFaceCheekRight": "mFaceCheekRight", "mFaceNose": "mFaceNose", "mFaceNoseShaper": "mFaceNoseShaper",
    "mFaceForehead": "mFaceForehead", "mFaceBrowLeft": "mFaceBrowLeft", "mFaceBrowRight": "mFaceBrowRight",
    "mFaceLipUpper": "mFaceLipUpper", "mFaceLipLower": "mFaceLipLower", "mFaceLipCornerLeft": "mFaceLipCornerLeft", "mFaceLipCornerRight": "mFaceLipCornerRight",
    "mWing1Left": "mWing1Left", "mWing2Left": "mWing2Left", "mWing3Left": "mWing3Left", "mWing4Left": "mWing4Left",
    "mWing1Right": "mWing1Right", "mWing2Right": "mWing2Right", "mWing3Right": "mWing3Right", "mWing4Right": "mWing4Right",
    "mTail1": "mTail1", "mTail2": "mTail2", "mTail3": "mTail3", "mTail4": "mTail4", "mTail5": "mTail5",
    "mExtraArmLeft": "mExtraArmLeft", "mExtraForearmLeft": "mExtraForearmLeft", "mExtraHandLeft": "mExtraHandLeft",
    "mExtraArmRight": "mExtraArmRight", "mExtraForearmRight": "mExtraForearmRight", "mExtraHandRight": "mExtraHandRight",

}
MIXAMO_BONE_MAP = {
    # Vollständige Zuordnung für Mixamo (Bento-kompatibel)
    "Hips": "mPelvis", "Spine": "mTorso", "Spine1": "mChest", "Spine2": "mChest2", "Neck": "mNeck", "Head": "mHead",
    "LeftShoulder": "mShoulderLeft", "LeftArm": "mElbowLeft", "LeftForeArm": "mWristLeft", "LeftHand": "mHandLeft",
    "LeftHandThumb1": "mThumb0Left", "LeftHandThumb2": "mThumb1Left", "LeftHandThumb3": "mThumb2Left",
    "LeftHandIndex1": "mIndexFinger0Left", "LeftHandIndex2": "mIndexFinger1Left", "LeftHandIndex3": "mIndexFinger2Left",
    "LeftHandMiddle1": "mMiddleFinger0Left", "LeftHandMiddle2": "mMiddleFinger1Left", "LeftHandMiddle3": "mMiddleFinger2Left",
    "LeftHandRing1": "mRingFinger0Left", "LeftHandRing2": "mRingFinger1Left", "LeftHandRing3": "mRingFinger2Left",
    "LeftHandPinky1": "mPinkyFinger0Left", "LeftHandPinky2": "mPinkyFinger1Left", "LeftHandPinky3": "mPinkyFinger2Left",
    "RightShoulder": "mShoulderRight", "RightArm": "mElbowRight", "RightForeArm": "mWristRight", "RightHand": "mHandRight",
    "RightHandThumb1": "mThumb0Right", "RightHandThumb2": "mThumb1Right", "RightHandThumb3": "mThumb2Right",
    "RightHandIndex1": "mIndexFinger0Right", "RightHandIndex2": "mIndexFinger1Right", "RightHandIndex3": "mIndexFinger2Right",
    "RightHandMiddle1": "mMiddleFinger0Right", "RightHandMiddle2": "mMiddleFinger1Right", "RightHandMiddle3": "mMiddleFinger2Right",
    "RightHandRing1": "mRingFinger0Right", "RightHandRing2": "mRingFinger1Right", "RightHandRing3": "mRingFinger2Right",
    "RightHandPinky1": "mPinkyFinger0Right", "RightHandPinky2": "mPinkyFinger1Right", "RightHandPinky3": "mPinkyFinger2Right",
    "LeftUpLeg": "mHipLeft", "LeftLeg": "mKneeLeft", "LeftFoot": "mFootLeft", "LeftToeBase": "mToeLeft",
    "RightUpLeg": "mHipRight", "RightLeg": "mKneeRight", "RightFoot": "mFootRight", "RightToeBase": "mToeRight",
    "LeftEye": "mEyeLeft", "RightEye": "mEyeRight",
}

DAZ_BONE_MAP = {
    # Vollständige Zuordnung für DAZ (Bento-kompatibel)
    "hip": "mPelvis", "abdomen": "mTorso", "chest": "mChest", "chest2": "mChest2", "neck": "mNeck", "head": "mHead",
    "lCollar": "mCollarLeft", "lShldr": "mShoulderLeft", "lForeArm": "mElbowLeft", "lHand": "mHandLeft",
    "lThumb1": "mThumb0Left", "lThumb2": "mThumb1Left", "lThumb3": "mThumb2Left",
    "lIndex1": "mIndexFinger0Left", "lIndex2": "mIndexFinger1Left", "lIndex3": "mIndexFinger2Left",
    "lMid1": "mMiddleFinger0Left", "lMid2": "mMiddleFinger1Left", "lMid3": "mMiddleFinger2Left",
    "lRing1": "mRingFinger0Left", "lRing2": "mRingFinger1Left", "lRing3": "mRingFinger2Left",
    "lPinky1": "mPinkyFinger0Left", "lPinky2": "mPinkyFinger1Left", "lPinky3": "mPinkyFinger2Left",
    "rCollar": "mCollarRight", "rShldr": "mShoulderRight", "rForeArm": "mElbowRight", "rHand": "mHandRight",
    "rThumb1": "mThumb0Right", "rThumb2": "mThumb1Right", "rThumb3": "mThumb2Right",
    "rIndex1": "mIndexFinger0Right", "rIndex2": "mIndexFinger1Right", "rIndex3": "mIndexFinger2Right",
    "rMid1": "mMiddleFinger0Right", "rMid2": "mMiddleFinger1Right", "rMid3": "mMiddleFinger2Right",
    "rRing1": "mRingFinger0Right", "rRing2": "mRingFinger1Right", "rRing3": "mRingFinger2Right",
    "rPinky1": "mPinkyFinger0Right", "rPinky2": "mPinkyFinger1Right", "rPinky3": "mPinkyFinger2Right",
    "lThigh": "mHipLeft", "lShin": "mKneeLeft", "lFoot": "mFootLeft", "lToe": "mToeLeft",
    "rThigh": "mHipRight", "rShin": "mKneeRight", "rFoot": "mFootRight", "rToe": "mToeRight",
}

PRESETS = {
    # Einheitliche Preset-Namen für UI und Logik
    "Second Life Default": SL_BONE_MAP,
    "OpenSim Default": SL_BONE_MAP,
    "Rigify Default": RIGIFY_BONE_MAP,
    "Avastar Default": AVASTAR_BONE_MAP,
    "Bento Buddy Default": BENTOBUDDY_BONE_MAP,
    "Mixamo Default": MIXAMO_BONE_MAP,
    "DAZ Default": DAZ_BONE_MAP
}

def get_meshes_with_armature(armature):
    """Finde alle Meshes, die diesen Armature Modifier nutzen (auch mehrfach)."""
    meshes = []
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE' and mod.object == armature:
                    meshes.append(obj)
    return meshes


class CHARACTERREBUILDER_PT_panel(bpy.types.Panel):
    bl_label = "Character Rebuilder"
    bl_idname = "CHARACTERREBUILDER_PT_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Knochen für SL/OpenSim", icon='ARMATURE_DATA')
        scene = context.scene
        # Preset-Auswahl (Dropdown)
        if hasattr(scene, "characterrebuilder_preset"):
            col.prop(scene, "characterrebuilder_preset", text="Preset")
            # Startet das Umbenennen der Knochen nach gewähltem Preset
            col.operator("characterrebuilder.rename_bones", icon='OUTLINER_OB_ARMATURE', text="Knochen umbenennen")
        else:
            col.label(text="[Preset-Property fehlt! Bitte Addon neu aktivieren]", icon='ERROR')
            col.operator("characterrebuilder.rename_bones", icon='OUTLINER_OB_ARMATURE')
        col.operator("characterrebuilder.weight_bones", icon='MOD_VERTEX_WEIGHT')
        layout.separator()
        # Einklappbare Bone-Mapping-Liste
        show_bonelist = getattr(scene, "characterrebuilder_show_bonelist", False)
        layout.prop(scene, "characterrebuilder_show_bonelist", text="Bone-Mapping anzeigen", toggle=True, icon='TRIA_DOWN' if show_bonelist else 'TRIA_RIGHT')
        if show_bonelist:
            box = layout.box()
            box.label(text="Bone-Mapping (Rigify-Style)", icon='BONE_DATA')
            preset_key = getattr(scene, "characterrebuilder_preset", "Second Life Default")
            if preset_key is None:
                preset_key = "Second Life Default"
            bone_map = PRESETS.get(str(preset_key), SL_BONE_MAP)
            obj = context.object
            rigify_unmapped = False
            if obj and obj.type == 'ARMATURE':
                for bone in obj.data.bones:
                    mapped = bone_map.get(bone.name, "[nicht gemappt]")
                    row = box.row()
                    row.label(text=f"{bone.name}", icon='BONE_DATA')
                    row.label(text=f"→ {mapped}")
                    if (bone.name.startswith('ORG-') or bone.name.startswith('DEF-')) and mapped == "[nicht gemappt]":
                        rigify_unmapped = True
                if rigify_unmapped:
                    box.label(text="Warnung: Rigify-Bones erkannt, aber nicht gemappt!", icon='ERROR')
            else:
                box.label(text="Kein Armature-Objekt ausgewählt.", icon='ERROR')
        layout.separator()
        col2 = layout.column(align=True)
        col2.label(text="Einstellungen speichern/laden", icon='FILE_FOLDER')
        col2.operator("characterrebuilder.save_settings", icon='EXPORT')
        col2.operator("characterrebuilder.load_settings", icon='IMPORT')
        layout.separator()
        col3 = layout.column(align=True)
        col3.label(text="Eigenes Preset speichern", icon='PRESET')
        col3.operator("characterrebuilder.save_preset", icon='PLUS')

class CHARACTERREBUILDER_OT_save_preset(bpy.types.Operator):
    bl_idname = "characterrebuilder.save_preset"
    bl_label = "Preset aus Charakter speichern"
    bl_description = "Speichert die aktuelle Knochenzuordnung als neues Preset (.crc)"

    filepath = bpy.props.StringProperty(
        name="Dateipfad",
        description="CharacterRebuilderConfig-Preset (*.crc)",
        default="",
        subtype='FILE_PATH',
    )
    filter_glob = bpy.props.StringProperty(
        default="*.crc",
        options={'HIDDEN'}
    )

    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Bitte ein Armature-Objekt auswählen.")
            return {'CANCELLED'}
        # Mapping: Quellname -> Zielname (wie aktuell im Rig)
        bone_map = collections.OrderedDict()
        for bone in obj.data.bones:
            bone_map[bone.name] = bone.name
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(bone_map, f, indent=2)
            self.report({'INFO'}, f"Preset gespeichert: {os.path.basename(self.filepath)}")
        except Exception as e:
            self.report({'ERROR'}, f"Fehler beim Speichern: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}



# Dummy-Operatoren (Platzhalter für spätere Implementierung)
class CHARACTERREBUILDER_OT_rename_bones(bpy.types.Operator):
    bl_idname = "characterrebuilder.rename_bones"
    bl_label = "Knochen umbenennen"
    bl_description = "Benennt Knochen nach SL/OpenSim-Konventionen um"



    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Bitte ein Armature-Objekt auswählen.")
            return {'CANCELLED'}
        # Hole das aktuell gewählte Preset
        preset = getattr(context.scene, "characterrebuilder_preset", "Second Life Default")
        bone_map = PRESETS.get(preset, SL_BONE_MAP)
        renamed = 0
        for bone in obj.data.bones:
            if bone.name in bone_map:
                new_name = bone_map[bone.name]
                if bone.name != new_name:
                    bone.name = new_name
                    renamed += 1
                elif bone.name == new_name:
                    renamed += 1
        # Rückmeldung an den Nutzer
        if renamed == 0:
            self.report({'WARNING'}, "Keine Knochen wurden umbenannt. Prüfe das Mapping und die Namen im Rig.")
        else:
            self.report({'INFO'}, f"{renamed} Knochen wurden umbenannt (Preset: {preset}).")
        return {'FINISHED'}

class CHARACTERREBUILDER_OT_weight_bones(bpy.types.Operator):
    bl_idname = "characterrebuilder.weight_bones"
    bl_label = "Knochen gewichten"
    bl_description = "Passt Knochengewichte für SL/OpenSim an"

    def execute(self, context):
        armature = context.object
        if not armature or armature.type != 'ARMATURE':
            self.report({'ERROR'}, "Bitte ein Armature-Objekt auswählen.")
            return {'CANCELLED'}
        meshes = get_meshes_with_armature(armature)
        affected = 0
        for mesh in meshes:
            # Übertrage alle Vertex Groups aus Armature auf Mesh (nur Namen)
            for bone in armature.data.bones:
                if bone.name not in mesh.vertex_groups:
                    mesh.vertex_groups.new(name=bone.name)
            affected += 1
        self.report({'INFO'}, f"Gewichte für {affected} Meshes angepasst (Gruppen übernommen, keine Werte kopiert).")
        return {'FINISHED'}

class CHARACTERREBUILDER_OT_save_settings(bpy.types.Operator):
    bl_idname = "characterrebuilder.save_settings"
    bl_label = "Einstellungen speichern"
    bl_description = "Speichert aktuelle Knochen- und Gewichtseinstellungen in eine Datei"

    filepath = bpy.props.StringProperty(
        name="Dateipfad",
        description="CharacterRebuilderConfig-Datei (*.crc)",
        default="",
        subtype='FILE_PATH',
    )

    filter_glob = bpy.props.StringProperty(
        default="*.crc",
        options={'HIDDEN'}
    )

    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Bitte ein Armature-Objekt auswählen.")
            return {'CANCELLED'}
        data = {}
        # Knochen-Namen und Gewichte sammeln
        data['bones'] = {}
        for bone in obj.data.bones:
            data['bones'][bone.name] = {
                'head': list(bone.head_local),
                'tail': list(bone.tail_local),
                'roll': getattr(bone, 'roll', 0.0)
            }
        # Vertex Groups (Gewichte)
        data['vertex_groups'] = {}
        # Suche Meshes mit Armature Modifier
        meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
        for mesh in meshes:
            for mod in mesh.modifiers:
                if mod.type == 'ARMATURE' and mod.object == obj:
                    vg_data = {}
                    for vg in mesh.vertex_groups:
                        vg_data[vg.name] = {}
                    # Speichere Gewichte pro Vertex
                    for v in mesh.data.vertices:
                        for g in v.groups:
                            group = mesh.vertex_groups[g.group].name
                            if group not in vg_data:
                                vg_data[group] = {}
                            vg_data[group][str(v.index)] = g.weight
                    data['vertex_groups'][mesh.name] = vg_data
        # ...existing code...
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            self.report({'INFO'}, f"Einstellungen gespeichert: {os.path.basename(self.filepath)}")
        except Exception as e:
            self.report({'ERROR'}, f"Fehler beim Speichern: {e}")
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class CHARACTERREBUILDER_OT_load_settings(bpy.types.Operator):
    bl_idname = "characterrebuilder.load_settings"
    bl_label = "Einstellungen laden"
    bl_description = "Lädt Knochen- und Gewichtseinstellungen aus einer Datei"

    filepath = bpy.props.StringProperty(
        name="Dateipfad",
        description="CharacterRebuilderConfig-Datei (*.crc)",
        default="",
        subtype='FILE_PATH',
    )

    filter_glob = bpy.props.StringProperty(
        default="*.crc",
        options={'HIDDEN'}
    )

    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Bitte ein Armature-Objekt auswählen.")
            return {'CANCELLED'}
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.report({'ERROR'}, f"Fehler beim Laden: {e}")
            return {'CANCELLED'}
        # Fallback: Wenn Datei nur ein Mapping enthält (Preset), führe Umbenennung durch
        if 'bones' not in data:
            renamed = 0
            for bone in obj.data.bones:
                if bone.name in data:
                    bone.name = data[bone.name]
                    renamed += 1
            self.report({'INFO'}, f"{renamed} Knochen wurden umbenannt (Preset geladen: {os.path.basename(self.filepath)})")
            return {'FINISHED'}
        # Knochen umbenennen und Positionen zurücksetzen
        for bone in obj.data.bones:
            if bone.name in data['bones']:
                bone.head_local = data['bones'][bone.name]['head']
                bone.tail_local = data['bones'][bone.name]['tail']
                bone.roll = data['bones'][bone.name]['roll']
        # Vertex Groups (Gewichte) auf Meshes anwenden
        for mesh_name, vg_data in data.get('vertex_groups', {}).items():
            mesh = bpy.data.objects.get(mesh_name)
            if not mesh or mesh.type != 'MESH':
                continue
            # Stelle sicher, dass alle Gruppen existieren
            for group in vg_data.keys():
                if group not in mesh.vertex_groups:
                    mesh.vertex_groups.new(name=group)
            # Setze Gewichte
            for group, verts in vg_data.items():
                for v_idx, weight in verts.items():
                    v_idx = int(v_idx)
                    vg = mesh.vertex_groups.get(group)
                    if vg:
                        vg.add([v_idx], weight, 'REPLACE')
        self.report({'INFO'}, f"Einstellungen geladen: {os.path.basename(self.filepath)}")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

classes = (
    CHARACTERREBUILDER_Preferences,
    CHARACTERREBUILDER_PT_panel,
    CHARACTERREBUILDER_OT_rename_bones,
    CHARACTERREBUILDER_OT_weight_bones,
    CHARACTERREBUILDER_OT_save_settings,
    CHARACTERREBUILDER_OT_load_settings,
    CHARACTERREBUILDER_OT_save_preset,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # EnumProperty für Presets robust registrieren
    if not hasattr(bpy.types.Scene, "characterrebuilder_preset"):
        bpy.types.Scene.characterrebuilder_preset = bpy.props.EnumProperty(
            name="Preset",
            description="Bone-Mapping-Preset",
            items=[(k, k, "") for k in PRESETS.keys()],
            default="Second Life Default"
        )
    if not hasattr(bpy.types.Scene, "characterrebuilder_show_bonelist"):
        bpy.types.Scene.characterrebuilder_show_bonelist = bpy.props.BoolProperty(
            name="Bone-Mapping anzeigen",
            description="Zeige oder verstecke die Knochen-Mapping-Liste",
            default=False
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    if hasattr(bpy.types.Scene, "characterrebuilder_preset"):
        del bpy.types.Scene.characterrebuilder_preset
    if hasattr(bpy.types.Scene, "characterrebuilder_show_bonelist"):
        del bpy.types.Scene.characterrebuilder_show_bonelist

if __name__ == "__main__":
    register()
