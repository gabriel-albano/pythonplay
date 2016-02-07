import subprocess

host = "www.google.com"

#ping -n -q -c 5 -W 2 www.google.com
ping = subprocess.Popen(
    ["ping", "-n", "-q","-c", "5", "-W", "2", host],
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE
)

out, error = ping.communicate()

if error == "":
	print "SUCCESS!"
	print out
	print ""

	#import re
	#matcher = re.compile("\nrtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
	#print matcher.search(out).groups()
	outArray = out.split('\n')
	#print outArray
	#print len(outArray)
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
	json_string = '{"transmitted":"'+ transmitted + ',"received":"'+received+'","loss":"'+loss+'","min":"'+min+'","max":"'+max+'","ave":"'+ave+'"}'
	print json_string

else:
	print 'ERROR!' 
	print error

