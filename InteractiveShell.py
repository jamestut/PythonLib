import code
import readline
import rlcompleter
import importlib.util

def run(pth, **lcls):
	# run the given python file in "pth". local variables are set to "lcls".
	for k, v in lcls.items():
		locals()[k] = v
	with open(pth, 'rb') as f:
		exec(f.read())

def run_console(**lcls):
	# start an interactive shell
	lcls = dict(lcls)
	lcls["INTERACTIVE_SHELL"] = True
	lcls["run"] = lambda pth: run(pth, **lcls)
	console = code.InteractiveConsole(locals=lcls)
	readline.set_completer( rlcompleter.Completer(lcls).complete )
	readline.parse_and_bind("tab: complete")
	console.interact()
