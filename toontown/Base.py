from Data import *
from ToonActor import ToonActor
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import os
import uuid

class ToonView(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.Preloaded = {}
        self.LegsAnimDict = {}
        self.TorsoAnimDict = {}
        self.HeadAnimDict = {}

    def loadAnimations(self):
        phaseList = [Phase3AnimList,
                     Phase3_5AnimList,
                     Phase4AnimList,
                     Phase5AnimList,
                     Phase5_5AnimList,
                     Phase6AnimList,
                     Phase9AnimList,
                     Phase10AnimList,
                     Phase12AnimList]
        phaseStrList = ['phase_3',
                        'phase_3.5',
                        'phase_4',
                        'phase_5',
                        'phase_5.5',
                        'phase_6',
                        'phase_9',
                        'phase_10',
                        'phase_12']
        for animList in phaseList:
            phaseStr = phaseStrList[phaseList.index(animList)]
            for key in LegDict.keys():
                self.LegsAnimDict.setdefault(key, {})
                for anim in animList:
                    file = phaseStr + LegDict[key] + anim[1] + ".bam"
                    self.LegsAnimDict[key][anim[0]] = file

            for key in TorsoDict.keys():
                self.TorsoAnimDict.setdefault(key, {})
                for anim in animList:
                    file = phaseStr + TorsoDict[key] + anim[1] + ".bam"
                    self.TorsoAnimDict[key][anim[0]] = file

            for key in HeadDict.keys():
                if key.find('d') >= 0:
                    self.HeadAnimDict.setdefault(key, {})
                    for anim in animList:
                        file = phaseStr + HeadDict[key] + anim[1] + ".bam"
                        self.HeadAnimDict[key][anim[0]] = file

    def loadModels(self):
        getModelPath().appendDirectory(('%s/resources/' % (os.getcwd())))
        for key in TorsoDict.keys():
            fileRoot = TorsoDict[key]
            self.Preloaded[fileRoot] = loader.loadModel('phase_3' + fileRoot + "1000.bam")

        for key in LegDict.keys():
            fileRoot = LegDict[key]
            self.Preloaded[fileRoot] = loader.loadModel('phase_3' + fileRoot + "1000.bam")

        for key in HeadDict.keys():
            fileRoot = HeadDict[key]
            self.Preloaded[fileRoot] = loader.loadModel('phase_3' + fileRoot + '1000.bam')
            self.Preloaded[fileRoot].flattenMedium()

        self.loadAnimations()

    def takeScreenshot(self, task):
        file_name = Filename(str(uuid.uuid4()) + ".png")
        print ('file: %s' % (file_name))
        self.win.saveScreenshot(file_name)
        self.toon.removeNode()

    def displayDNA(self, dna):
        self.toon = ToonActor(self.Preloaded, self.LegsAnimDict, self.TorsoAnimDict, self.HeadAnimDict)
        self.toon.loadDNA(dna)
        self.toon.buildToon()
        self.toon.reparentTo(self.render)
        self.toon.setPos(0, 9, -2.1)
        self.toon.setHpr(-180, 0, 0)
        taskMgr.doMethodLater(0.1, self.takeScreenshot, 'screenshotTask')

    def cleanup(self):
        if self.toon:
            self.toon.disable()

        self.destroy()
