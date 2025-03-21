from CustomProcessing import Custom

class compass(Custom.Function):
    def createImage(self):
        return Custom.runFunctionFromPath(
            "shared", 
            "stack_textures", 
            self.wiiuName, 
            self.type,
            self.wiiuImage, 
            True, # print recursion
            "clock_", # name
            True # pad zeros
        )