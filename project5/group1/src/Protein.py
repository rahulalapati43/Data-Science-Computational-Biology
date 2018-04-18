import util

class Protein:
    def __init__(self, proteinName):
        self._proteinName = proteinName

    def setFastaFile(self, fastaFile):
        self._fastaFile = fastaFile
        proteinName, sequence = util.decodeFastaformat(fastaFile)[0]
        self._sequence = sequence

    def getSequence(self):
        return self._sequence

    def setPssmFile(self, pssmFile):
        self._pssmFile = pssmFile

    def setPdbFile(self, pdbFile):
        self._pdbFile = pdbFile

    def getTmScore(self):
        pass

    def getHECAvgs(self):
        pass

    def getExposedBuriedAvgs(self):
        pass

    def getPssmAvgs(self):
        pass


