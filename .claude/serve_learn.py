import os, sys, runpy
sys.argv = ["http.server", os.environ.get("PORT", "8765"), "--directory", "learn"]
runpy.run_module("http.server", run_name="__main__")
