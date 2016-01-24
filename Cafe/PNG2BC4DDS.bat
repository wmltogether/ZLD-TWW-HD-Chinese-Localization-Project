AMDCompressCLI.exe -nomipmap -fd BC4 inPNG/font.0.Png inDDS/font.0.dds
AMDCompressCLI.exe -nomipmap -fd BC4 inPNG/font.1.Png inDDS/font.1.dds
AMDCompressCLI.exe -nomipmap -fd BC4 inPNG/font.2.Png inDDS/font.2.dds
AMDCompressCLI.exe -nomipmap -fd BC4 inPNG/font.3.Png inDDS/font.3.dds
AMDCompressCLI.exe -nomipmap -fd BC4 inPNG/font.4.Png inDDS/font.4.dds
AMDCompressCLI.exe -nomipmap -fd BC4 inPNG/font.5.Png inDDS/font.5.dds
AMDCompressCLI.exe -nomipmap -fd BC4 inPNG/font.6.Png inDDS/font.6.dds
AMDCompressCLI.exe -nomipmap -fd BC4 inPNG/font.7.Png inDDS/font.7.dds
AMDCompressCLI.exe -nomipmap -fd BC4 inPNG/font.8.Png inDDS/font.8.dds
AMDCompressCLI.exe -nomipmap -fd BC4 inPNG/font.9.Png inDDS/font.9.dds

TexConv2.exe -i inDDS/font.0.dds -o inGTX/font.0.gtx -swizzle 0
TexConv2.exe -i inDDS/font.1.dds -o inGTX/font.1.gtx -swizzle 2
TexConv2.exe -i inDDS/font.2.dds -o inGTX/font.2.gtx -swizzle 4
TexConv2.exe -i inDDS/font.3.dds -o inGTX/font.3.gtx -swizzle 6
TexConv2.exe -i inDDS/font.4.dds -o inGTX/font.4.gtx -swizzle 8
TexConv2.exe -i inDDS/font.5.dds -o inGTX/font.5.gtx -swizzle 10
TexConv2.exe -i inDDS/font.6.dds -o inGTX/font.6.gtx -swizzle 12
TexConv2.exe -i inDDS/font.7.dds -o inGTX/font.7.gtx -swizzle 14
TexConv2.exe -i inDDS/font.8.dds -o inGTX/font.8.gtx -swizzle 16
TexConv2.exe -i inDDS/font.9.dds -o inGTX/font.9.gtx -swizzle 18
pause
