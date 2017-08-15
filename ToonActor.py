from Data import *
from Head import ToonHead
from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

class ToonActor(ToonHead):
    def __init__(self, models, legs, torso, head):
        ToonHead.__init__(self)
        self.models = models
        self.LegsAnimDict = legs
        self.TorsoAnimDict = torso
        self.HeadAnimDict = head

    def buildTorso(self):
        torso = TorsoDict.get(self.torso)
        if torso is None:
            raise Exception("Unable to build torso")

        self.loadModel(self.models[torso], 'torso', 'lodRoot', True)
        self.loadAnims(self.TorsoAnimDict[self.torso], 'torso', 'lodRoot')
        self.showPart('torso')

    def buildLegs(self):
        legs = LegDict.get(self.legs)
        if legs is None:
            raise Exception("Unable to build legs")

        self.loadModel(self.models[legs], 'legs', 'lodRoot', True)
        self.loadAnims(self.LegsAnimDict[self.legs], 'legs', 'lodRoot')
        self.findAllMatches('**/boots_short').stash()
        self.findAllMatches('**/boots_long').stash()
        self.findAllMatches('**/shoes').stash()
        self.showPart('legs')

    def applyClothes(self):
        swappedTorso = 0
        if self.gender == 'f':
            try:
                bottomPair = GirlBottoms[self.botTex]
            except:
                bottomPair = GirlBottoms[0]

        try:
            texName = Shirts[self.topTex]
        except:
            texName = Shirts[0]

        shirtTex = loader.loadTexture(texName, okMissing=True)
        if shirtTex is None:
            raise Exception("Unable to load clothes")

        shirtTex.setMinfilter(Texture.FTLinearMipmapLinear)
        shirtTex.setMagfilter(Texture.FTLinear)
        try:
            shirtColor = ClothesColors[self.topTexColor]
        except:
            shirtColor = ClothesColors[0]

        try:
            texName = Sleeves[self.sleeveTex]
        except:
            texName = Sleeves[0]

        sleeveTex = loader.loadTexture(texName, okMissing=True)
        if sleeveTex is None:
            raise Exception("Unable to load clothes")

        sleeveTex.setMinfilter(Texture.FTLinearMipmapLinear)
        sleeveTex.setMagfilter(Texture.FTLinear)
        try:
            sleeveColor = ClothesColors[self.sleeveTexColor]
        except:
            sleeveColor = ClothesColors[0]

        if self.gender == 'm':
            try:
                texName = BoyShorts[self.botTex]
            except:
                texName = BoyShorts[0]

        else:
            try:
                texName = GirlBottoms[self.botTex][0]
            except:
                texName = GirlBottoms[0][0]

        bottomTex = loader.loadTexture(texName, okMissing=True)
        if bottomTex is None:
            raise Exception("Unable to load clothes")

        bottomTex.setMinfilter(Texture.FTLinearMipmapLinear)
        bottomTex.setMagfilter(Texture.FTLinear)
        try:
            bottomColor = ClothesColors[self.botTexColor]
        except:
            bottomColor = ClothesColors[0]

        darkBottomColor = bottomColor * 0.5
        darkBottomColor.setW(1.0)

        thisPart = self.getPart('torso', 'lodRoot')
        top = thisPart.find('**/torso-top')
        top.setTexture(shirtTex, 1)
        top.setColor(shirtColor)
        sleeves = thisPart.find('**/sleeves')
        sleeves.setTexture(sleeveTex, 1)
        sleeves.setColor(sleeveColor)
        bottoms = thisPart.findAllMatches('**/torso-bot')
        for bottomNum in xrange(0, bottoms.getNumPaths()):
            bottom = bottoms.getPath(bottomNum)
            bottom.setTexture(bottomTex, 1)
            bottom.setColor(bottomColor)

        caps = thisPart.findAllMatches('**/torso-bot-cap')
        caps.setColor(darkBottomColor)

    def applyColors(self):
        parts = self.findAllMatches('**/head*')
        parts.setColor(self.headColor)
        animalType = self.getAnimal()
        if animalType == 'cat' or animalType == 'rabbit' or animalType == 'bear' or animalType == 'mouse' or animalType == 'pig' or animalType == 'deer' or animalType == 'beaver':
            parts = self.findAllMatches('**/ear?-*')
            parts.setColor(self.headColor)

        armColor = self.armColor
        gloveColor = self.gloveColor
        legColor = self.legColor

        torso = self.getPart('torso', 'lodRoot')
        if len(self.torso) == 1:
            parts = torso.findAllMatches('**/torso*')
            parts.setColor(*armColor)

        for pieceName in ('arms', 'neck'):
            piece = torso.find('**/' + pieceName)
            piece.setColor(*armColor)

        hands = torso.find('**/hands')
        hands.setColor(*gloveColor)
        legs = self.getPart('legs', 'lodRoot')
        for pieceName in ('legs', 'feet'):
            piece = legs.find('**/%s;+s' % pieceName)
            piece.setColor(*legColor)

    def stitchToon(self):
        print(self.getJoints())
        self.attach('head', 'torso', 'def_head')
        self.attach('torso', 'legs', 'joint_hips')

    def buildHead(self):
        self.loadHead(self.head)
        if self.getAnimal() == 'dog':
            self.loadAnims(self.HeadAnimDict[self.head], 'head', 'lodRoot')

    def buildToon(self):
        # loadDNA must be called before this
        self.buildTorso()
        self.buildLegs()
        self.buildHead()
        self.applyColors()
        self.applyClothes()
        self.stitchToon()

        anim = 'neutral'
        self.pose(anim, 1)
        self.loop(anim, restart=0)
        self.setPlayRate(1, anim)
        self.playingAnim = anim

    def loadDNA(self, dna):
        dg = PyDatagram(dna)
        dgi = PyDatagramIterator(dg)
        self.type = dgi.getFixedString(1)
        if self.type == 't':
            headIndex = dgi.getUint8()
            torsoIndex = dgi.getUint8()
            legsIndex = dgi.getUint8()
            self.head = toonHeadTypes[headIndex]
            self.torso = toonTorsoTypes[torsoIndex]
            self.legs = toonLegTypes[legsIndex]
            gender = dgi.getUint8()
            if gender == 1:
                self.gender = 'm'
            else:
                self.gender = 'f'
            self.topTex = dgi.getUint8()
            self.topTexColor = dgi.getUint8()
            self.sleeveTex = dgi.getUint8()
            self.sleeveTexColor = dgi.getUint8()
            self.botTex = dgi.getUint8()
            self.botTexColor = dgi.getUint8()
            try:
                self.armColor = (dgi.getFloat64(), dgi.getFloat64(), dgi.getFloat64(), 1.0)
                self.gloveColor = (dgi.getFloat64(), dgi.getFloat64(), dgi.getFloat64(), 1.0)
                self.legColor = (dgi.getFloat64(), dgi.getFloat64(), dgi.getFloat64(), 1.0)
                self.headColor = (dgi.getFloat64(), dgi.getFloat64(), dgi.getFloat64(), 1.0)
            except:
                self.armColor = dgi.getUint8()
                self.gloveColor = dgi.getUint8()
                self.legColor = dgi.getUint8()
                self.headColor = dgi.getUint8()
                self.armColor = allColorsList[self.armColor]
                self.gloveColor = allColorsList[self.gloveColor]
                self.legColor = allColorsList[self.legColor]
                self.headColor = allColorsList[self.headColor]
        else:
            print(self.type)
            raise Exception("Error parsing net string")
        return None

