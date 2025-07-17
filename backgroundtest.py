import subprocess
process = subprocess.Popen(['python', 'GamepadReader.py'])
done = False
while not done:
    a = 1
process.terminate()
quit()
