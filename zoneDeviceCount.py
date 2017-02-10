#!/usr/bin/env python
  

from flask import Flask, request
from flask import render_template, jsonify
import json

ZoneMemDB = {}
ZoneCountMemDB = {}
zoneName = "zone3"
whichzone = "System Campus>SJC-24>3rd Floor"
ZoneCountMemDB[whichzone] = 0;

#whichzone = "System Campus>Shelby Store 612>Shelby 0612 Indoor>A14"

app = Flask(__name__)


@app.route("/count")
def count():
    return str(ZoneCountMemDB[whichzone])

@app.route("/zonename")
def zname():
    return str(zoneName)

#
# dict1 = mac, zone
# dict2 = zone, count
#
@app.route('/notify',methods=['POST'])
def foo():
   dataDict = json.loads(request.data.decode("utf-8"))
   notices =  dataDict['notifications']
   for x in notices:
       zoneName = x['locationMapHierarchy']
       mac = x['deviceId']

       # if u get the "OUTSIDE" notification
       # simply remove the mac on the DB if it exists
       # and decrement count

       if x['boundary'] == "OUTSIDE":
           print ("OUT: ", mac);
           if mac in ZoneMemDB:
	       del ZoneMemDB[mac]
           if zoneName in ZoneCountMemDB:
               if ZoneCountMemDB[zoneName] > 0:
                   ZoneCountMemDB[zoneName] -= 1;
           return "OK"

       # if mac was already present, decrement old zone counter
       # and increment new zone counter

       if mac in ZoneMemDB:
           oldzone = ZoneMemDB[mac];
           ZoneCountMemDB[oldzone] -= 1;

           ZoneMemDB[mac] = zoneName;
           if zoneName in ZoneCountMemDB:
	       #print ("add one")
               ZoneCountMemDB[zoneName] += 1;
           else:
	       #print ("add first")
               ZoneCountMemDB[zoneName] = 1;
	 
       else:
           print ("MAC coming in very first time")
           ZoneMemDB[mac] = zoneName;
           if zoneName in ZoneCountMemDB:
               ZoneCountMemDB[zoneName] += 1;
           else:
               ZoneCountMemDB[zoneName] = 1;

       
       
   print ZoneCountMemDB
   #print ZoneMemDB

   return "OK"

if __name__ == '__main__':
   app.run('0.0.0.0')
