{
  gEnv->SetValue("Root.DynamicPath", "@PWD@/lib");
  gEnv->SetValue("Root.MacroPath", "@PWD@/macros");
  gEnv->SetValue("Root.PluginPath", "@PWD@/etc/plugins");
  gSystem->AddIncludePath("-I@PWD@/include");
  gSystem->AddIncludePath("-I@PWD@/cint/cint/include");
  gSystem->AddIncludePath("-I@PWD@/cint/cint/stl");
  gSystem->AddIncludePath("-I@PWD@/cint/cint/lib");
  TInterpreter::Instance()->AddIncludePath("@PWD@/include");
  TInterpreter::Instance()->AddIncludePath("@PWD@/cint/cint/include");
  TInterpreter::Instance()->AddIncludePath("@PWD@/cint/cint/stl");
  TInterpreter::Instance()->AddIncludePath("@PWD@/cint/cint/lib");
  #include <RtypesCint.h>
  #include <iostream>
  #include <string>
  #include <DllImport.h>
  gROOT->GetPluginManager()->LoadHandlersFromPluginDirs("");
  gROOT->GetPluginManager()->AddHandler("TVirtualPS","image",
					"TImageDump","Postscript",
					"TImageDump()");
  gROOT->GetPluginManager()->AddHandler("TVirtualStreamerInfo",
					"*","TStreamerInfo",
					"RIO","TStreamerInfo()");
  gROOT->GetPluginManager()->AddHandler("TVirtualGraphPainter", "*",
					"TGraphPainter","GraphPainter",
					"TGraphPainter()");
  delete (TFile*) gROOT->ProcessLine(".x tutorials/hsimple.C");
  THtml html;
  html.SetProductName("ROOT");
  html.SetEtcDir("@PWD@/etc/html");
  html.SetHomepage("http://root.cern.ch");
  html.LoadAllLibs();
  html.SetBatch(kTRUE);
  html.MakeAll();
}
