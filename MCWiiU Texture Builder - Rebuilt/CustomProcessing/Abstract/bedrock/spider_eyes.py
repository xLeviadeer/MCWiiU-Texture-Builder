from CustomProcessing import Custom

class spider_eyes(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("abstract", "spiders", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)