from CustomProcessing import Custom

class horse_armor_leather_1_b(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("abstract", "horse_armor_leather", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)