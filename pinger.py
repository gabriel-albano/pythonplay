#!/usr/bin/env python
# ping a list of host with threads for increase speed
# use standard linux /bin/ping utility

from threading import Thread
import subprocess
import Queue
import re
import imp
import logging

alog    = imp.load_source('alog', 'logger.py')
logger  = alog.getLogger('pinger')
logger.setLevel(logging.DEBUG)

# some global vars
num_threads = 15
ips_q = Queue.Queue()
out_q = Queue.Queue()

# load IP array from config.py
config = imp.load_source('config', 'config.py')

# thread code : wraps system ping command
def thread_pinger(i, q):
  """Pings hosts in queue"""
  while True:
    # get an IP item form queue
    ip = q.get()
    # ping it
    args=["ping", "-n", "-q","-c", "5", "-W", "2", str(ip)]
    p_ping = subprocess.Popen(args,
                              shell=False,
                              stdout=subprocess.PIPE)
    # save ping stdout
    p_ping_out = p_ping.communicate()[0]

    if (p_ping.wait() == 0):
      ## rtt min/avg/max/mdev = 22.293/22.293/22.293/0.000 ms
      #search = re.search(r'rtt min/avg/max/mdev = (.*)/(.*)/(.*)/(.*) ms',
      #                   p_ping_out, re.M|re.I)
      #ping_rtt = search.group(2)
      #out_q.put("OK " + str(ip) + " rtt= "+ ping_rtt)

      outArray = p_ping_out.split('\n')
      stats1 = outArray[3].split(',')
      transmitted = stats1[0][0:1]  
      received = stats1[1].strip()[0:1]
      p = stats1[2].strip().index('%')
      loss = stats1[2].strip()[0:p+1]
  
      #min/avg/max/mdev
      stats2 = outArray[4].split('=')
      stats2Vals = stats2[1].split('/')
      min=stats2Vals[0]
      ave=stats2Vals[1]
      max=stats2Vals[2]
      res = {"transmitted":transmitted, "received":received, "loss":loss, "min":min,"max":max,"ave":ave}
      json_string = '{"host":"'+ str(ip) +'",transmitted":"'+ transmitted + ',"received":"'+received+'","loss":"'+loss+'","min":"'+min+'","max":"'+max+'","ave":"'+ave+'"}'
      out_q.put(json_string);

    # update queue : this ip is processed 
    q.task_done()

# start the thread pool
for i in range(num_threads):
  worker = Thread(target=thread_pinger, args=(i, ips_q))
  worker.setDaemon(True)
  worker.start()

# fill queue
for ip in config.ips:
  ips_q.put(ip)

# wait until worker threads are done to exit    
ips_q.join()

# print result
while True:
  try:
    msg = out_q.get_nowait()
  except Queue.Empty:
    break
  #print msg
  logger.info(msg)