import FWCore.ParameterSet.Config as cms

process = cms.Process('jetToolbox')

process.load('PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')

## ----------------- test GT and outName ------------------
testGT = "92X_dataRun2_HLT_v7"
testOutName = "dijetNtuple.root"

## ----------------- Global Tag ------------------
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = "THISGLOBALTAG"

#--------------------- Report and output ---------------------------

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.TFileService=cms.Service("TFileService",
                                 fileName=cms.string("THISROOTFILE"),
                                 closeFileFast = cms.untracked.bool(True)
                                 )

process.options = cms.untracked.PSet(
        allowUnscheduled = cms.untracked.bool(True),
        wantSummary = cms.untracked.bool(False),
)


## ---------------- Interactive testing-----------------
import FWCore.ParameterSet.VarParsing as VarParsing
variables = VarParsing.VarParsing('analysis')
variables.register('local',
                   False,
                   VarParsing.VarParsing.multiplicity.singleton,
                   VarParsing.VarParsing.varType.bool,
                   "Local running")

variables.parseArguments()

if variables.local == True:
    process.GlobalTag.globaltag = testGT
    process.TFileService.fileName = cms.string(testOutName)


##-------------------- Define the source  ----------------------------

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/data/Run2017F/ScoutingCaloHT/RAW/v1/000/305/040/00000/48B963FD-53B0-E711-8CFD-02163E019CA4.root' # 2017F data
    )
)

##------------------- l1 stage2 digis ------------------------------
process.load("EventFilter.L1TRawToDigi.gtStage2Digis_cfi")
process.gtStage2Digis.InputLabel = cms.InputTag( "hltFEDSelectorL1" )

##-------------------- User analyzer  --------------------------------
#import trigger conf
from CMSDIJET.DijetScoutingRootTreeMaker.TriggerPaths_cfi import getHLTConf, getL1Conf

process.dijetscouting = cms.EDAnalyzer(
    'DijetCaloScoutingTreeProducer',
    ## JETS/MET ########################################
    jetsAK4    = cms.InputTag('hltScoutingCaloPacker'),
    ptMinAK4   = cms.double(10),
    rho        = cms.InputTag('hltScoutingCaloPacker:rho'),
    met        = cms.InputTag('hltScoutingCaloPacker:caloMetPt'),
    vtx        = cms.InputTag('hltScoutingPrimaryVertexPackerCaloMuon','primaryVtx','HLT'),
    # ParkingScoutingMonitor
    doRECO     = cms.bool(False),

    ## trigger ###################################
    triggerAlias = cms.vstring(getHLTConf(0)),
    triggerSelection = cms.vstring(getHLTConf(1)),
    triggerDuplicates = cms.vint32(getHLTConf(2)),

    triggerConfiguration = cms.PSet(
        hltResults            = cms.InputTag('TriggerResults','','HLT'),
        l1tResults            = cms.InputTag(''),
        daqPartitions         = cms.uint32(1),
#        l1tIgnoreMask         = cms.bool(False), # obsolete
#        l1techIgnorePrescales = cms.bool(False), # obsolete
        l1tIgnoreMaskAndPrescale = cms.bool(False),
        throw                 = cms.bool(False)
    ),

    ## JECs ################
    doJECs = cms.bool(True),

    L1corrAK4_DATA = cms.FileInPath('CMSDIJET/DijetScoutingRootTreeMaker/data/80X_dataRun2_HLT_v12/80X_dataRun2_HLT_v12_L1FastJet_AK4CaloHLT.txt'),
    L2corrAK4_DATA = cms.FileInPath('CMSDIJET/DijetScoutingRootTreeMaker/data/80X_dataRun2_HLT_v12/80X_dataRun2_HLT_v12_L2Relative_AK4CaloHLT.txt'),
    L3corrAK4_DATA = cms.FileInPath('CMSDIJET/DijetScoutingRootTreeMaker/data/80X_dataRun2_HLT_v12/80X_dataRun2_HLT_v12_L3Absolute_AK4CaloHLT.txt'),

                                                                                              
    #L1 trigger info
    doL1 = cms.bool(True),
    AlgInputTag = cms.InputTag("gtStage2Digis"),
    l1tAlgBlkInputTag = cms.InputTag("gtStage2Digis"),
    l1tExtBlkInputTag = cms.InputTag("gtStage2Digis"),
    ReadPrescalesFromFile = cms.bool(False),
    l1Seeds = cms.vstring(getL1Conf())
)


# ------------------ path --------------------------
process.p = cms.Path(process.dijetscouting)
