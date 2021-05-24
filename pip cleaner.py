#I don't know if this is already a command in pip, but many times I have found myself needing a way to clear out my pip to do testing or because I got tired of having a million 
# things installed when I will never use them again
#so, this script will quickly just unintall everything that's not in the "do_not_delete" list


import subprocess as sub

#get names of all installed pip files
values = sub.Popen("pip list", shell = True, stdout = sub.PIPE).stdout.read().split()

#change them from their binary input (stupid, but I don't care)
values = [values[i].decode('utf-8') for i in range(4, len(values), 2)]

#ADD TO THESE VALUES TO IGNORE CERTAIN FILES YOU WANT TO ACTUALLY KEEP
do_not_delete = ['pip', 'setuptools', 'wheel', 'numpy']

#uninstall
for value in values:
    if value not in do_not_delete:
        sub.Popen(f"pip uninstall -y {value}", shell = False)
        print(f"uninstalled {value}")
    
