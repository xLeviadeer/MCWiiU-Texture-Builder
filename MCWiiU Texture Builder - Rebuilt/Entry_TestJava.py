from EntryPoint import EntryPoint
from CodeLibs import Logger as log
import Global

# set the name (must be set in the entry file)
Global.name = str(__name__)

# declare new entry point
entry = EntryPoint(
    executedFromC=False,
    errorMode="replace",
    processingSize=16,
    useComplexProcessing=True,
    debug=False,
    
    inputPath="F:\\Coding\\B- LeRe\\MCWiiU-Texture-Builder\\MCWiiU Texture Builder - Rebuilt\\base_textures\\1.13.2_java",
    inputPathType="folder",
    inputGame="java",
    inputVersion="1.13.2",
    
    outputPath="F:\\Coding\\B- LeRe\\MCWiiU-Texture-Builder\\MCWiiU Texture Builder - Rebuilt\\output",
    outputStructureIndex=2,
    outputDrive="system",

    logging=[],
    showTracebacks=False,
    isDirectPath=True,
    useErrorTexture=False
)

# run entry point
entry.start()