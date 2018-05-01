import subprocess
import shlex

def RateSentiment(sentiString):
    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split("java -jar ../sentistrength/SentiStrengthCom.jar stdin sentidata ../sentistrength/data/"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    
    stdout_text, stderr_text = p.communicate(sentiString)
    vals = stdout_text.split("\t")

    pos = vals[0]
    neg = vals[1]

    return pos, neg

if __name__ == "__main__":
	print(RateSentiment("bob"))