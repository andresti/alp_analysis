#!/usr/bin/env python 
# to EXE: 
# once with trgIso
# once with trgIsoandJet plus update

# good old python modules
import json
import os
import importlib
from glob import glob

# ROOT imports
import ROOT
from ROOT import TChain, TH1F, TFile, vector, gROOT
# custom ROOT classes 
from ROOT import alp, ComposableSelector, CounterOperator, TriggerOperator, JetFilterOperator, BTagFilterOperator, JetPairingOperator, DiJetPlotterOperator
from ROOT import BaseOperator, EventWriterOperator, IsoMuFilterOperator, MetFilterOperator, JetPlotterOperator, FolderOperator, MiscellPlotterOperator
from ROOT import ThrustFinderOperator, HemisphereProducerOperator, HemisphereWriterOperator, DiHiggsFilterOperator

# imports from ../python 
from Analysis.alp_analysis.alpSamples  import samples
from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_analysis.triggerlists import triggerlists
from Analysis.alp_analysis.workingpoints import wps

TH1F.AddDirectory(0)

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--numEvts", help="number of events", type=int, default='-1')
parser.add_argument("-s", "--samList", help="sample list", default="")
parser.add_argument("--btag", help="which btag algo", default='cmva')
parser.add_argument("-i", "--iDir", help="input directory", default="def_cmva_mixed") 
parser.add_argument("-o", "--oDir", help="output directory", default="def_cmva_mixed")
parser.set_defaults()
args = parser.parse_args()

# exe parameters
numEvents  =  args.numEvts
if not args.samList: samList = ['test']  # list of samples to be processed - append multiple lists
else: samList = [args.samList]
trgList   = 'def_2016'
intLumi_fb = 35.9

iDir = "/lustre/cmswork/hh/alp_moriond_base/" + args.iDir
oDir = '/lustre/cmswork/hh/alp_moriond_base/' + args.oDir

data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])
if args.btag == 'cmva':  
    btagAlgo = "pfCombinedMVAV2BJetTags"
    btag_wp = wps['CMVAv2_moriond']
elif args.btag == 'csv': 
    btagAlgo  = "pfCombinedInclusiveSecondaryVertexV2BJetTags"
    btag_wp = wps['CSVv2_moriond']

if not os.path.exists(oDir): os.mkdir(oDir)
print oDir

# to convert weights 
weights_v = vector("string")()

# to parse variables to the anlyzer
config = {"jets_branch_name": "Jets",
          "dijets_branch_name": "DiJets",
          "dihiggs_branch_name": "DiHiggs",
          "muons_branch_name" : "Muons",
          "electrons_branch_name" : "Electrons",
          "met_branch_name" : "MET",
          "n_gen_events":0,
          "xsec_br" : 0,
          "matcheff": 0,
          "kfactor" : 0,
          "isData" : False,
          "isSignal" : False,
          "lumiFb" : intLumi_fb,
          "isMixed" : False,
          "ofile_update" : True, #True, #False,
          "evt_weight_name" : "evtWeight",
         }

snames = []
for s in samList:
    snames.extend(samlists[s])

# process samples
ns = 0
for sname in snames:
    #get file names in all sub-folders:
    reg_exp = iDir+"/"+sname+".root"
    print "reg_exp: {}".format(reg_exp) 
    files = glob(reg_exp)
    print "\n ### processing {}".format(sname)        
 
    #preliminary checks
    if not files: 
        print "WARNING: files do not exist"
        continue
    else:
        if "Run" in files[0]: config["isData"] = True
        if "GluGluToHH" in files[0] or "HHTo4B" in files[0]: config["isSignal"] = True

    #read weights from alpSamples 
    config["xsec_br"]  = samples[sname]["xsec_br"]
    config["matcheff"] = samples[sname]["matcheff"]
    config["kfactor"]  = samples[sname]["kfactor"]

    json_str = json.dumps(config)

    #define selectors list
    selector = ComposableSelector(alp.Event)(0, json_str)
    selector.addOperator(BaseOperator(alp.Event)())

#    selector.addOperator(FolderOperator(alp.Event)("trg_Iso"))
    selector.addOperator(FolderOperator(alp.Event)("trg_IsoAndJet"))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"], weights_v))
    selector.addOperator(JetPlotterOperator(alp.Event)(btagAlgo, weights_v))
    selector.addOperator(MiscellPlotterOperator(alp.Event)(weights_v))        
    selector.addOperator(EventWriterOperator(alp.Event)(json_str,weights_v))

    #create tChain and process each files
#    tchain = TChain("trg_Iso/tree")    
    tchain = TChain("trg_IsoAndJet/tree")    
    for File in files:                     
        tchain.Add(File)       
    nev = numEvents if (numEvents > 0 and numEvents < tchain.GetEntries()) else tchain.GetEntries()
    procOpt = "ofile=./"+sname+".root" if not oDir else "ofile="+oDir+"/"+sname+".root"
    print "max numEv {}".format(nev)
    tchain.Process(selector, procOpt, nev)
    ns+=1

print "### processed {} samples ###".format(ns)



