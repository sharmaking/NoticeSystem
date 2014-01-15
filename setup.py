from distutils.core import setup
import py2exe

options = {
	"py2exe":{
		"compressed"	: 1,
		"optimize"		: 2,
		"dll_excludes"	: ["MSVCP90.dll"],
		"includes"		: ["sip"],
		"bundle_files"	: 1
	}     
}
setup(
	options		= options,
	zipfile		= None,
	windows		= [{"script": "main.py", "icon_resources": [(1, "main.ico")] }]
)