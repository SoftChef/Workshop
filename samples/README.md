### controller.py

負責MQTT連線及回報

**Usage**
```python

from controller import BpiController

```


### nodes.py

定義Grove Base HAT 各元件接腳
讀值及控制邏輯

**Usage**
```python

from nodes import Fan,Buzzer,Led,Co2Sensor

```

### airQuality.py

基本情境-環境控制

**Usage**
```bash

pi@bpi-iot-ros-ai:samples$ sudo python airQuality.py

```

### lightRegulator.py

基本情境-照明節能

**Usage**
```bash

pi@bpi-iot-ros-ai:samples$ sudo python lightRegulator.py

```

### createFaceIndex.py



**Usage**
```bash

pi@bpi-iot-ros-ai:samples$ sudo python createFaceIndex.py

```

### createFaceIndex.py && faceRekognition.py

額外情境-門禁監控

**Usage**

輸入臉部資料
1. 到AWS Console -> s3 服務
2. 建立Bucket, 名稱輸入 "hkpc-face-indexs" (過程中設定皆為預設)
3. 建立Folder, 名稱輸入 "<你的名字>" (Example: Frank)
3. 依序執行以下程式
```bash

pi@bpi-iot-ros-ai:samples$ sudo python createFaceIndex.py
pi@bpi-iot-ros-ai:samples$ sudo python faceRekognition.py

```

### smoke.py

額外情境-消防安全

**Usage**
```bash

pi@bpi-iot-ros-ai:samples$ sudo python smoke.py

```

### energyManage.py

額外情境-能源管理

文章參考

1. 數值轉換
https://forum.dexterindustries.com/t/solved-how-to-measure-electric-current-with-grove-electricity-sensor/3117/5

**Usage**
```bash

pi@bpi-iot-ros-ai:samples$ sudo python energyManage.py

```
