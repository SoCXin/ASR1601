import log
from machine import I2C
import utime
import checkNet


'''
下面两个全局变量是必须有的，用户可以根据自己的实际项目修改下面两个全局变量的值，
在执行用户代码前，会先打印这两个变量的值。
'''
PROJECT_NAME = "QuecPython_I2C_example"
PROJECT_VERSION = "1.0.0"

checknet = checkNet.CheckNetwork(PROJECT_NAME, PROJECT_VERSION)

'''
I2C使用示例
'''

# 设置日志输出级别
log.basicConfig(level=log.INFO)
i2c_log = log.getLogger("I2C")


if __name__ == '__main__':
    '''
    手动运行本例程时，可以去掉该延时，如果将例程文件名改为main.py，希望开机自动运行时，需要加上该延时,
    否则无法从CDC口看到下面的 poweron_print_once() 中打印的信息
    '''
    utime.sleep(5)
    checknet.poweron_print_once()
    '''
    如果用户程序包含网络相关代码，必须执行 wait_network_connected() 等待网络就绪（拨号成功）；
    如果是网络无关代码，可以屏蔽 wait_network_connected()
    【本例程可以屏蔽下面这一行！】
    '''
    # checknet.wait_network_connected()

    # I2C_SLAVE_ADDR = 0x1B  # i2c 设备地址
    # WHO_AM_I = bytearray({0x02, 0})   # i2c 寄存器地址，以buff的方式传入，取第一个值，计算一个值的长度

    I2C_SLAVE_ADDR = 0x49  # i2c 设备地址
    WHO_AM_I = bytearray({0x03, 0})   # Tos   i2c 寄存器地址，以buff的方式传入，取第一个值，计算一个值的长度
    w_data = bytearray({35, 0})   # 设置tos 寄存器 35度 高温报警
    i2c_obj = I2C(I2C.I2C1, I2C.STANDARD_MODE)  # 返回i2c对象
    i2c_obj.write(I2C_SLAVE_ADDR, WHO_AM_I, 1, w_data, 2) # 写入w_data

    r_data = bytearray(2)  # 创建长度为2的字节数组接收
    temperature = -1.0
    ad_val = -1
    ad_val1 = -1

    while 1:
        i2c_obj.read(I2C_SLAVE_ADDR, WHO_AM_I, 1, r_data, 2, 0)   # read temperature
        # i2c_log.info(r_data[0])
        # i2c_log.info(r_data[1])

        print('< PCT2075 read i2c value= 0x%02x %02x >\n' % (r_data[0] , r_data[1])) # Little  endian
        ad_val = ( (r_data[0] << 8) + (r_data[1]) )  #参考PCT2075 datasheet

        #ad_val = 0X7FF << 5  # 模拟测试负数情况-1     -0.125度
        #ad_val = 0X738 << 5  # 模拟测试负数情况-200   -25.0度
        #ad_val = 0X649 << 5  # 模拟测试负数情况-439   -54.875度
        ad_val = 0X648 << 5  # 模拟测试负数情况-400   -55.0度

        if ad_val & 0x8000: #负数
            ad_val1 = -1* ( ( (( ad_val & 0X7FFF)-1 ) ^ 0X7FFF ) >> 5 )# 参考PCT2075 datasheet
        else:
            ad_val1 = ad_val >> 5
        print('adval is 0X %04x\n' %ad_val1)

        temperature = ad_val1 * 0.125
        print("The temperature is %.3f C\n" %temperature)
        utime.sleep(1)

