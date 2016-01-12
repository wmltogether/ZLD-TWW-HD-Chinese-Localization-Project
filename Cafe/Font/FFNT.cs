using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace bffnt_tool
{
    public class FFNT
    {
        public FFNTHeader Header;
        public FINF FontInfo;
        public TGLP TextureGlyph;
        public CWDH[] CharWidths;
        public CMAP[] CharMaps;
        public FFNT(byte[] Data)
        {
            EndianBinaryReader er = new EndianBinaryReader(new MemoryStream(Data), Endianness.BigEndian);
            Header = new FFNTHeader(er);
            FontInfo = new FINF(er);
            er.BaseStream.Position = FontInfo.TGLPOffset - 8;
            TextureGlyph = new TGLP(er);

            List<CWDH> tmp = new List<CWDH>();
            er.BaseStream.Position = FontInfo.CWDHOffset - 8;
            CWDH Last;
            do
            {
                Last = new CWDH(er);
                tmp.Add(Last);
                if (Last.NextCWDHOffset != 0) er.BaseStream.Position = Last.NextCWDHOffset - 8;
            }
            while (Last.NextCWDHOffset != 0);
            CharWidths = tmp.ToArray();

            List<CMAP> tmp2 = new List<CMAP>();
            er.BaseStream.Position = FontInfo.CMAPOffset - 8;
            CMAP Last2;
            do
            {
                Last2 = new CMAP(er);
                tmp2.Add(Last2);
                if (Last2.NextCMAPOffset != 0) er.BaseStream.Position = Last2.NextCMAPOffset - 8;
            }
            while (Last2.NextCMAPOffset != 0);
            CharMaps = tmp2.ToArray();
            er.Close();
        }
        public class FFNTHeader
        {
            public String Signature;
            public UInt16 Endianness;
            public UInt16 HeaderSize;
            public UInt32 Version;
            public UInt32 FileSize; // BFFNT文件长度
            public UInt32 NrBlocks; //文件内数据块数量 FINF + TGLP + CWDH * N + CMAP * N
            public FFNTHeader(EndianBinaryReader er)
            {

                Signature = er.ReadString(Encoding.ASCII, 4);//FFNT
                Endianness = er.ReadUInt16();
                HeaderSize = er.ReadUInt16();
                Version = er.ReadUInt32();
                FileSize = er.ReadUInt32();
                NrBlocks = er.ReadUInt32();
            }

        }
        public class FINF
        {
            public String Signature; //FINF
            public UInt32 SectionSize; //块大小
            public Byte FontType;
            public Byte LineFeed;
            public Byte Width;
            public Byte Ascent;
            public Byte Padding;
            public Byte Height;
            public UInt16 AlterCharIndex;
            public CharWidthInfo DefaultWidth;
            public Byte Encoding;
            public UInt32 TGLPOffset;
            public UInt32 CWDHOffset; //第一个CWDH地址
            public UInt32 CMAPOffset; //第一个CMAP的起始地址

            public FINF(EndianBinaryReader er)
            {
                Signature = er.ReadString(System.Text.Encoding.ASCII, 4); //FINF
                SectionSize = er.ReadUInt32();
                FontType = er.ReadByte(); //01
                LineFeed = er.ReadByte(); //28
                Width = er.ReadByte();
                Ascent = er.ReadByte();
                Padding = er.ReadByte();
                Height = er.ReadByte();
                AlterCharIndex = er.ReadUInt16();
                DefaultWidth = new CharWidthInfo(er);
                Encoding = er.ReadByte();
                TGLPOffset = er.ReadUInt32();
                CWDHOffset = er.ReadUInt32();
                CMAPOffset = er.ReadUInt32();
                
                
            }

        }
        public class CharWidthInfo
        {
            public CharWidthInfo(EndianBinaryReader er)
            {
                Left = er.ReadSByte();
                GlyphWidth = er.ReadByte();
                CharWidth = er.ReadByte();
            }
            public SByte Left;
            public Byte GlyphWidth;
            public Byte CharWidth;
        }
        public class TGLP
        {
            public String Signature;
            public UInt32 SectionSize;
            public Byte CellWidth; //21
            public Byte CellHeight; //28
            public Byte FLIMNums;//纹理数量
            public Byte MaxCharWidth;//20
            public UInt32 FLIMSize; //每张纹理大小
            public UInt16 Ascent;
            public UInt16 FLIMFormat; //0c == DXGI_BC4
            public UInt16 SheetNrRows;
            public UInt16 SheetNrLines;
            public UInt16 FLIMWidth; //纹理宽度
            public UInt16 FLIMHeight; //纹理高度
            public UInt32 FLIMDataOffset; //纹理起始地址
            public Byte[][] FLIMSheets; //纹理是swizzle过的，swizzle参数为纹理编号 * 2 ，需要用TexConv2转换
            public TGLP(EndianBinaryReader er)
            {
                Signature = er.ReadString(Encoding.ASCII, 4);
                SectionSize = er.ReadUInt32();
                CellWidth = er.ReadByte();//实际为CellWidth += 1
                CellHeight = er.ReadByte();//实际为CellHeight += 1
                FLIMNums = er.ReadByte();//纹理数量
                MaxCharWidth = er.ReadByte();
                FLIMSize = er.ReadUInt32();//纹理大小
                Ascent = er.ReadUInt16();
                FLIMFormat = er.ReadByte();//纹理压缩格式
                SheetNrRows = er.ReadUInt16();//横向tile数 (FLIMWidth / (CellWidth))
                SheetNrLines = er.ReadUInt16();//纵向tile数(FLIMHeight / (CellHeight))
                FLIMWidth = er.ReadUInt16();//纹理宽度
                FLIMHeight = er.ReadUInt16();//纹理高度
                FLIMDataOffset = er.ReadUInt32();//纹理起始地址
                er.BaseStream.Position = FLIMDataOffset;
                FLIMSheets = new byte[FLIMNums][];
                for (int i = 0; i < FLIMNums; i++)
                {
                    FLIMSheets[i] = er.ReadBytes((int)FLIMSize);
                }
            }


        }

        public class CWDH
        {
            public String Signature;
            public UInt32 SectionSize;
            public UInt16 StartIndex;
            public UInt16 EndIndex;
            public UInt32 NextCWDHOffset;
            public CharWidthInfo[] CharWidths;
            public CWDH(EndianBinaryReader er)
            {
                Signature = er.ReadString(Encoding.ASCII, 4);
                SectionSize = er.ReadUInt32();
                StartIndex = er.ReadUInt16();
                EndIndex = er.ReadUInt16();
                NextCWDHOffset = er.ReadUInt32();
                CharWidths = new CharWidthInfo[EndIndex - StartIndex + 1];
                for (int i = 0; i < EndIndex - StartIndex + 1; i++)
                {
                    CharWidths[i] = new CharWidthInfo(er); // 3字节， LEFT,GLYPH WIDTH,CHAR WIDTH
                }
            }
        }
        public class CMAP
        {
            public String Signature;
            public UInt32 SectionSize;
            public UInt16 CodeBegin;
            public UInt16 CodeEnd;
            public CMAPMappingMethod MappingMethod; // 2字节
            public UInt16 Reserved;// 00
            public UInt32 NextCMAPOffset;

            //Direct
            public UInt16 IndexOffset;

            //Table
            public UInt16[] IndexTable;

            //Scan
            public UInt16 NrScanEntries;
            public Dictionary<UInt16, UInt16> ScanEntries;

            public enum CMAPMappingMethod : ushort
            {
                Direct = 0,
                Table = 1,
                Scan = 2
            }
            public CMAP(EndianBinaryReader er)
            {
                Signature = er.ReadString(Encoding.ASCII, 4);
                SectionSize = er.ReadUInt32();
                CodeBegin = er.ReadUInt16();
                CodeEnd = er.ReadUInt16();
                MappingMethod = (CMAPMappingMethod)er.ReadUInt16();
                Reserved = er.ReadUInt16();
                NextCMAPOffset = er.ReadUInt32();

                switch (MappingMethod)
                {
                    case CMAPMappingMethod.Direct:
                        IndexOffset = er.ReadUInt16();
                        break;
                    case CMAPMappingMethod.Table:
                        IndexTable = er.ReadUInt16s(CodeEnd - CodeBegin + 1);
                        break;
                    case CMAPMappingMethod.Scan:
                        ScanEntries = new Dictionary<ushort, ushort>();
                        NrScanEntries = er.ReadUInt16();
                        for (int i = 0; i < NrScanEntries; i++) ScanEntries.Add(er.ReadUInt16(), er.ReadUInt16());
                        break;
                }
            }
            public UInt16 GetIndexFromCode(UInt16 Code)
            {
                if (Code < CodeBegin || Code > CodeEnd) return 0xFFFF;
                switch (MappingMethod)
                {
                    case CMAPMappingMethod.Direct:
                        return (UInt16)(Code - CodeBegin + IndexOffset); 
                    case CMAPMappingMethod.Table:
                        return IndexTable[Code - CodeBegin];
                    case CMAPMappingMethod.Scan:
                        if (!ScanEntries.ContainsKey(Code)) return 0xFFFF;
                        return ScanEntries[Code];
                }
                return 0xFFFF;
            }

        }
        public UInt16 GetIndexFromCode(UInt16 Code)
        {
            foreach (var v in CharMaps)
            {
                UInt16 result = v.GetIndexFromCode(Code);
                if (result != 0xFFFF) return result;
            }
            return 0xFFFF;
        }
        /*
         对unicode值 遍历所有的charmaps表
         当charmap.method = Direct:
         index_value = Code - charmap.CodeBegin + charmaps.IndexOffset
         当method = Table；
         * index_value = Table[Code - charmap.CodeBegin]
         当method = Scan:
         * index_value = ScanEntries[Code]
         */
    }
    
    
}
