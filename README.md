HKPC Workshop
=====
https://docs.google.com/presentation/d/1HaaZnJyDwmkY9jQIGIVPQMNGPL5MAGeQJ_zyRxLQ3E4/edit#slide=id.g5fe9e099e6_0_170

### 新的映像檔環境建置完整指令紀錄

使用 2018-11-02-ubuntu-16.04-mate-desktop-preview-bpi-m64-aarch64-sd-emmc.img 

sudo -H pip install --upgrade pip

nano /usr/bin/pip

sudo -H pip3 install --upgrade pip

nano /usr/bin/pip3

**Wrong**
```
from pip import main
if __name__ == '__main__':
    sys.exit(main())
```

**Changed**
```
from pip import __main__
if __name__ == '__main__':
    sys.exit(__main__._main())
```

```bash
curl https://seeed-studio.github.io/pi_repo/public.key | sudo apt-key add -
sudo add-apt-repository ppa:mraa/mraa
echo "deb https://seeed-studio.github.io/pi_repo/ stretch main" | sudo tee /etc/apt/sources.list.d/seeed.list
sudo apt update
sudo apt-get install libupm-dev libupm-java python-upm python3-upm node-upm upm-examples python-mraa
git clone https://github.com/LeMaker/RPi.GPIO_BP -b bananapi
sudo apt-get update
sudo apt-get install python-dev
cd RPi.GPIO_BP
sudo python setup.py install
git clone https://github.com/Seeed-Studio/grove.py
cd grove.py
sudo python setup.py install
cd ~/Download
curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
unzip awscli-bundle.zip
sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws

aws configure

AWS Access Key ID [None]:
AWS Secret Access Key [None]:
Default region name [None]:
Default output format [None]: json
```

Troubleshooting
=====

### ImportError: No module named upm.pyupm_mcp9808

加入mraa源庫並更新apt

```
sudo add-apt-repository ppa:mraa/mraa
sudo apt update
```

安裝python mraa和upm 相關套件

```
sudo apt-get install libupm-dev libupm-java python-upm python3-upm node-upm upm-examples python-mraa
```

### Unable to lock the administration directory (/var/lib/dpkg/) is another process using it?
```
sudo rm /var/lib/dpkg/lock
sudo dpkg --configure -a
```
