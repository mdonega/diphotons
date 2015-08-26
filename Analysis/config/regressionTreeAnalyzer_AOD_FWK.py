#!/usr/bin/env cmsRun

import FWCore.ParameterSet.Config as cms

import FWCore.ParameterSet.VarParsing as VarParsing
from flashgg.MetaData.samples_utils import SamplesManager

def addMiniTreeVar(miniTreeCfg,var,name=None):
    if not name:
        name = var.replace(".","_").replace("get","")
    miniTreeCfg.append( cms.untracked.PSet(var=cms.untracked.string(var),
                                           name=cms.untracked.string(name)),
                        )
        
def addMiniTreeVars(miniTreeCfg,lst):
    for var in lst:
        args = [var]
        if type(var) == list or type(var) == tuple:
            args = var
        addMiniTreeVar(miniTreeCfg,*args)
        

process = cms.Process("Analysis")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.source = cms.Source("PoolSource",
                            fileNames=cms.untracked.vstring(
        )
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1000 )

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("test.root")
)

process.regressionAnalyzer = cms.EDAnalyzer('PhotonIdAnalyzer',
  ## photons = cms.InputTag('gedPhotons'), ## input for the simple example above
  ## photons = cms.InputTag('slimmedPhotons'), ## input for the simple example above
  photons = cms.InputTag('flashggPhotons'), ## input for the simple example above
  packedGenParticles = cms.InputTag('genParticles'),
  lumiWeight = cms.double(1.),
  processId = cms.string(""),
  rho = cms.InputTag('fixedGridRhoAll'),
  miniTreeCfg = cms.untracked.VPSet(
        ),
  vertexes = cms.InputTag("offlinePrimaryVertices"),
  
  dumpRecHits = cms.untracked.bool(True),
  dumpAllRechisInfo = cms.untracked.bool(True),
  barrelRecHits = cms.InputTag('reducedEcalRecHitsEB'),
  endcapRecHits = cms.InputTag('reducedEcalRecHitsEE'),

  idleWatchdog = cms.PSet(checkEvery = cms.untracked.int32(1000),
                          minIdleFraction = cms.untracked.double(0.),
                          tolerance = cms.untracked.int32(5)
                          ),
  
  mvas = cms.VPSet(),
  mvaPreselection = cms.string("0"),
  minPt = cms.untracked.double(0),
  categories = cms.VPSet()

  ## dumpFakes = cms.untracked.bool(False),

  ## recomputeNoZsShapes = cms.untracked.bool(True),
)

addMiniTreeVars(process.regressionAnalyzer.miniTreeCfg,
                ["phi","eta","pt","energy",
                 
                 ("superCluster.eta","scEta"),("superCluster.eta","scPhy"),
                 ("superCluster.rawEnergy","scRawEnergy"),
                 ("superCluster.preshowerEnergy","scPreshowerEnergy"),
                 ("superCluster.clustersSize","scClustersSize"),
                 ("superCluster.seed.energy","scSeedEnergy"),
                 ("superCluster.energy","scEnergy"),
                 
                 ## ("? hasMatchedGenPhoton ? matchedGenPhoton.energy : 0","etrue"),
                 ("userFloat('etrue')","etrue"),

                 ("userFloat('genIso')","genIso"),
                 ("userFloat('frixIso')","frixIso"),
                 ("userInt('seedRecoFlag')","seedRecoFlag"),
                                  
                 "passElectronVeto","hasPixelSeed",
                 ## cluster shapes
                 "e1x5",           "full5x5_e1x5",           
                 "e2x5",           "full5x5_e2x5",           
                 "e3x3",           "full5x5_e3x3",           
                 "e5x5",           "full5x5_e5x5",           
                 "maxEnergyXtal",  "full5x5_maxEnergyXtal",  
                 "sigmaIetaIeta",  "full5x5_sigmaIetaIeta",  
                 "r1x5",           "full5x5_r1x5",           
                 "r2x5",           "full5x5_r2x5",           
                 "r9",             "full5x5_r9",             
                 "eMax","e2nd","eTop","eBottom","eLeft","eRight",
                 "iEta","iPhi","cryEta","cryPhi",
                                  
                 "hadTowOverEm",
                 ## more cluster shapes
                 ("e2x5right" ,"e2x5Right"  ),
                 ("e2x5left"  ,"e2x5Left"   ),
                 ("e2x5top"   ,"e2x5Top"    ),
                 ("e2x5bottom","e2x5Bottom" ),
                 ("e2x5max"   ,"e2x5Max"    ),
                 ("e1x3"      ,"e1x3"       ),
                 ("s4"        ,"s4"         ),
                 
                 ("esEffSigmaRR","sigmaRR"),
                 ("sqrt(spp)","sigmaIphiIphi"),
                 ("sep","covarianceIetaIphi"),
                 ("superCluster.etaWidth","etaWidth"),("superCluster.phiWidth","phiWidth"),
                 ]
                )

process.load("flashgg/MicroAOD/flashggMicroAODSequence_cff")

process.p = cms.Path((process.flashggVertexMapUnique+process.flashggVertexMapNonUnique+process.flashggMicroAODGenSequence)*process.flashggPhotons*process.regressionAnalyzer)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:miniAOD-prod_RECO.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('miniAOD-prod nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('miniAOD-prod_PAT.root'),
    outputCommands = process.MINIAODSIMEventContent.outputCommands,
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)

from flashgg.MicroAOD.flashggJets_cfi import addFlashggPFCHSLegJets 
# call the function, it takes care of everything else.
addFlashggPFCHSLegJets(process)


# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V7', '')

# Path and EndPath definitions
process.endjob_step = cms.EndPath(process.endOfProcess)
## process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)



#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)
process.load('Configuration.StandardSequences.PATMC_cff')

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC 

#call to customisation function miniAOD_customizeAllMC imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllMC(process)

process.reducedEgamma.keepPhotons = "1"
process.reducedEgamma.slimRelinkPhotons = "1"
process.reducedEgamma.relinkPhotons = "1"

# End of customisation functions

# customization for job splitting, lumi weighting, etc.
from diphotons.MetaData.JobConfig import customize
customize.setDefault("maxEvents",500)
customize(process)

# process.source.fileNames = ['/store/mc/RunIISpring15DR74/SinglePhoton_FlatPt-300To3000/GEN-SIM-RECO/AsymptFlat0to50bx25RawReco_MCRUN2_74_V9-v1/00000/0A5CBBA3-3113-E511-9E58-02163E01437C.root']
