import util
import DecisionTree.project2 as DT
import HEC.project3 as HEC

class Protein:
    def __init__(self, proteinName):
        self._proteinName = proteinName

    def setFastaFile(self, fastaFile):
        self._fastaFile = fastaFile
        proteinName, sequence = util.decodeFastaformat(fastaFile)[0]
        self._sequence = sequence

    def getFastaFile(self):
        return self._fastaFile

    def getSequence(self):
        return self._sequence

    def getProteinName(self):
        return self._proteinName

    def setPssmFile(self, pssmFile):
        self._pssmFile = pssmFile

    def getPssmFile(self):
        return self._pssmFile

    def setPdbFile(self, pdbFile):
        self._pdbFile = pdbFile

    def getPdbFile(self):
        return self._pdbFile

    def getTmScoreAvg(self, tmAlignProg, otherProtein):
        scores = util.tmAlign(tmAlignProg, self.getPdbFile(), otherProtein.getPdbFile())
        return sum(scores)/float(len(scores))

    def getHECAvgs(self):
        _HECAvg = getattr(self, "_HECAvg", None)
        if _HECAvg is None:
            HECString = HEC.main(self._pssmFile, self._fastaFile)
            HECAvg = dict()
            HECAvg['H']=float(HECString.count('H'))/len(HECString)
            HECAvg['E']=float(HECString.count('E'))/len(HECString)
            HECAvg['C']=float(HECString.count('C'))/len(HECString)
            self._HECAvg = HECAvg
            _HECAvg = self._HECAvg
        return _HECAvg

    def getExposedBuriedAvgs(self):
        _burExpAvg = getattr(self, "_burExpAvg", None)
        if _burExpAvg is None:
            DTprediction = DT.predict(self._fastaFile)
            burExpAvg = dict()
            burExpAvg['exp'] = float(DTprediction.count('e'))/len(DTprediction)
            burExpAvg['bur'] = float(DTprediction.count('-'))/len(DTprediction)
            self._burExpAvg = burExpAvg
            _burExpAvg = self._burExpAvg
        return _burExpAvg 

    def getPssmAvgs(self):
        _pssmAvgs = getattr(self, "_pssmAvgs", None)
        if _pssmAvgs is None:
            sequenceName, sequence, pssmHeader, pssmSequence = util.readPSSMNew(self.getPssmFile())
            pssmFeatures = util.slidingWindow(pssmSequence, 1)
            self._pssmAvgs = util.columnAvg(pssmFeatures, 100)
            _pssmAvgs = self._pssmAvgs
        return _pssmAvgs

