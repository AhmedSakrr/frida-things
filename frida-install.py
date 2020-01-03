from adbutils import adb
import adbutils
import subprocess
import wget
import os

try:
	check_adb = subprocess.check_output(['which','adb'])
except Exception as e:
	print("[+] Installing ADB")
	sf = subprocess.Popen(['sudo','apt-get','install','adb','-y'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = sf.communicate()

try:
	sf = subprocess.Popen(['adb','connect'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = sf.communicate()
	ADB = adbutils.AdbClient(host="127.0.0.1", port=5037)
except Exception as e:
	print("[*] Cannot Connect via ADB")
	exit()

def Install_download(FRIDA_VERSION="12.8.3",TARGET_ARCH="arm"):
	DOWNLOAD_BASE = "https://github.com/frida/frida/releases/download/{}/".format(FRIDA_VERSION)
	DOWNLOAD_URL = DOWNLOAD_BASE + f"frida-server-{FRIDA_VERSION}-android-{TARGET_ARCH}.xz"
	print("[+] Downloading {} {}".format(FRIDA_VERSION , TARGET_ARCH))
	downloaded_file = wget.download(DOWNLOAD_URL)
	print('\n')
	print("[+] {} {} Downloaded to {} \n".format(FRIDA_VERSION , TARGET_ARCH, downloaded_file))
	return downloaded_file


def install_on_devices(device,serverfile):
	unzip = f"unxz {serverfile}"
	os.system(unzip)
	filename = serverfile.replace('.xz','')
	cmd = f"adb push {filename} /data/local/tmp/"
	print(f"[+] Pushing {filename} to {device}")
	os.system(cmd)
	fileoneserver = f"/data/local/tmp/{filename}"
	chmod = f"adb shell 'su -c chmod 755 {fileoneserver}'"
	print(f"[+] Chmod {filename} in {device}")
	os.system(chmod)	
	ex = f'adb shell "su -c .{fileoneserver} &"'
	print(f"[+] Executing {filename} in {device}")
	os.system(ex)
	print(f"[+] Checking frida connection {device}")
	os.system("frida-ps -U")
	os.remove(filename)

def main():
	arch = ""
	check_arch = subprocess.check_output(['adb','shell','getprop','ro.product.cpu.abi'])
	if 'arm6' in str(check_arch):
		arch = "arm64"
	elif 'arm' in str(check_arch) and not '64' in str(check_arch):
		arch = "arm"
	elif 'x86_64' in str(check_arch):
		arch = "x86_64"
	else:
		arch = "x86"
	downloaded_file = Install_download(TARGET_ARCH=arch)
	for d in ADB.device_list():
	    install_on_devices(d.serial,downloaded_file) 

if __name__ == '__main__':
	main()
