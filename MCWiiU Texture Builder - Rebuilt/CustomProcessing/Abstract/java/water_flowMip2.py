from CustomProcessing import Custom

class water_flowMip2(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("shared", "water_process", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)