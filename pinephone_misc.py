#!/usr/bin/env python3
__author__ = 'Jon Stratton'
import tkinter as tk
import subprocess, sys, re
from functools import partial

commands = {"Reset Modem": "sudo systemctl restart eg25-manager",
   "Disable Keyboard": "gsettings set org.gnome.desktop.a11y.applications screen-keyboard-enabled false"}
#   "Fast Charge": "sudo sh -c '( echo \"1500000\" > /sys/class/power_supply/axp20x-usb/input_current_limit )'"}

# Look at the list above for commands that start with "sudo", remove the sudo, and replace with the commands full path
def mkSudoFileCommands():
   sudo_cmds = []
   for label in commands:
      cmd = commands[label]
      if cmd.startswith("sudo"):
         cmd = cmd.replace("sudo ", "")

         # Swap command with full path
         baseCmd = cmd.split(' ')[0]
         p = subprocess.Popen("which " + baseCmd, stdout=subprocess.PIPE, shell=True)
         (output, err) = p.communicate()
         p_status = p.wait()
         cmdWithPath = output.decode('utf-8').replace('\n', '')
         cmd = cmd.replace(baseCmd, cmdWithPath)

         sudo_cmds.append(cmd)
   return(", ".join(sudo_cmds))

def install():
   # Build Desktop File
   mkdesktop = """sudo sh -c '( echo "[Desktop Entry]
Type=Application
Encoding=UTF-8
Name=Pinephone Misc Commands
Comment=Pinephone Misc Commands
Exec=/usr/local/bin/pinephone_misc.py
Terminal=false
Categories=Tags;Describing;Application" > /usr/share/applications/pinephone_misc.desktop )'"""
   subprocess.call( mkdesktop, shell=True, stdout=None, stderr=None )

   # Build Sudo File
   sudoCommands = mkSudoFileCommands()
   mksudo = """sudo sh -c '( echo "Cmnd_Alias PINEPHONEMISC = """ + sudoCommands + """
%pinephone-misc ALL=NOPASSWD: PINEPHONEMISC" > /etc/sudoers.d/pinephone-misc-sudoers )'"""
   subprocess.call( mksudo, shell=True, stdout=None, stderr=None )

   # Build group and add user to it.
   subprocess.call( "sudo groupadd pinephone-misc", shell=True, stdout=None, stderr=None )
   subprocess.call( "sudo usermod -a -G pinephone-misc $USER", shell=True, stdout=None, stderr=None )

   # Install the script
   thisScript = sys.argv[0]
   subprocess.call( "sudo cp " + thisScript + " /usr/local/bin/", shell=True, stdout=None, stderr=None )

def uninstall():
   subprocess.call( "sudo rm /usr/local/bin/pinephone_misc.py", shell=True, stdout=None, stderr=None )
   subprocess.call( "sudo groupdel pinephone-misc", shell=True, stdout=None, stderr=None )
   subprocess.call( "sudo rm /etc/sudoers.d/pinephone-misc-sudoers", shell=True, stdout=None, stderr=None )
   subprocess.call( "sudo rm /usr/share/applications/pinephone_misc.desktop", shell=True, stdout=None, stderr=None )

def command_exec(cmd):
   code = subprocess.call( cmd, shell=True, stdout=None, stderr=None )
   # print(cmd)

class Application(tk.Frame):
   def __init__(self, master=None):
      super().__init__(master)

      self.master = master
      self.pack()
      self.command_select()

   def command_select(self):
      for widget in self.winfo_children():
          widget.destroy()
      self.master.title("Select Command")
      for label in commands:
         self.main = tk.Button(self, text=label, command=partial(command_exec, commands[label]))
         self.main.pack(side="top")

if (__name__ == '__main__'):
   if len(sys.argv) > 1:
      arg = sys.argv[1]
      if sys.argv[1] == 'uninstall':
         uninstall()
      else:
         install()
   else:
      root = tk.Tk()
      app = Application(master=root)
      app.mainloop()
