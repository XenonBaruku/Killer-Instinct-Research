# Killer-Instinct-Research
Tools & binary templates for researching and reverse engineering model & texture formats from game Killer Instinct (2013).    

Currently work in progress. Not sure everything is correct.

## Binary Templates
 * <b>kipak.bt</b> - Parsing *.pak game archive file structures.
 * <b>kimesh.bt</b> - Parsing mesh files (usually *.kimesh) that unpacked from game pak archive.
 * <b>kitex.bt</b> - Parsing texture files (usually *.kitex) that unpacked from game pak archive.

## Tools
 * <b>Killer-Instinct-Blender-Tools</b> - Importing geometry data from *.kimesh files into Blender (3.0+).
 * <b>KIPakTool</b> - Tool for unpacking (and maybe packing in the future) paks from game.
 * <b>KITexConv</b> - Texture converter that converts *.kitex textures into DDS images.
 * <b>KI.bms</b> - QuickBMS script that used for extracting game files from *.pak archives. Imprvoed from an older script that I can't find where the source is. Fixed extraction issue with some stage paks.