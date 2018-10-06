import os
import requests
import shutil
import subprocess

__all__ = [
  'install_ngrok',
  'install_apache',
  'install_filemanager',
  'launch_apache',
]

def __shell__(cmd, split=True):
  # get_ipython().system_raw(cmd)
  result = get_ipython().getoutput(cmd, split=split)
  if result and not split:
    result = result.strip('\n')
  return result

def install_filemanager(bin_dir="/tmp"):
  is_apache_avail = os.path.exists('/var/www/html/')
  if is_apache_avail:
    print("calling wget https://ufpr.dl.sourceforge.net/project/extplorer/eXtplorer_2.1.9.zip" )
    get_ipython().system_raw( "wget https://ufpr.dl.sourceforge.net/project/extplorer/eXtplorer_2.1.9.zip" )
    print("calling mv eXtplorer_2.1.9.zip /var/www/html/" )
    get_ipython().system_raw( "mv eXtplorer_2.1.9.zip /var/www/html/" )
    print("calling unzip eXtplorer_2.1.9.zip" )
    get_ipython().system_raw( "unzip /var/www/html/phpFileManager-1.5.zip" )
    print("calling rm /var/www/html/index.html" )
    get_ipython().system_raw( "rm /var/www/html/index.html" )
  else:
    print("apache not installed")
  return

def install_apache(bin_dir="/tmp"):
  """ download and install apache on local vm instance

  Args:
    bin_dir: full path for the target directory for the `apache` binary
  """
  TARGET_DIR = bin_dir
  CWD = os.getcwd()
  is_apache_avail = os.path.exists('/var/www/html/')
  if is_apache_avail:
    print("apache installed")
  else:
    import platform
    plat = platform.platform() # 'Linux-4.4.64+-x86_64-with-Ubuntu-17.10-artful'
    if 'x86_64' in plat:
      
      print("calling apt-get update -qq 2>&1 > /dev/null..." )
      get_ipython().system_raw( "apt-get update -qq 2>&1 > /dev/null" )
      print("calling apt-get -y -qq install apache2 apache2-doc apache2-utils php php7.1-mbstring" )
      get_ipython().system_raw( "apt-get -y -qq install apache2 apache2-doc apache2-utils php php7.1-mbstring" )
      print("calling phpenmod mbstring" )
      get_ipython().system_raw( "phpenmod mbstring" )
      print("calling service apache2 start" )
      get_ipython().system_raw( "service apache2 start" )
      print("calling service apache2 start" )
      get_ipython().system_raw( "service apache2 start" )
      is_apache_avail = os.path.exists('/var/www/html/')

      if is_apache_avail:
        print("apache installed. path={}".format(os.path.join(TARGET_DIR,'ngrok')))
      else:
        # ValueError: ERROR: ngrok not found, path=
        raise ValueError( "ERROR: apache not found, path=".format(TARGET_DIR) )
    else:
      raise NotImplementedError( "ERROR, apache install not configured for this platform, platform={}".format(plat))
    os.chdir(CWD)
    return

def install_ngrok(bin_dir="/tmp"):
  """ download and install ngrok on local vm instance

  Args:
    bin_dir: full path for the target directory for the `ngrok` binary
  """
  TARGET_DIR = bin_dir
  CWD = os.getcwd()
  is_grok_avail = os.path.isfile(os.path.join(TARGET_DIR,'ngrok'))
  if is_grok_avail:
    print("ngrok installed")
  else:
    import platform
    plat = platform.platform() # 'Linux-4.4.64+-x86_64-with-Ubuntu-17.10-artful'
    if 'x86_64' in plat:
      
      os.chdir('/tmp')
      print("calling wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip ..." )
      get_ipython().system_raw( "wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip" )
      print("calling unzip ngrok-stable-linux-amd64.zip ...")
      get_ipython().system_raw( "unzip ngrok-stable-linux-amd64.zip" )
      os.rename("ngrok", "{}/ngrok".format(TARGET_DIR))
      os.remove("ngrok-stable-linux-amd64.zip")
      is_grok_avail = os.path.isfile(os.path.join(TARGET_DIR,'ngrok'))
      os.chdir(TARGET_DIR)
      if is_grok_avail:
        print("ngrok installed. path={}".format(os.path.join(TARGET_DIR,'ngrok')))
      else:
        # ValueError: ERROR: ngrok not found, path=
        raise ValueError( "ERROR: ngrok not found, path=".format(TARGET_DIR) )
    else:
      raise NotImplementedError( "ERROR, ngrok install not configured for this platform, platform={}".format(plat))
    os.chdir(CWD)
    return
    
# tested OK
def launch_apache(bin_dir="/tmp", log_dir="/tmp", retval=False):
  install_ngrok(bin_dir)
  install_apache(bin_dir)
  install_filemanager(bin_dir)
  
  # check status of tensorboard and ngrok
  ps = __shell__("ps -ax")
  is_apache2_running = len([f for f in ps if "apache2" in f ]) > 0
  is_ngrok_running = len([f for f in ps if "ngrok" in f ]) > 0
  print("status: apache={}, ngrok={}".format(is_apache2_running, is_ngrok_running))

  if not is_apache2_running:
    get_ipython().system_raw(
        'apache2 --logdir {} --host 0.0.0.0 --port 6006 &'
        .format(log_dir)
    )
    is_tensorboard_running = True
    
  if not is_ngrok_running:  
    #    grok should be installed in /tmp/ngrok
    get_ipython().system_raw('{}/ngrok http 80 &'.format(bin_dir))
    is_ngrok_running = True

  # get apache2 url
  # BUG: getting connection refused for HTTPConnectionPool(host='localhost', port=4040)
  #     on first run, retry works
  import time
  time.sleep(3)
  retval = requests.get('http://localhost:4040/api/tunnels')
  apache2_url = retval.json()['tunnels'][0]['public_url'].strip()
  print("apache url=", apache2_url)
  if retval:
    return apache2_url
