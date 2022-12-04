"""
echoLang created by Brian Dean Ullery Copyright 2022
"""

import sys
import os
from http.server import HTTPServer, CGIHTTPRequestHandler

os.chdir("compiler")

pre = "let title = \"Echo! echo...\";\nlet icon = \"\";\n"
code = ""
post = "document.getElementsByTagName(\"title\")[0].innerHTML = title;\ndocument.getElementById(\"icon\").href = icon;\n"

updateCalled = False
if sys.argv[1].split(".")[len(sys.argv[1].split("."))-1] == "room":
  with open("../"+sys.argv[1], 'r+') as f:
    contents = f.read()
    lines = contents.split("\n")
    for i in range(len(lines)):
      if lines[i] and lines[i][0] != "#":
        words = lines[i].split()
        if words[0] == "init":
          code += "let " + words[1] + " = "
          words.pop(0)
          words.pop(0)
          if words[0][0] == "\"":
            code += " ".join(words) + ";\n"
          else:
            code += words[0] + ";\n"
        elif words[0] == "{set":
          if words[1] == "UPDATE":
            code += "let UPDATE = setInterval(function() {\n"
            updateCalled = True
          else:
            code += "function " + words[1] + "() {\n"
        elif words[0] == "}":
          if updateCalled:
            code += "}, 0);\n"
          else:
            code += "}\n"
        elif words[0] == "echo":
          if (len(words) == 2):
            code += words[1] + "();\n"
          else:
            code += "if(" + words[2] + words[3] + words[4] + ") {" + words[
              1] + "()}\n"
        elif words[0] == "say":
          code += "document.body.innerHTML += " + words[1] + "+\"<br>\";\n"
        elif words[0] == "override":
          code += words[len(words) - 1] + " = "
          del words[0]
          del words[len(words) - 1]
          code += "".join(words) + ";\n"
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
          code += "document.body.innerHTML = \"\";\n"
  
  if not os.path.exists("./temp/" + sys.argv[1].replace(".room", "")):
    os.mkdir("./temp/" + sys.argv[1].replace(".room", ""))
  with open('temp/' + sys.argv[1].replace(".room", "") + '/index.html',
            'wt') as f:
    f.write(
      "<head>\n  <title></title>\n  <link rel='icon' id='icon' />\n</head>\n<body>\n  <script defer>\ntry{\n"
      + pre + code + post +
      "} catch (inernalError182939227374) {alert(inernalError182939227374)}\n  </script>\n</body>"
    )
    f.close()
  
  os.chdir('./temp/' + sys.argv[1].replace(".room", ""))
  server_object = HTTPServer(server_address=('', 80),
                             RequestHandlerClass=CGIHTTPRequestHandler)
  print("Serving at URL: http://localhost:80/")
  server_object.serve_forever()