from CustomProcessing import Custom

class break_4(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("external", "breaks", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)