"""
echoLang created by Brian Dean Ullery Copyright 2022
"""

import sys
import os
from http.server import HTTPServer, CGIHTTPRequestHandler
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", dest= "port" ,type=int, default= "80", help="Website Port [default: 80]")
parser.add_argument("-c", "--compile", dest= "compile", action="store_true", help="Compile as HTML file")
parser.add_argument('file', metavar= 'filename', type=str, help='.room File to Compile')

args = parser.parse_args()

pre = "var title = \"Echo! echo...\";\nvar icon = \"\";\n"
code = ""
post = "document.getElementsByTagName(\"title\")[0].innerHTML = title;\ndocument.getElementById(\"icon\").href = icon;\n"

updateCalled = False
if args.file.split(".")[len(args.file.split(".")) - 1] == "room":
  with open(args.file, 'r+') as f:
    contents = f.read()
    lines = contents.split("\n")
    for i in range(len(lines)):
      if lines[i] and lines[i][0] != "#":
        words = lines[i].split()
        if words[0] == "init":
          code += "var " + words[1] + " = "
          words.pop(0)
          words.pop(0)
          if words[0][0] == "\"":
            code += " ".join(words) + ";\n"
          else:
            code += words[0] + ";\n"
        elif words[0] == "{set":
          if words[1] == "UPDATE":
            code += "var UPDATE = setInterval(function() {\n"
            updateCalled = True
          else:
            code += "function " + words[1] + "() {\n"
        elif words[0] == "}":
          if updateCalled:
            code += "}, 10);\n"
            updateCalled = False
          else:
            code += "}\n"
        elif words[0] == "echo":
          if (len(words) == 2):
            code += words[1] + "();\n"
          else:
            condition = words[:]
            condition.pop(0)
            condition.pop(0)
            code += "if(" + " ".join(condition) + ") {" + words[1] + "()}\n"
        elif words[0] == "say":
          if (len(lines[i].split("\"")) > 1):
            code += "document.getElementById(\"body\").innerHTML += \"" + lines[
              i].split("\"")[1] + "<br>\";\n"
          else:
            code += "document.getElementById(\"body\").innerHTML += " + words[
              1] + "+\"<br>\";\n"
        elif words[0] == "override":
          code += words[len(words) - 1] + " = "
          del words[0]
          del words[len(words) - 1]
          if words[0][0] == "\"":
            code += " ".join(words) + ";\n"
          else:
            code += words[0] + ";\n"
        elif words[0] == "overrideReal":
          code += words[len(words) - 1] + " = Number(prompt("
          del words[0]
          del words[len(words) - 1]
          code += " ".join(words) + "));\n"
        elif words[0] == "overrideStr":
          code += words[len(words) - 1] + " = prompt("
          del words[0]
          del words[len(words) - 1]
          code += " ".join(words) + ");\n"
        elif words[0] == "mute":
          code += "document.getElementById(\"body\").innerHTML = \"\";\n"
        elif words[0] == "wait":
          code += "setTimeout(function() {" + words[
            1] + "(); document.getElementsByTagName(\"title\")[0].innerHTML = title; document.getElementById(\"icon\").href = icon}, " + words[
              2] + ");\n"
        elif words[0] == "listen":
          code += "document.addEventListener(\"keydown\",(e)=>{if(e.key===\"" + words[
            1] + "\"){" + words[2] + "()}});\n"

  if not os.path.exists(os.path.dirname(os.path.realpath(__file__))+'/temp/' + "".join("".join(args.file.replace(".room", "").split(".")).split("/"))):
    os.mkdir(os.path.dirname(os.path.realpath(__file__))+'/temp/' + "".join("".join(args.file.replace(".room", "").split(".")).split("/")))
  os.chdir(os.path.dirname(os.path.realpath(__file__))+'/temp/' + "".join("".join(args.file.replace(".room", "").split(".")).split("/")))
  with open('./index.html', 'wt') as f:
    f.write(
      "<head>\n  <title></title>\n  <link rel='icon' id='icon' />\n</head>\n<body>\n  <div id=\"body\"></div>\n  <script defer>\ntry{\n"
      + pre + code + post +
      "} catch (inernalError182939227374) {alert(inernalError182939227374); console.log(inernalError182939227374)}\n  </script>\n</body>"
    )
    f.close()

  if args.compile:
    print("\nHTML file can be found at destination:\nfile://"+os.getcwd()+"/index.html\n")

  server_object = HTTPServer(server_address=('', args.port),
                             RequestHandlerClass=CGIHTTPRequestHandler)
  print(f"Serving at URL: http://localhost:{args.port}/")
  server_object.serve_forever()
