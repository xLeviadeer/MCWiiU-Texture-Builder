from CustomProcessing import Custom

class vex_charging(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath("shared", "vex_process", self.wiiuName, self.type, self.wiiuImage, isPrintRecursed=True)