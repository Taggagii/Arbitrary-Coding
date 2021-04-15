import subprocess as sub

#making sure user has pip
value = sub.Popen(["python", "-m", "ensurepip"], shell = True)
value.communicate()


def download_packages(names, hide_window = True):
    for name in names:
        value = sub.Popen(["pip", "install", name], hide_window = True)
        value.communicate()
    return "Packages are successfully downloaded"
