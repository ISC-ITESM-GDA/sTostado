import os
import PyPDF2
import sys
import random


OutPut2 = open("OutPut2.txt", "w")
Values2 = open("Values2.txt", 'w')

w = ""  # """Necessary parameter to run the code. This variable has to be assigned to the specific route of the directory where the thermal profiles are."""

y = "" # """Necessary parameter to run the code. This variable has to be assigned to the specific route of the directory where our code will be located."""
os.chdir(w)
directory = os.listdir(w)
ruta = str(w)

UserVariableElection = "" #"""Necessary parameter to run the code. The user has to choose which variable wants to analyze, either Time Above Liquids or Peak Temperature"""

FilesDef = []
nums = []


def ordenar(dirw):
    FilesName = []
    cont = 0
    for i in dirw:
        y = os.path.getctime(i)
        nums.append(y)
        FilesName.append(dirw[cont])
        cont += 1
    while len(nums) > 0:
        for i in nums:
            if i == max(nums):
                FilesDef.append(FilesName[nums.index(i)])
                FilesName.remove(FilesName[nums.index(i)])
                nums.remove(i)  # Se ordenan por fecha de cracion


ordenar(directory)
print(FilesDef)
os.chdir(y)

Warning1 = ""  #"""If the user insert a bigger number than the quantity of the files that are in the directory this warning has to be shown."""


def documents(Directory):
    num = int()  # """Necessary parameter to run the code. This variable has to be assigned to the number of thermal profiles that the user wans to analyze."""
    if num == len(FilesDef):
        return FilesDef
    elif num < len(FilesDef):
        PDF = FilesDef[len(FilesDef):(len(FilesDef) - num - 1): - 1]
        return PDF
    else:
        Warning1 = "Aqui solo existen {0} archivos".format(len(FilesDef))
        sys.exit()   #"""The program will end if the user insert a bigger number than the files quantity on the directory."""


for x in documents(FilesDef):
    pdfNewFile = open(ruta + "/" + x, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfNewFile)
    pageObj2 = pdfReader.getPage(1)
    pageObj = pdfReader.getPage(0)
    text = pageObj.extractText()
    text2 = pageObj2.extractText()
    numToWork = text2.find("#")
    toWork = text2[numToWork:]
    index_PositiveSlope = toWork.index("PositiveSlope")
    index_PositiveSlopeTime = toWork.index("PositiveSlope Time")
    index_TimeAboveLiquids = toWork.index("Time AboveLiquidus")
    index_PeakTemperature = toWork.index("PeakTemperature")
    index_Variable = 0
    index_Lower = text.index("Lower")
    if "Time AbovePeak" in toWork:
        index_Variable = toWork.index("Time AbovePeak")
    else:
        index_Variable = toWork.index("Delta T")

    def ValuesPositiveSlope():
        PositiveSlopeData = ""
        PositiveSlope = toWork[index_PositiveSlope:index_PositiveSlopeTime]
        for i in PositiveSlope:
            if i in "0123456789.":
                PositiveSlopeData += i
            elif i in "*":
                warning = OutPut2.write("0")
                Values2.write("0")
                return warning
        while len(PositiveSlopeData) > 0:
            point = PositiveSlopeData.index(".")
            end = point + 3
            firstPart = PositiveSlopeData[0:point]
            secondPart = PositiveSlopeData[point:end]
            term = firstPart + secondPart
            Values2.write(term)
            Values2.write(" ")
            PositiveSlopeData = PositiveSlopeData[end:]
        OutPut2.write("1")
        return True

    def ValuesTimeAboveLiquids():
        TimeAboveLiquidsData = ""
        TimeAboveLiquids = toWork[index_TimeAboveLiquids:index_PeakTemperature]
        while ")" in TimeAboveLiquids:
            x = TimeAboveLiquids.index(")")
            TimeAboveLiquids = TimeAboveLiquids[x + 1:]
        for i in TimeAboveLiquids:
            if i in "0123456789.":
                TimeAboveLiquidsData += i
            elif i in "*":
                warning = OutPut2.write("0")
                Values2.write("0")
                return warning
        while len(TimeAboveLiquidsData) > 0:
            point = TimeAboveLiquidsData.index(".")
            end = point + 3
            firstPart = TimeAboveLiquidsData[0:point]
            secondPart = TimeAboveLiquidsData[point:end]
            term = firstPart + secondPart
            Values2.write(term)
            Values2.write(" ")
            TimeAboveLiquidsData = TimeAboveLiquidsData[end:]
        OutPut2.write("1")
        return True

    def ValuesPeakTemperature():
        PeakTemperatureData = ""
        PeakTemperature = toWork[index_PeakTemperature:index_Variable]
        for i in PeakTemperature:
            if i in "0123456789.":
                PeakTemperatureData += i
            elif i in "*":
                warning = OutPut2.write("0")
                Values2.write("0")
                return warning
        while len(PeakTemperatureData) > 0:
            point = PeakTemperatureData.index(".")
            end = point + 2
            firstPart = PeakTemperatureData[0:point]
            secondPart = PeakTemperatureData[point:end]
            term = firstPart + secondPart
            Values2.write(term)
            Values2.write(" ")
            PeakTemperatureData = PeakTemperatureData[end:]
        OutPut2.write("1")
        return True

    def OvenTemperatureData():
        GeneralData = text[index_Lower:]
        TemperatureData = GeneralData.split(" ")
        GeneralData2 = ""
        if "Zona" in GeneralData:
            for i in GeneralData:
                if i == " ":
                    GeneralData2 += ""
                else:
                    GeneralData2 += i
            index_p = GeneralData.index(":")
            GeneralData2 = GeneralData2[index_p:]
            GeneralData2 = GeneralData2.split(".")
            for i in range(10):
                for j in range(2):
                    GeneralData2.remove(GeneralData2[0])
                Values2.write(GeneralData2[0])
                Values2.write(" ")
                GeneralData2.remove(GeneralData2[0])
            return True
        else:
            TemperatureData = TemperatureData[2]
            TemperatureData = TemperatureData[TemperatureData.index("H"):]
            TemperatureData = TemperatureData.split(".")
            for i in range(10):
                for j in range(2):
                    TemperatureData.remove(TemperatureData[0])
                Values2.write(TemperatureData[0])
                Values2.write(" ")
                TemperatureData.remove(TemperatureData[0])
            return True

    ValuesPositiveSlope()
    Values2.write("\n")
    ValuesTimeAboveLiquids()
    Values2.write("\n")
    ValuesPeakTemperature()
    Values2.write("\n")
    OvenTemperatureData()
    Values2.write("\n")
    Values2.write("\n")


OutPut2.close()
Values2.close()
pdfNewFile.close()

Values_list = list()  # Matrix
TimeAboveLiquidsMatrix = list()  # Matrix
PeakTemperatureMatrix = list()  # Matrix


def FileReadingAndFilter():
    File = None
    try:
        File = open("Values2.txt")
    except ValueError:
        print("The file cannot be opened")
    if File:
        for line in File:
            TimeAboveLiquidsTerms = line.split(" ")
            for i in TimeAboveLiquidsTerms:
                if i == "\n":
                    TimeAboveLiquidsTerms.remove(i)
            Values_list.append(TimeAboveLiquidsTerms)
        cont = 0
        for i in Values_list:
            newList = Values_list[cont]
            if len(newList) == 0:
                Values_list.remove(i)
            cont += 1
        while len(Values_list) > 0:
            Values_list.remove(Values_list[0])
            TimeAboveLiquidsMatrix.append(Values_list[0])
            Values_list.remove(Values_list[0])
            PeakTemperatureMatrix.append(Values_list[0])
            Values_list.remove(Values_list[0])
            Values_list.remove(Values_list[0])


FileReadingAndFilter()

TimeAboveLiquidsMatrixDef = []


def SampleSizeCorrectionTAL(variable):
    lengths = []
    for i in variable:
        lengths.append(len(i))
    for x in range(1, len(lengths)):
        if lengths[0] != lengths[1]:
            lengths.remove(lengths[0])
    common = lengths[0]
    for i in variable:
        if len(i) == common:
            TimeAboveLiquidsMatrixDef.append(i)
        elif len(i) - common > 0:
            num = len(i) - common
            for x in range(num):
                rand = random.randint(0, len(i) - 1)
                i.remove(i[rand])
                if len(i) == common:
                    TimeAboveLiquidsMatrixDef.append(i)


SampleSizeCorrectionTAL(TimeAboveLiquidsMatrix)
PeakTemperatureMatrixDef = []


def SampleSizeCorrectionPT(variable):
    lengths = []
    for i in variable:
        lengths.append(len(i))
    for x in range(1, len(lengths)):
        if lengths[0] != lengths[1]:
            lengths.remove(lengths[0])
    common = lengths[0]
    for i in variable:
        if len(i) == common:
            PeakTemperatureMatrixDef.append(i)
        elif len(i) - common > 0:
            num = len(i) - common
            for x in range(num):
                rand = random.randint(0, len(i) - 1)
                i.remove(i[rand])
                if len(i) == common:
                    PeakTemperatureMatrixDef.append(i)


SampleSizeCorrectionPT(PeakTemperatureMatrix)
SampleSizePT = len(PeakTemperatureMatrixDef[0])
SampleSizeTAL = len(TimeAboveLiquidsMatrixDef[0])

Warning2 = ""  # """If there was an error generating the thermal profiles data this warning has to be shown to the user."""

DocMessage = open("OutPut2.txt", 'r')
message = DocMessage.read()
conclutions = message[0:]
cont = 0
cont1 = 0
while cont < len(conclutions):
    if conclutions[cont] == "0":
        cont1 += 0
    elif conclutions[cont] == "1":
        cont1 += 1
    cont += 1
if cont1 == len(conclutions):
    SolderPaste1 = "Indium 8.9E Lead free"
    SolderPaste2 = "Indium 5.8LS Lead free"
    SolderPaste3 = "Senju M40-LS720V-Hf"
    SolderPaste4 = "Alpha OM 338 PT"
    SolderPaste5 = "Indium SMQ98H (Sn63Pb37)"
    MinTAL = 0  # MinimumTimeAboveLiquids
    MaxTAL = 0  # MaximumTimeAboveLiquids
    MinPT = 0  # MinimumPeakTemperature
    MaxPT = 0  # MaximumPeakTemperature

    UserElection = ""  # """Necessary parametr to run the code. This variable has to be assigned to the solder paste election of the user"""

    while True:
        if UserElection == SolderPaste1 or UserElection == SolderPaste2:
            MinTAL = 30.00
            MaxTAL = 100.00
            MinPT = 230.00
            MaxPT = 262.00
            break
        elif UserElection == SolderPaste3:
            MinTAL = 30.00
            MaxTAL = 90.00
            MinPT = 232.00
            MaxPT = 255.00
            break
        elif UserElection == SolderPaste4:
            MinTAL = 30.00
            MaxTAL = 90.00
            MinPT = 230.00
            MaxPT = 250.00
            break
        elif UserElection == SolderPaste5:
            MinTAL = 30.00
            MaxTAL = 90.00
            MinPT = 204.00
            MaxPT = 224.00
            break

    d2 = float()
    D3 = float()
    D4 = float()
    A2 = float()
    while True:
        if SampleSizeTAL == 4 or SampleSizePT == 4:
            D3 = 0
            D4 = 2.282
            A2 = 0.729
            d2 = 2.059
            break
        elif SampleSizeTAL == 5 or SampleSizePT == 5:
            D3 = 0
            D4 = 2.114
            A2 = 0.577
            d2 = 2.326
            break
        elif SampleSizeTAL == 6 or SampleSizePT == 6:
            D3 = 0
            D4 = 2.004
            A2 = 0.483
            d2 = 2.534
            break
        elif SampleSizeTAL == 7 or SampleSizePT == 7:
            D3 = 0.076
            D4 = 1.924
            A2 = 0.419
            d2 = 2.704
            break
        elif SampleSizeTAL == 8 or SampleSizePT == 8:
            D3 = 0.136
            D4 = 1.864
            A2 = 0.373
            d2 = 2.847
            break
        elif SampleSizeTAL == 9 or SampleSizePT == 9:
            D3 = 0.184
            D4 = 1.816
            A2 = 0.337
            d2 = 2.97
            break
        elif SampleSizeTAL == 10 or SampleSizePT == 10:
            D3 = 0.223
            D4 = 1.777
            A2 = 0.308
            d2 = 3.078
            break
        else:
            Warning3 = "Too few or too many data for SampleSize"

    def TimeAboveLiquidsCalculation(d2, D3, D4, A2):
        LSL_TAL = MinTAL
        USL_TAL = MaxTAL
        XBarW_TAL = list()
        cont = 0
        for i in TimeAboveLiquidsMatrixDef:
            Profile = TimeAboveLiquidsMatrixDef[cont]
            ProfileResult = 0
            for j in Profile:
                j = float(j)
                ProfileResult += j
            ProfileResult = ProfileResult / len(Profile)
            XBarW_TAL.append(ProfileResult)
            cont += 1
        print(XBarW_TAL)
        RBar_TAL = float()  # Promedio de todas las R.
        cont1 = 0
        RW_TAL = list()
        for i in TimeAboveLiquidsMatrixDef:
            Profile = TimeAboveLiquidsMatrixDef[cont1]
            Range = (float(max(Profile)) - float(min(Profile)))
            RW_TAL.append(Range)
            cont1 += 1
        for i in RW_TAL:
            i = float(i)
            RBar_TAL += i
        print(RW_TAL)
        RealLenght = len(TimeAboveLiquidsMatrixDef)
        RBar_TAL = (RBar_TAL / RealLenght)
        XBarBar_TAL = float()  # Promedio de todas las XBar.
        for i in XBarW_TAL:
            i = float(i)
            XBarBar_TAL += i
        XBarBar_TAL = (XBarBar_TAL / RealLenght)
        SigmaHat_TAL = (RBar_TAL / d2)
        LCLR_TAL = D3 * RBar_TAL
        Cp_TAL = float()
        Cpk_TAL = float()
        Cp_TAL = (USL_TAL - LSL_TAL) / (6 * SigmaHat_TAL)
        CPW = []
        Cpu_TAL = (USL_TAL - XBarBar_TAL) / (3 * SigmaHat_TAL)
        Cpl_TAL = (XBarBar_TAL - LSL_TAL) / (3 * SigmaHat_TAL)
        CPW.append(Cpu_TAL)
        CPW.append(Cpl_TAL)
        Cpk_TAL = min(CPW)
        UCLR_TAL = D4 * RBar_TAL
        CLR_TAL = RBar_TAL
        UCLXBar_TAL = (A2 * RBar_TAL) + XBarBar_TAL
        CLXBar_TAL = XBarBar_TAL
        LCLXBar_TAL = XBarBar_TAL - (A2 * RBar_TAL)
        return Cpk_TAL, Cpu_TAL, LCLR_TAL, Cp_TAL, UCLR_TAL, CLR_TAL, UCLXBar_TAL, CLXBar_TAL, LCLXBar_TAL, SigmaHat_TAL, RBar_TAL, XBarBar_TAL

    def PeakTemperatureCalculation(d2, D3, D4, A2):
        XBarW_PT = list()
        LSL_PT = MinPT
        USL_PT = MaxPT
        cont = 0
        for i in PeakTemperatureMatrixDef:
            Profile = PeakTemperatureMatrixDef[cont]
            ProfileResult = 0
            for j in Profile:
                j = float(j)
                ProfileResult += j
            ProfileResult = ProfileResult / len(Profile)
            XBarW_PT.append(ProfileResult)
            cont += 1
        RW_PT = []
        cont1 = 0
        for i in PeakTemperatureMatrixDef:
            Profile = PeakTemperatureMatrixDef[cont1]
            Range = (float(max(Profile)) - float(min(Profile)))
            RW_PT.append(Range)
            cont1 += 1
        RBar_PT = 0
        for i in RW_PT:
            i = float(i)
            RBar_PT += i
        RBar_PT = (RBar_PT / len(PeakTemperatureMatrixDef))
        XBarBar_PT = 0
        for i in XBarW_PT:
            i = float(i)
            XBarBar_PT += i
        XBarBar_PT = (XBarBar_PT / len(PeakTemperatureMatrixDef))
        SigmaHat_PT = (RBar_PT / d2)
        LCLR_PT = D3 * RBar_PT
        Cp_PT = (USL_PT - LSL_PT) / (6 * SigmaHat_PT)
        Cpu_PT = (USL_PT - XBarBar_PT) / (3 * SigmaHat_PT)
        Cpl_PT = (XBarBar_PT - LSL_PT) / (3 * SigmaHat_PT)
        Cpk_PT = float()  # El valor mas pequeño entre Cpl y Cpu
        if Cpl_PT < Cpu_PT:
            Cpk_PT = Cpl_PT
        elif Cpl_PT > Cpu_PT:
            Cpk_PT = Cpu_PT
        UCLR_PT = D4 * RBar_PT
        CLR_PT = RBar_PT
        UCLXBar_PT = (A2 * RBar_PT) + XBarBar_PT
        CLXBar_PT = XBarBar_PT
        LCLXBar_PT = XBarBar_PT - (A2 * RBar_PT)
        return Cpk_PT, LCLR_PT, Cp_PT, UCLR_PT, CLR_PT, UCLXBar_PT, CLXBar_PT, LCLXBar_PT, SigmaHat_PT, RBar_PT, XBarBar_PT
    Warning3 = ""  # """If the number os samplesize is not in the range 4-10
    # we have to show this warning to the user."""

    if UserVariableElection == "Time Above Liquidus":
        TimeAboveLiquidsCalculation(d2, D3, D4, A2)
        # """We have to show all this data to the user on the user nterface."""
    elif UserVariableElection == "Peak Temperature":
        PeakTemperatureCalculation(d2, D3, D4, A2)
        # """We have to show all this data to the user on the user nterface."""
else:
    Warning2 = "Impossible to calculate. Try to generate the data again."
    # """If there is an error on one data of one thermal profile this warning has to be shown."""
