These files are Python with Pyretic codes for simulating Bellman-ford Algorithm using Mininet
It uses mininet with Abilene topology included (abilene.mn), open using miniedit!
The topology will perform Bellman-ford routing scenario everytime a node send "ping" request to another node
rutebellman.py is the file where algorithm are located
routing2cost.py is the main program (the one should be executed as controller)
wG_bellfordCost.py contained cost of every edge in the topology (if the file doen't exist, every vertex's cost will be set to 1, 
  don't forget to delete "from pyretic.modules.wG_bellfordCost import *" line from routing2cost.py)
These files were edited from my lecturer of Brawijaya University, Widhi Yahya that contained Dijkstra Algorithm at it's original version

Warning: if the files do not work, please install the elder version of Pyretic
Thanks for Ulfa for the help
