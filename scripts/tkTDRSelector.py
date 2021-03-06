#!/usr/bin/env python 
# to EXE: python scripts/BaselineSelector.py -s data_moriond -t -o def_cmva

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
from ROOT import ThrustFinderOperator, HemisphereProducerOperator, HemisphereWriterOperator, JEShifterOperator, JERShifterOperator, WeightSumOperator, MCTruthOperator, GenJetPlotterOperator

# imports from ../python 
from Analysis.alp_analysis.triggerlists import triggerlists
from Analysis.alp_analysis.workingpoints import wps

TH1F.AddDirectory(0)

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--numEvts", help="number of events", type=int, default='-1')
parser.add_argument("-s", "--samList", help="sample list", default="SM")
parser.add_argument("--pu", help="pileup scenario", default="")
parser.add_argument("--pt", help="jets pt cut",  type=float, default='30.')
parser.add_argument("--eta", help="jets eta cut",  type=float, default='2.4')

parser.add_argument("-t", "--doTrigger", help="apply trigger filter", action='store_true')
parser.add_argument("--jetCorr", help="apply [0=jesUp, 1=jesDown, 2=jerUp, 3=jerDown]", type=int, default='-1')
parser.add_argument("--btag", help="which btag algo", default='cmva')
parser.add_argument("-i", "--iDir", help="input directory", default="tkTDR") 
parser.add_argument("-o", "--oDir", help="output directory", default="tkTDR")
parser.add_argument("-m", "--doMixed", help="to process mixed samples", action='store_true') 
parser.add_argument("-f", "--no_savePlots", help="to save histos already in output file", action='store_false', dest='savePlots', ) #to get faster execution
# NOTICE: do not use trigger, jesUp, jesDown with '-m'
parser.set_defaults(doTrigger=False, doMixed=False, savePlots=True)
args = parser.parse_args()

# exe parameters
numEvents  =  args.numEvts
trgList   = 'def_2016'
intLumi_fb = 1.
pu = args.pu

iDir = "/lustre/cmswork/hh/" + args.iDir
oDir = '/lustre/cmswork/hh/' + args.oDir
if args.jetCorr   == 0: oDir += "_JESup"
elif args.jetCorr == 1: oDir += "_JESdown"
elif args.jetCorr == 2: oDir += "_JERup"
elif args.jetCorr == 3: oDir += "_JERdown"

data_path = "{}/src/Analysis/alp_analysis/data/".format(os.environ["CMSSW_BASE"])
if args.btag == 'cmva':  
    btagAlgo = "pfCombinedMVAV2BJetTags"
    btag_wp = wps['CMVAv2_moriond']
elif args.btag == 'csv': 
    btagAlgo  = "pfCombinedInclusiveSecondaryVertexV2BJetTags"
    btag_wp = wps['CSVv2_moriond']

#weights to be applied 
weights        = {}
weights_nobTag = {} 
if not args.doMixed:
    weights        = {}
    weights_nobTag = {} 
# ---------------

if not os.path.exists(oDir): os.mkdir(oDir)
print oDir

trg_names = triggerlists[trgList]
if not trg_names: print "### WARNING: empty hlt_names ###"
trg_names_v = vector("string")()
for t in trg_names: trg_names_v.push_back(t)

# to convert weights 
weights_v = vector("string")()
for w in weights: weights_v.push_back(w)
w_nobTag_v = vector("string")()
for w in weights_nobTag: w_nobTag_v.push_back(w)

# to parse variables to the anlyzer
if args.doMixed: config = { "jets_branch_name": "Jets", }
else: config = { "eventInfo_branch_name" : "EventInfo",
              "jets_branch_name": "Jets",
              "genbfromhs_branch_name" : "GenBFromHs",
              "genhs_branch_name" : "GenHs",
              "tl_genhs_branch_name" : "TL_GenHs",
            }
#"muons_branch_name" : "",
#"electrons_branch_name" : "",
#"met_branch_name" : "",
config.update(        
        { "n_gen_events":0,
          "xsec_br" : 0,
          "matcheff": 0,
          "kfactor" : 0,
          "isData"  : False,
          "isSignal" : True,
          "lumiFb" : intLumi_fb,
          "isMixed" : args.doMixed,
          "ofile_update" : False,
         } )

snames = [args.samList]

# process samples
ns = 0
for sname in snames:

    #get file names in all sub-folders:
    reg_exp = iDir+"/alpha_HHTo4B_SM_"+pu+".root" 
    files = glob(reg_exp)
    print "\n ### processing {}".format(sname)        
    print "reg_exp: {}".format(reg_exp) 
 
    #preliminary checks
    if not files: 
        print "WARNING: files do not exist"
        continue
    else:
        if "Run" in files[0]: config["isData"] = True
        if "GluGluToHH" in files[0] or "HHTo4B" in files[0]: config["isSignal"] = True

    #read counters to get generated eventsbj (from alpha ntuple only)
    if not args.doMixed:
        ngenev = 0
        nerr = 0
        hcount = TH1F('hcount', 'num of genrated events',1,0,1)
        for f in files:
            tf = TFile(f)
            if tf.Get('counter/c_nEvents'):
               hcount.Add(tf.Get('counter/c_nEvents'))
            else:
                nerr+=1        
            tf.Close()
        ngenev = hcount.GetBinContent(1)
        config["n_gen_events"]=ngenev
        print  "empty files {}".format(nerr)
        print  "genevts {}".format(ngenev)

    json_str = json.dumps(config)

    #define selectors list
    selector = ComposableSelector(alp.Event)(0, json_str)
    selector.addOperator(BaseOperator(alp.Event)())
    if args.jetCorr == 0:         
        print "- applying JEC Up -"
        selector.addOperator(JEShifterOperator(alp.Event)(+1))
    elif args.jetCorr == 1: 
        print "- applying JEC Down -"
        selector.addOperator(JEShifterOperator(alp.Event)(-1))
    elif args.jetCorr == 2:
        print "- applying JER Up -"
        selector.addOperator(JERShifterOperator(alp.Event)(+1))
    elif args.jetCorr == 3:
        print "- applying JER Down -"
        selector.addOperator(JERShifterOperator(alp.Event)(-1))
#    else:
 #       print "- default JEC-JER applied -"


    selector.addOperator(FolderOperator(alp.Event)("base"))
    selector.addOperator(WeightSumOperator(alp.Event)(w_nobTag_v))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"], w_nobTag_v))
    selector.addOperator(GenJetPlotterOperator(alp.Event)(btagAlgo))

    selector.addOperator(FolderOperator(alp.Event)("acc"))
    selector.addOperator(JetFilterOperator(alp.Event)(args.eta, args.pt, 4))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"], w_nobTag_v))
    selector.addOperator(JetPlotterOperator(alp.Event)(btagAlgo, w_nobTag_v)) #with bTag since jets are sorted
    selector.addOperator(GenJetPlotterOperator(alp.Event)(btagAlgo))

    selector.addOperator(FolderOperator(alp.Event)("btag"))
    selector.addOperator(BTagFilterOperator(alp.Event)(btagAlgo, btag_wp[1], 4, 99, config["isData"], data_path)) #99=noAntitag  3
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"], weights_v))
    selector.addOperator(JetPlotterOperator(alp.Event)(btagAlgo, weights_v))        
    selector.addOperator(GenJetPlotterOperator(alp.Event)(btagAlgo))

    selector.addOperator(FolderOperator(alp.Event)("pair"))
    selector.addOperator(JetPairingOperator(alp.Event)(4))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"], weights_v))
    if args.savePlots: selector.addOperator(JetPlotterOperator(alp.Event)(btagAlgo, weights_v))        
    if args.savePlots: selector.addOperator(DiJetPlotterOperator(alp.Event)(weights_v))

    selector.addOperator(FolderOperator(alp.Event)("alljets"))
    selector.addOperator(MCTruthOperator(alp.Event)(0.4, -1, False))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"], weights_v))

    selector.addOperator(FolderOperator(alp.Event)("fourjets"))
    selector.addOperator(MCTruthOperator(alp.Event)(0.4, 4, False))
    selector.addOperator(CounterOperator(alp.Event)(config["n_gen_events"], weights_v))

    selector.addOperator(EventWriterOperator(alp.Event)(json_str, weights_v))

    #create tChain and process each files
    if args.doMixed: treename = "mix_tree"
    else: treename = "ntuple/tree"
    tchain = TChain(treename)    
    for File in files:                     
        tchain.Add(File)
    ev = tchain.GetEntries()
    nev = numEvents if (numEvents > 0 and numEvents < ev) else ev
    procOpt = "ofile=./HHTo4B_SM_"+pu+".root" if not oDir else "ofile="+oDir+"/HHTo4B_SM_g_"+pu+"_"+str(args.pt).rstrip('.')+"_"+str(args.eta).rstrip('.')+"_"+args.btag+".root"
    print "maxevts {}".format(nev)
    tchain.Process(selector, procOpt, nev)
    ns+=1
   
    #some cleaning
    if not args.doMixed: hcount.Reset()
    print "{}".format(procOpt)

print "### processed {} samples ###".format(ns)
