from CustomProcessing import Custom

class firework__star_colored(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("external", "firework__stars", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)