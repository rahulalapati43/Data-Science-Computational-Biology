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

    def setPssmFile(self, pssmFile):
        self._pssmFile = pssmFile

    def setPdbFile(self, pdbFile):
        self._pdbFile = pdbFile

    def getTmScore(self):
        pass

    def setHECAvgs(self):
        HECString = HEC.main(self._pssmFile,self._fastaFile)
        HECAvg = dict()
        HECAvg['H']=float(HECString.count('H'))/len(HECString)
        HECAvg['E']=float(HECString.count('E'))/len(HECString)
        HECAvg['C']=float(HECString.count('C'))/len(HECString)
        self._HECAvg = HECAvg

    def getHECAvgs(self):
        return self._HECAvg

    def setExposedBuriedAvgs(self):
        DTprediction = DT.predict(self._fastaFile)
        burExpAvg = dict()
        burExpAvg['exp'] = float(DTprediction.count('e'))/len(DTprediction)
        burExpAvg['bur'] = float(DTprediction.count('-'))/len(DTprediction)
        self._burExpAvg = burExpAvg

    def getExposedBuriedAvgs(self):
        return self._burExpAvg

    def setPssm(self, pssm):
        self._pssm = pssm

    def getPssm(self):
        return self._pssm

    def setPssmAvgs(self, pssmAvgs):
        self._pssmAvgs = pssmAvgs

    def getPssmAvgs(self):
        return self._pssmAvgs


