# RaspberryPi-attention
AttentionGo on RaspberryPi

/BlueTooth

    --变量
    --方法
        --- get_state()：获取连接状态
        --- read()：读取数据
        --- send()：上传数据
/Screen

/AudioPlayer

/main

    CarState = 0
    --set up:
        -0: 读取：训练文件 -> 赋值：用户小车等级、训练index、上传index、WIFI名称(如果有)、WIFI密码(如果有)、用户ID(如果有)
        -1: (有以上WIFI相关的三个文件则)：WIFI联网初始化
            开启蓝牙线程(板载蓝牙 或 HC05串口协议)
                读取蓝牙数据 -> 解析json -> 存储WIFI名称、WIFI密码、用户ID至SD卡并赋值 -> WIFI联网初始化
    --blue tooth（线程1）
        0: BlueTooth.read() -> 读取蓝牙数据(如果有) -> 解析json -> 赋值：new-WIFI名称、new-WIFI密码、用户ID
    --main loop:
        -0: Sleep mode / upload mode 休眠模式：数据堆积上传
            --0.0 判断用户是否切换模式
            --0.1 上传数据：
                ---> BlueTooth.get_state() == "connected" ? 通过蓝牙上传BlueTooth.send(堆积数据) : 往下执行
                ---> wifi是否连接 ? 通过wifi上传(post->upload) : 往下执行
        -1: Preparation mode  训练准备模式：用户连接脑电和是在道路初始位置判断
        -2: Train mode  正式训练模式
            --2.0: 物联网
                -判断：(new-WIFI名称 == WIFI名称 || new-WIFI密码 == WIFI密码) ? 不重连 : 重连
                -读取：脑电专注数据 -> 实时上传：(post -> updateDot)
                -读取：Response -> 更新阈值数据、地图(训练模式)
            -2.1: 屏幕初始化(初始化对象)
            -2.2: 播放器初始化(初始化对象)
            -2.3: 地图(训练模式) -> 模式判断与执行
                --2.3.0: 娱乐模式
                    --- 小车运动控制
                        -读取手柄数据 -> 控制行进(左右)方向
                        -读取脑电专注数据 -> 控制行进速度
                    --- 屏幕刷新
                        -计算：目前小车等级 -> 决定：等级对应的页面号
                        -页面刷新(等级对应的页面初始化)
                        -专注度实时刷新
                    --- 声音反馈
                        -专注力上升超过阈值(之前低于阈值) -> 播放音效文件
                --2.3.1: 快速训练模式
                    --- 小车运动控制
                        -脑电专注数据 -> 控制行进速度
                        -PID算法(读取灰度传感器模拟引脚) -> 控制行进方向
                    --- 屏幕刷新
                        -计算：目前小车等级 -> 决定：等级对应的页面号
                        -页面刷新(等级对应的页面初始化)
                        -专注度实时刷新
                --2.3.2: 地图训练模式
                    --- 小车运动控制
                        -脑电专注数据 -> 控制行进速度
                        -PID算法(读取灰度传感器模拟引脚) -> 控制行进方向
                    --- 屏幕刷新
                        -计算：目前训练时间 -> 决定：地图对应的小车形态页面号
                              目前小车等级 -> 决定：等级对应的页面号
                        -页面刷新(等级对应的页面 与 地图对应的小车形态 定时切换)
                        -(等级对应的页面)等级显示、专注度实时刷新
                    --- 声音反馈
                        -专注力上升超过阈值(之前低于阈值) -> 播放音效文件
                        -读取：目前训练时间 和 当前地图  -> 决定：播放训练阶段性音效