import subprocess
keyboard.send_keys("<ctrl>+l")
time.sleep(0.15)
keyboard.send_keys("<ctrl>+c")
time.sleep(0.15)

text = clipboard.get_selection()
text = text.replace('"', "%22").replace("'", "%27").replace("\\", "%5C")


subprocess.call(["cite", text])
