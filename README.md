# [ASR1601](https://github.com/SoCXin/ASR1601)

[![sites](http://182.61.61.133/link/resources/SoC.png)](http://www.SoC.Xin)

* [asrmicro](http://www.SoC.Xin)：[Cortex-R5](https://github.com/SoCXin/Cortex)
* [L6R6](https://github.com/SoCXin/Level)：624 MHz

## [简介](https://github.com/SoCXin/ASR1601/wiki)

[ASR1601](https://github.com/SoCXin/ASR1601) 是一款高性价比的片上系统（SOC）设备，集成了应用程序处理子系统，通信子系统，音频编解码器和嵌入式pSRAM，以支持单芯片4G LTE功能电话解决方案以及GSM解决方案。 该通信子系统集成了LTE CAT1，GSM调制解调器基带和RF收发器，覆盖450MHz〜2.7GHz频段，可在全球范围内漫游。 该应用子系统运行在Cortex-R5处理器上，该处理器具有集成的多媒体组件，包括摄像头系统，ISP，视频播放/编码，显示控制器和音频编解码器。


[![sites](docs/ASR1601.png)](https://github.com/SoCXin/ASR1601)

#### 关键特性

* LTE Cat.1
* 8Mb SPI pSRAM，200MHz，支持SDR和DDR模式
* XIP和QSPI模式支持的QuaDSPI NAND / NOR闪存控制器，可达120MHz


### [资源收录](https://github.com/SoCXin)

* [参考资源](src/)
* [参考文档](docs/)
* [参考工程](project/)

### [选型建议](https://github.com/SoCXin)

[ASR1601](https://github.com/SoCXin/ASR1601) 为Cat.1方案，相对Cat.4的[ASR1802](https://github.com/SoCXin/ASR1802)具有成本优势，类似产品[UIS8910DM](https://github.com/SoCXin/UIS8910DM)。

芯片的开发模组主要有移远EC600S系列（EC600N:ASR1603,EC600U:UIS8910DM）

* [QuecPython](https://python.quectel.com/wiki/#/)

### 相关工具

* ASR USB(WIN10): Quectel_ASR_Series_UMTS&LTE_Windows_USB_Driver_Customer_V1.0.8
* aboot: ASR原厂工具,可用于EC600S系列模组
* QPYcom 图形化工具  ----> 用于调试，下载脚本和固件
* QMulti 批量下载工具 ----->用于批量下载

### [探索芯世界 www.SoC.xin](http://www.SoC.Xin)
