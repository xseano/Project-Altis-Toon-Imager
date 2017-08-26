from Data import *
from panda3d.core import *
from direct.actor import Actor

class ToonHead(Actor.Actor):
    def __init__(self):
        Actor.Actor.__init__(self)
        self.models = None

    def getAnimal(self):
        if self.head[0] == 'd':
            return 'dog'
        elif self.head[0] == 'c':
            return 'cat'
        elif self.head[0] == 'm':
            return 'mouse'
        elif self.head[0] == 'h':
            return 'horse'
        elif self.head[0] == 'r':
            return 'rabbit'
        elif self.head[0] == 'f':
            return 'duck'
        elif self.head[0] == 'p':
            return 'monkey'
        elif self.head[0] == 'b':
            return 'bear'
        elif self.head[0] == 's':
            return 'pig'
        elif self.head[0] == 'x':
            return 'deer'
        elif self.head[0] == 'z':
            return 'beaver'
        elif self.head[0] == 'a':
            return 'alligator'
        else:
            notify.error('unknown headStyle: ', self.head[0])

    def __fixHeadLongLong(self):
        searchRoot = self
        otherParts = searchRoot.findAllMatches('**/*short*')
        for partNum in range(0, otherParts.getNumPaths()):
            otherParts.getPath(partNum).stash()

    def __fixHeadLongShort(self, copy=False):
        animalType = self.getAnimal()
        headStyle = self.head
        searchRoot = self
        if animalType != 'duck' and animalType != 'horse' and animalType != 'alligator':
            if animalType == 'rabbit':
                if copy:
                    searchRoot.find('**/ears-long').removeNode()
                else:
                    searchRoot.find('**/ears-long').hide()
            elif copy:
                searchRoot.find('**/ears-short').removeNode()
            else:
                searchRoot.find('**/ears-short').hide()
        if animalType != 'rabbit':
            if copy:
                searchRoot.find('**/eyes-short').removeNode()
            else:
                searchRoot.find('**/eyes-short').hide()
        if animalType != 'dog':
            if copy:
                searchRoot.find('**/joint_pupilL_short').removeNode()
                searchRoot.find('**/joint_pupilR_short').removeNode()
            else:
                searchRoot.find('**/joint_pupilL_short').stash()
                searchRoot.find('**/joint_pupilR_short').stash()
        if copy:
            self.find('**/head-short').removeNode()
            self.find('**/head-front-short').removeNode()
        else:
            self.find('**/head-short').hide()
            self.find('**/head-front-short').hide()
        if animalType != 'rabbit':
            muzzleParts = searchRoot.findAllMatches('**/muzzle-long*')
            for partNum in range(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                else:
                    muzzleParts.getPath(partNum).hide()

        else:
            muzzleParts = searchRoot.findAllMatches('**/muzzle-short*')
            for partNum in range(0, muzzleParts.getNumPaths()):
                muzzleParts.getPath(partNum).hide()

    def __fixHeadShortShort(self):
        searchRoot = self
        otherParts = searchRoot.findAllMatches('**/*long*')
        for partNum in range(0, otherParts.getNumPaths()):
            otherParts.getPath(partNum).stash()

    def __fixHeadShortLong(self, copy=False):
        animalType = self.getAnimal()
        headStyle = self.head
        searchRoot = self
        if animalType != 'duck' and animalType != 'horse' and animalType != 'alligator':
            if animalType == 'rabbit':
                if copy:
                    searchRoot.find('**/ears-short').removeNode()
                else:
                    searchRoot.find('**/ears-short').hide()
            elif copy:
                searchRoot.find('**/ears-long').removeNode()
            else:
                searchRoot.find('**/ears-long').hide()
        if animalType != 'rabbit':
            if copy:
                searchRoot.find('**/eyes-long').removeNode()
            else:
                searchRoot.find('**/eyes-long').hide()
        if animalType != 'dog':
            if copy:
                searchRoot.find('**/joint_pupilL_long').removeNode()
                searchRoot.find('**/joint_pupilR_long').removeNode()
            else:
                searchRoot.find('**/joint_pupilL_long').stash()
                searchRoot.find('**/joint_pupilR_long').stash()
        if copy:
            searchRoot.find('**/head-long').removeNode()
            searchRoot.find('**/head-front-long').removeNode()
        else:
            searchRoot.find('**/head-long').hide()
            searchRoot.find('**/head-front-long').hide()
        if animalType != 'rabbit':
            muzzleParts = searchRoot.findAllMatches('**/muzzle-short*')
            for partNum in range(0, muzzleParts.getNumPaths()):
                if copy:
                    muzzleParts.getPath(partNum).removeNode()
                else:
                    muzzleParts.getPath(partNum).hide()

        else:
            muzzleParts = searchRoot.findAllMatches('**/muzzle-long*')
            for partNum in range(0, muzzleParts.getNumPaths()):
                muzzleParts.getPath(partNum).hide()

    def loadHead(self, models, headStyle):
        self.models = models
        fix = None
        if headStyle == 'dls':
            filePrefix = HeadDict['dls']
            headHeight = 0.75
        elif headStyle == 'dss':
            filePrefix = HeadDict['dss']
            headHeight = 0.5
        elif headStyle == 'dsl':
            filePrefix = HeadDict['dsl']
            headHeight = 0.5
        elif headStyle == 'dll':
            filePrefix = HeadDict['dll']
            headHeight = 0.75
        elif headStyle == 'cls':
            filePrefix = HeadDict['c']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'css':
            filePrefix = HeadDict['c']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'csl':
            filePrefix = HeadDict['c']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'cll':
            filePrefix = HeadDict['c']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'hls':
            filePrefix = HeadDict['h']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'hss':
            filePrefix = HeadDict['h']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'hsl':
            filePrefix = HeadDict['h']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'hll':
            filePrefix = HeadDict['h']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'mls':
            filePrefix = HeadDict['m']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'mss':
            filePrefix = HeadDict['m']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'rls':
            filePrefix = HeadDict['r']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'rss':
            filePrefix = HeadDict['r']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'rsl':
            filePrefix = HeadDict['r']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'rll':
            filePrefix = HeadDict['r']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'fls':
            filePrefix = HeadDict['f']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'fss':
            filePrefix = HeadDict['f']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'fsl':
            filePrefix = HeadDict['f']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'fll':
            filePrefix = HeadDict['f']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'pls':
            filePrefix = HeadDict['p']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'pss':
            filePrefix = HeadDict['p']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'psl':
            filePrefix = HeadDict['p']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'pll':
            filePrefix = HeadDict['p']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'bls':
            filePrefix = HeadDict['b']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'bss':
            filePrefix = HeadDict['b']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'bsl':
            filePrefix = HeadDict['b']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'bll':
            filePrefix = HeadDict['b']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'sls':
            filePrefix = HeadDict['s']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'sss':
            filePrefix = HeadDict['s']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'ssl':
            filePrefix = HeadDict['s']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'sll':
            filePrefix = HeadDict['s']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'xls':
            filePrefix = HeadDict['x']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'xss':
            filePrefix = HeadDict['x']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'xsl':
            filePrefix = HeadDict['x']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'xll':
            filePrefix = HeadDict['x']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'zls':
            filePrefix = HeadDict['z']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'zss':
            filePrefix = HeadDict['z']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'zsl':
            filePrefix = HeadDict['z']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'zll':
            filePrefix = HeadDict['z']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        elif headStyle == 'als':
            filePrefix = HeadDict['a']
            fix = self.__fixHeadLongShort
            headHeight = 0.75
        elif headStyle == 'ass':
            filePrefix = HeadDict['a']
            fix = self.__fixHeadShortShort
            headHeight = 0.5
        elif headStyle == 'asl':
            filePrefix = HeadDict['a']
            fix = self.__fixHeadShortLong
            headHeight = 0.5
        elif headStyle == 'all':
            filePrefix = HeadDict['a']
            fix = self.__fixHeadLongLong
            headHeight = 0.75
        else:
            ToonHead.notify.error('unknown head style: %s' % headStyle)

        self.loadModel(self.models[filePrefix], 'head', 'lodRoot')
        self.showAllParts('head')
        if fix != None:
            print(fix)
            fix()

        self.__fixEyes()
        self.setupEyelashes()
        self.setupMuzzles()
        return headHeight

    def setupMuzzles(self):
        def hideItem(item):
            item.hide()

        if self.getAnimal() != 'dog':
            muzzle = self.find('**/muzzle*neutral')
        else:
            muzzle = self.find('**/muzzle*')
            filePrefix = DogMuzzleDict[self.head]
            muzzles = loader.loadModel('phase_3' + filePrefix + '1000.bam')
            if not self.find('**/def_head').isEmpty():
                muzzles.reparentTo(self.find('**/def_head'))

        surpriseMuzzle = self.find('**/muzzle*surprise')
        angryMuzzle = self.find('**/muzzle*angry')
        sadMuzzle = self.find('**/muzzle*sad')
        smileMuzzle = self.find('**/muzzle*smile')
        laughMuzzle = self.find('**/muzzle*laugh')
        hideItem(surpriseMuzzle)
        hideItem(angryMuzzle)
        hideItem(sadMuzzle)
        hideItem(smileMuzzle)
        hideItem(laughMuzzle)

    def setupEyelashes(self):
        if self.gender == 'm':
            print("not loading eyelashes")
        else:
            animal = self.head[0]
            model = loader.loadModel('phase_3' + EyelashDict[animal] + ".bam")
            head = self.getPart('head', 'lodRoot')
            length = self.head[1]
            if length == 'l':
                openString = 'open-long'
            else:
                openString = 'open-short'

            self.__eyelashOpen = model.find('**/' + openString).copyTo(head)
            model.removeNode()
        return

    def __fixEyes(self):
        mode = -3

        self.drawInFront('eyes*', 'head-front*', mode)
        if not self.find('joint_pupil*').isEmpty():
            self.drawInFront('joint_pupil*', 'eyes*', -1)
        else:
            self.drawInFront('def_*_pupil', 'eyes*', -1)

        self.__eyes = self.find('**/eyes*')

        if not self.__eyes.isEmpty():
            self.__eyes.setColorOff()
            self.__lpupil = None
            self.__rpupil = None

            if not self.find('**/joint_pupilL*').isEmpty():
                if self.getLOD(1000):
                    lp = self.getLOD(1000).find('**/joint_pupilL*')
                    rp = self.getLOD(1000).find('**/joint_pupilR*')
                else:
                    lp = self.find('**/joint_pupilL*')
                    rp = self.find('**/joint_pupilR*')
            elif not self.getLOD(1000):
                lp = self.find('**/def_left_pupil*')
                rp = self.find('**/def_right_pupil*')
            else:
                lp = self.getLOD(1000).find('**/def_left_pupil*')
                rp = self.getLOD(1000).find('**/def_right_pupil*')


            if lp.isEmpty() or rp.isEmpty():
                print ('Unable to locate pupils.')
            else:
                leye = self.__eyes.attachNewNode('leye')
                reye = self.__eyes.attachNewNode('reye')
                lmat = Mat4(0.802174, 0.59709, 0, 0, -0.586191, 0.787531, 0.190197, 0, 0.113565, -0.152571, 0.981746, 0, -0.233634, 0.418062, 0.0196875, 1)
                leye.setMat(lmat)
                rmat = Mat4(0.786788, -0.617224, 0, 0, 0.602836, 0.768447, 0.214658, 0, -0.132492, -0.16889, 0.976689, 0, 0.233634, 0.418062, 0.0196875, 1)
                reye.setMat(rmat)
                self.__lpupil = leye.attachNewNode('lpupil')
                self.__rpupil = reye.attachNewNode('rpupil')
                lpt = self.__eyes.attachNewNode('')
                rpt = self.__eyes.attachNewNode('')
                lpt.wrtReparentTo(self.__lpupil)
                rpt.wrtReparentTo(self.__rpupil)
                lp.reparentTo(lpt)
                rp.reparentTo(rpt)
                self.__lpupil.adjustAllPriorities(1)
                self.__rpupil.adjustAllPriorities(1)
                animalType = self.getAnimal()
                if animalType != 'dog':
                    self.__lpupil.flattenStrong()
                    self.__rpupil.flattenStrong()

        return
