from abc import ABC, abstractmethod
import CustomProcessing.Custom
import Global
import CodeLibs.Logger as log
from CodeLibs.Logger import print
import CustomProcessing
import importlib
import Utility as ut
import Read as rd
import SizingImage
from builtins import type as typeof

class Function(ABC):
    """
    Description:
        a custom function base class that is intended to be extended for each custom function
    Important:
        - Custom function (class) names with spaces must be replaced with __ (double underscore)
    """

    def __init__(self, wiiuName, type, wiiuImage, isShared=False) -> None:
        """
        Description:
            all custom functions require wiiuName, type and wiiuImage
        """
        super().__init__()
        self.wiiuName = wiiuName
        self.type = type
        self.wiiuImage = wiiuImage
        self.isShared = isShared

    @abstractmethod
    def createImage(self):
        """
        Description:
            create function must be overriden, this is how the texture is processed. it must return an image
        """
        pass

# function to end the program if debug mode is disabled, or return an error image
def _closeProgramIfDebugFalse(name:str, message:str):
    if (Global.useErrorTexture == True):
        print(f"using error texture for texture {name}, because a function for it could not be found", log.ERROR)
        return Global.errorImage.resize(ut.size()) # resize to singular size on sheet if needed
    print(message, log.ERROR)
    Global.endProgram()

# function for getting a name with underscores
def formatName(name:str):
    """
    Description:
        formats a name with underscores
    """
    return name.replace(" ", "__")

# gets a class from CustomProcessing
def getClass(functionType:str, functionName:str):
    """
    Description:
        gets a custom class from the input (not an instance)
    ---
    Variables:
        - functionType : String <>
            - The location to find/type of custom function
            - Abstract
            - External
            - Versional
            - Shared
        - functionName : String <>
            - The name of the custom function you want to run
        - wiiuKey : String <>
            - The current wiiuName
        - type : String <>
            - The current type
        - wiiuImage : SizingImage <>
            - The current wiiuImage
    ---
    Returns:
        - A SizingImage proccessed by the respective custom function
    """
    
    # function to get the functionType module module
    def getFunctionTypeModule(root):
        match (str.lower(functionType) if isinstance(functionType, str) else functionType): # try to do .lower() on string, but if not just pass the value
            case "abstract":
                return root.Abstract
            case "external":
                return root.External
            case "versional":
                return root.Versional
            case "override":
                return root.Override
            case None | "shared":
                return root
            case _:
                Global.endProgram(f"\"{functionType}\" is not a valid functionType")
    
    # gets the game module from the function type
    def getGameModule(root):
        if (hasattr(root, "java")) or (hasattr(root, "bedrock")):
            if (Global.inputGame == "java"):
                return root.java
            elif (Global.inputGame == "bedrock"):
                return root.bedrock
            else:
                Global.endProgram("Custom > getClass > getGameModule > Global.inputGame wasn't set to a valid game name")
                return
        else: # if has no game/can't find game, return root
            return root
    
    functionNameUnderscores = formatName(functionName)
    
    # get root module for checking from
    checking_module = getGameModule(getFunctionTypeModule(CustomProcessing))

    # try to locate the specific module
    try:
        module = importlib.import_module(f"{checking_module.__name__}.{functionNameUnderscores}") # import the module and create an image with it
    except ImportError:
        return _closeProgramIfDebugFalse(functionName, f"could not find custom function file \"{functionNameUnderscores}\"")

    # check if the module has the right class name
    if hasattr(module, functionNameUnderscores):
        cls = getattr(module, functionNameUnderscores)  # get the class from the module
        if (not issubclass(cls, CustomProcessing.Custom.Function)): # if the class doesn't extend custom function class
            return _closeProgramIfDebugFalse(functionName, f"class \"{functionNameUnderscores}\" doesn't extend CustomFunction")
        return cls
    else:
        return _closeProgramIfDebugFalse(functionName, f"class \"{functionNameUnderscores}\" not found in module \"{functionNameUnderscores}\"")

# runs the function internally
def _runFunction(cls_instance:Function, isPrintRecursed:bool, *args):
    """
    Description
        internal function for running functions
    """
    
    args = args[0] # fixes multi-tupling
    functionName = cls_instance.__class__.__name__

    def generateImage():
        if (cls_instance.isShared == True):
            return cls_instance.createImage(args)
        else: # is not shared
            return cls_instance.createImage()
        
    output = generateImage() # try to generate the image
    if (output == None): # if no output was given, meaning the function returned nothing
        return _closeProgramIfDebugFalse(functionName, f"the function for \"{functionName}\" returned None")
    if (isPrintRecursed != None): # none = no print
        print(f"found function for \"{functionName}\" and returned", log.CUSTOMFUNCTION if (isPrintRecursed == False) else log.CUSTOMFUNCTIONRECURSION)
    return output

# runs a function from custom processing by using the class
def runFunctionFromInstance(cls_instance:Function, isPrintRecursed:bool=False, *args):
    """
    Description:
        runs a custom function according to the input
    ---
    Variables:
        - cls_instance : CustomProcessing.Custom.Function <>
            - A class instance to run the function from
        - wiiuKey : String <>
            - The current wiiuName
        - type : String <>
            - The current type
        - wiiuImage : SizingImage <>
            - The current wiiuImage
        - isPrintRecursed : int <0>
            - Whether or not the function was called as part of a recursion
            - If set to None, then no print is made
        - *args : A list of extra arguments. These can only be included when executing a shared function
    ---
    Returns:
        - A SizingImage proccessed by the respective custom function
    """
    
    return _runFunction(cls_instance, isPrintRecursed, args)

# runs a function from custom processing by using tree/folder pathing
def runFunctionFromPath(functionType:str, functionName:str, wiiuKey:str, type:str, wiiuImage:SizingImage, isPrintRecursed:bool=False, *args):
    """
    Description:
        runs a custom function according to the input
    ---
    Variables:
        - functionType : String <>
            - The location to find/type of custom function
            - Abstract
            - External
            - Versional
            - Shared
        - functionName : String <>
            - The name of the custom function you want to run
        - wiiuKey : String <>
            - The current wiiuName
        - type : String <>
            - The current type
        - wiiuImage : SizingImage <>
            - The current wiiuImage
        - isPrintRecursed : int <0>
            - Whether or not the function was called as part of a recursion
            - If set to None, then no print is made
        - *args : A list of extra arguments. These can only be included when executing a shared function
    ---
    Returns:
        - A SizingImage proccessed by the respective custom function
    """

    cls_instance = getClass(functionType, functionName)(wiiuKey, type, wiiuImage, isShared=(functionType.lower() == "shared"))
    return _runFunction(cls_instance, isPrintRecursed, args)