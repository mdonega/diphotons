#include "FWCore/Framework/interface/MakerMacros.h"
#include "PhysicsTools/UtilAlgos/interface/EDAnalyzerWrapper.h"
#include "diphotons/FWLiteAlgos/interface/PhotonIdAnalyzer.h"

typedef edm::AnalyzerWrapper<diphotons::PhotonIdAnalyzer> PhotonIdAnalyzer;
DEFINE_FWK_MODULE( PhotonIdAnalyzer );

