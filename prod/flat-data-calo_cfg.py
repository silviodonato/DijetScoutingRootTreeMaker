import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process('jetToolbox',eras.Run2_25ns)

process.load('PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')

## ----------------- Global Tag ------------------
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = "80X_dataRun2_HLT_v12"
#process.GlobalTag.globaltag = THISGLOBALTAG


#--------------------- Report and output ---------------------------

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.TFileService=cms.Service("TFileService",
                                 fileName=cms.string("dijetNtuple.root"),
                                 closeFileFast = cms.untracked.bool(True)
                                 )

process.options = cms.untracked.PSet(
        allowUnscheduled = cms.untracked.bool(True),
        wantSummary = cms.untracked.bool(False),
)


##-------------------- Define the source  ----------------------------

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/user/duanders/ScoutingCaloHT_Run272798.root'
    )
)

##--- l1 stage2 digis ---
process.load("EventFilter.L1TRawToDigi.gtStage2Digis_cfi")
process.gtStage2Digis.InputLabel = cms.InputTag( "hltFEDSelectorL1" )

##-------------------- User analyzer  --------------------------------

process.dijetscouting = cms.EDAnalyzer(
    'DijetCaloScoutingTreeProducer',
    ## JETS/MET ########################################
    jetsAK4    = cms.InputTag('hltScoutingCaloPacker'),
    ptMinAK4   = cms.double(10),
    rho        = cms.InputTag('hltScoutingCaloPacker:rho'),
    met        = cms.InputTag('hltScoutingCaloPacker:caloMetPt'),
    vtx        = cms.InputTag('hltScoutingCaloPacker'),
    # ParkingScoutingMonitor
    doRECO     = cms.bool(False),

    ## trigger ###################################
    triggerAlias = cms.vstring(
        # Scouting
        'CaloJet40_CaloScouting_PFScouting', 
        'L1HTT_CaloScouting_PFScouting', 
        'CaloScoutingHT250', 
        # RECO 
        'PFHT800', 
        'PFHT650', 
        'PFHT600',
        'PFHT475',
        'PFHT400',
        'PFHT350',
        'PFHT300',
        'PFHT250',
        'PFHT200',
        'PFHT650MJJ950',
        'PFHT650MJJ900',
        'PFJET500',
        'PFJET450',
        'PFJET200',
        'HT2000',
        'HT2500',
        'Mu45Eta2p1',
        'AK8PFHT700TriMass50',
        'AK8PFJet360TrimMass50',
        'CaloJet500NoJetID',
        'DiPFJetAve300HFJEC',
        'DiPFJetAve500',
        'PFHT750FourJetPt50',
        'QuadPFJetVBF'
    ),
    triggerSelection = cms.vstring(
        # Scouting
        'DST_CaloJet40_CaloScouting_PFScouting_v*',
        'DST_L1HTT_CaloScouting_PFScouting_v*',
        'DST_HT250_CaloScouting_v*',
        # RECO
        'HLT_PFHT800_v*',
        'HLT_PFHT650_v*',
        'HLT_PFHT600_v*',
        'HLT_PFHT475_v*',
        'HLT_PFHT400_v*',
        'HLT_PFHT350_v*',
        'HLT_PFHT300_v*',
        'HLT_PFHT250_v*',
        'HLT_PFHT200_v*',
        'HLT_PFHT650_WideJetMJJ950DEtaJJ1p5_v*',
        'HLT_PFHT650_WideJetMJJ900DEtaJJ1p5_v*',
        'HLT_PFJet500_v*',
        'HLT_PFJet450_v*',
        'HLT_PFJet200_v*',
        'HLT_HT2000_v*',
        'HLT_HT2500_v*',
        'HLT_Mu45_eta2p1_v*',
        'HLT_AK8PFHT700_TrimR0p1PT0p03Mass50_v*',
        'HLT_AK8PFJet360_TrimMass30_v*',
        'HLT_CaloJet500_NoJetID_v*',
        'HLT_DiPFJetAve300_HFJEC_v*',
        'HLT_DiPFJetAve500_v*',
        'HLT_PFHT750_4JetPt50_v*',
        'HLT_QuadPFJet_VBF_v*'
    ),
    triggerDuplicates = cms.vint32(
        ## If >0, trigger result will be ORed with result from the previous
        ## trigger rather than being push_backed
        # Scouting
        0, # CaloJet40_CaloScouting_PFScouting
        0, # L1HTT_CaloScouting_PFScouting
        0, # CaloScoutingHT250
        # RECO
        0, # PFHT800
        0, # PFHT650
        0, # PFHT600
        0, # PFHT475
        0, # PFHT400
        0, # PFHT350
        0, # PFHT300
        0, # PFHT250
        0, # PFHT200
        0, # PFHT650MJJ950
        0, # PFHT650MJJ900
        0, # PFJET500
        0, # PFJET450
        0, # PFJET200
        0, # HT2000
        0, # HT2500
        0, # Mu45Eta2p1
        0, # AK8PFHT700TriMass50
        0, # AK8PFJet360TrimMass50
        0, # CaloJet500NoJetID
        0, # DiPFJetAve300HFJEC
        0, # DiPFJetAve500
        0, # PFHT750FourJetPt50
        0  # QuadPFJetVBF'
    ),
    triggerConfiguration = cms.PSet(
        hltResults            = cms.InputTag('TriggerResults','','HLT'),
        l1tResults            = cms.InputTag(''),
        daqPartitions         = cms.uint32(1),
        l1tIgnoreMask         = cms.bool(False),
        l1techIgnorePrescales = cms.bool(False),
        throw                 = cms.bool(False)
    ),

    ## JECs ################
    doJECs = cms.bool(True),

    L1corrAK4_DATA = cms.FileInPath('CMSDIJET/DijetScoutingRootTreeMaker/data/74X_dataRun2_HLT_v1/74X_dataRun2_HLT_v1_L1FastJet_AK4PFHLT.txt'),
    L2corrAK4_DATA = cms.FileInPath('CMSDIJET/DijetScoutingRootTreeMaker/data/74X_dataRun2_HLT_v1/74X_dataRun2_HLT_v1_L2Relative_AK4PFHLT.txt'),
    L3corrAK4_DATA = cms.FileInPath('CMSDIJET/DijetScoutingRootTreeMaker/data/74X_dataRun2_HLT_v1/74X_dataRun2_HLT_v1_L3Absolute_AK4PFHLT.txt'),

    #L1 trigger info
    doL1 = cms.bool(True),
    AlgInputTag = cms.InputTag("gtStage2Digis"),

    l1Seeds = cms.vstring("L1_HTT120","L1_HTT170","L1_HTT200")
)


# ------------------ path --------------------------
process.p = cms.Path(process.dijetscouting)
