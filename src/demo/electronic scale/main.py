#微信公众号关注 白话物联网 获取持续更新  淘宝iotnow.taobao.com
#cmd(0)/data(1),data_numbers,register
test = (
0,0,0x11,
2,0,120,

0,3,0xb1,
1,1,0x01,
1,1,0x08,
1,1,0x05,

0,3,0xb2,
1,1,0x05,
1,1,0x3c,
1,1,0x3c,

0,6,0xb3,
1,1,0x05,
1,1,0x3c,
1,1,0x3c,
1,1,0x05,
1,1,0x3c,
1,1,0x3c,

0,1,0xb4,
1,1,0x03,

0,3,0xc0,
1,1,0x28,
1,1,0x08,
1,1,0x04,

0,1,0xc1,
1,1,0xc0,

0,2,0xc2,
1,1,0x0d,
1,1,0x00,

0,2,0xc3,
1,1,0x8d,
1,1,0x2a,

0,2,0xc4,
1,1,0x8d,
1,1,0xee,

0,1,0xc5,
1,1,0x12,

0,1,0x36,#set rgb register
1,1,0xC8,#C0-->zero left top,left to right,top to bottom RGB ,C8-->BGR

0,16,0xe0,
1,1,0x04,
1,1,0x22,
1,1,0x07,
1,1,0x0a,
1,1,0x2e,
1,1,0x30,
1,1,0x25,
1,1,0x2a,
1,1,0x28,
1,1,0x26,
1,1,0x2e,
1,1,0x3a,
1,1,0x00,
1,1,0x01,
1,1,0x03,
1,1,0x13,

0,16,0xe1,
1,1,0x04,
1,1,0x16,
1,1,0x06,
1,1,0x0d,
1,1,0x2d,
1,1,0x26,
1,1,0x23,
1,1,0x27,
1,1,0x27,
1,1,0x25,
1,1,0x2d,
1,1,0x3b,
1,1,0x00,
1,1,0x01,
1,1,0x04,
1,1,0x13,

0,1,0x3a,
1,1,0x05,

0,1,0x35,
1,1,0x00,

0,0,0x29,
1,0,0x2c,
)

XSTART_H = 0xf0
XSTART_L = 0xf1
YSTART_H = 0xf2
YSTART_L = 0xf3
XEND_H = 0xE0
XEND_L = 0xE1
YEND_H = 0xE2
YEND_L = 0xE3


XSTART = 0xD0
XEND = 0xD1
YSTART = 0xD2
YEND = 0xD3

LCD_WIDTH = 132


# 以下报错？为啥？待尝试验证
# XSTART_H = 0x00
# XSTART_L = 0x00
# YSTART_H = 0x00
# YSTART_L = 0x00
#
# XEND_H = 0x00
# XEND_L = 0x00
# YEND_H = 0x00
# YEND_L = 0x84



import utime
from machine import LCD
from machine import Pin
from audio import TTS
from misc import PWM
from usr import fonts


lcd = LCD()

test1 = bytearray(test)




def display_on(para):
    print("display on")
    lcd.lcd_write_cmd(0x11, 1)
    lcd.lcd_write_cmd(0x29, 1)

def display_light(para):
    print("display_light")
    lcd.lcd_write_cmd(0x13, 1)
    lcd.lcd_write_data(para, 2)

def display_off(para):
    print("display off")
    lcd.lcd_write_cmd(0x28, 1)
    lcd.lcd_write_cmd(0x10, 1)


def lcd_invalid(para):
    print("invalid:",para[0], para[1], para[2], para[3])
    lcd.lcd_write_cmd(0x2A, 1)
    lcd.lcd_write_data((para[0]>>8) & 0xff, 1)
    lcd.lcd_write_data(para[0] & 0xff, 1)
    lcd.lcd_write_data((para[2]>>8) & 0xff, 1)
    lcd.lcd_write_data(para[2] & 0xff, 1)
    lcd.lcd_write_cmd(0x2B, 1)
    lcd.lcd_write_data((para[1]>>8) & 0xff, 1)
    lcd.lcd_write_data(para[1] & 0xff, 1)
    lcd.lcd_write_data((para[3]>>8) & 0xff, 1)
    lcd.lcd_write_data(para[3] & 0xff, 1)
    lcd.lcd_write_cmd(0x2C, 1)
    lcd.lcd_write_cmd(0xff, 1)


def lcd_set_cursor(xStart,yStart,xEnd,yEnd):
    print("lcd_set_cursor")
    lcd.lcd_write_cmd(0x2A)
    lcd.lcd_write_data(0x00)  # 起始位置x高位，因为1.8寸屏是128*160, 不大于255, 直接写0省事
    lcd.lcd_write_data(xStart)  # 起始位置x低位，值传递时自动舍弃了高8位，也省得运算了
    lcd.lcd_write_data(0x00)  # 起始位置y高位
    lcd.lcd_write_data(xEnd)  # 起始位置y低位

    lcd.lcd_write_cmd(0x2B)
    lcd.lcd_write_data(0x00)
    lcd.lcd_write_data(yStart)
    lcd.lcd_write_data(0x00)
    lcd.lcd_write_data(yEnd)

    lcd.lcd_write_cmd(0x2c)  # 发送写数据命令

lcd_invalid_data = (
0,4,0x2a,
1,1,XSTART_H,
1,1,XSTART_L,
1,1,XEND_H,
1,1,XEND_L,
0,4,0x2b,
1,1,YSTART_H,
1,1,YSTART_L,
1,1,YEND_H,
1,1,YEND_L,
0,0,0x2c,
)


def lcd_show_image_file(path, x, y, width, heigth, h):
    image_data = []
    read_n = 0  # 已经读取的字节数
    byte_n = 0  # 字节数
    xs = x
    ys = y
    h_step = h  # 按高度h_step个像素点作为步长
    h1 = heigth // h_step  # 当前图片按h_step大小分割，可以得到几个 width * h_step 大小的图片
    h2 = heigth % h_step  # 最后剩下的一块 大小不足 width * h_step 的图片的实际高度
    # print('h1 = {}, h2 = {}'.format(h1, h2))
    with open(path, "rb") as fd:
        end = ''
        while not end:
            if h1 > 0:#还有数据需要读
                image_data = fd.read(width * h_step * 2)
                lcd.lcd_write(bytearray(image_data), xs, ys, xs + width - 1, ys + h_step - 1)
                h1 -= 1
                ys = ys + h_step
                #print('ys={}\r\n'.format(ys))
            elif h2 >0:#说明有剩余最后一块，不整除的高度图像
                image_data = fd.read(width * h2 * 2)
                lcd.lcd_write(bytearray(image_data), xs, ys, xs + width - 1, ys + h2 - 1)
                h2 = 0  # 最后一块只刷一次即可
                #print('h2 ys={}\r\n'.format(ys))
            else:
                end = 1
                #print('start to close image file\r\n')
                fd.close()
                #print('close image file end\r\n')

    '''
    单个字符显示，包括汉字和ASCII
    x - x轴坐标
    y - y轴坐标
    xsize - 字体宽度
    ysize - 字体高度
    ch_buf - 存放汉字字模的元组或者列表
    fc - 字体颜色，RGB565
    bc - 背景颜色，RGB565
    '''
def lcd_show_char(x, y, xsize, ysize, ch_buf, fc, bc):
    rgb_buf = []
    t1 = xsize // 8
    t2 = xsize % 8
    if t2 != 0:
        xsize = (t1 + 1) * 8
    for i in range(0, len(ch_buf)):
        for j in range(0, 8):
            if (ch_buf[i] << j) & 0x80 == 0x00:
                rgb_buf.append(bc & 0xff)
                rgb_buf.append(bc >> 8)
            else:
                rgb_buf.append(fc & 0xff)
                rgb_buf.append(fc >> 8)
    lcd.lcd_write(bytearray(rgb_buf), x, y, x + xsize - 1, y + ysize - 1)

'''
ASCII字符显示,目前支持8x16、16x24的字体大小，
如果需要其他字体大小需要自己增加对应大小的字库数据，并
在下面函数中增加这个对应字库的字典。
x - x轴显示起点
y - y轴显示起点
xsize - 字体宽度
ysize - 字体高度
ch - 待显示的ASCII字符
fc - 字体颜色，RGB565
bc - 背景颜色，RGB565
'''
def lcd_show_ascii(x, y, xsize, ysize, ch, fc, bc):
    ascii_dict = {}
    if xsize == 8 and ysize == 16:
        ascii_dict = fonts.ascii_8x16_dict
    elif xsize == 16 and ysize == 24:
        ascii_dict = fonts.ascii_16x24_dict
    elif xsize == 16 and ysize == 32:
        ascii_dict = fonts.ascii_16x32_dict

    for key in ascii_dict:
        if ch == key:
            lcd_show_char(x, y, xsize, ysize, ascii_dict[key], fc, bc)

'''
显示字符串,目前支持8x16的字体大小，
如果需要其他字体大小需要自己增加对应大小的字库数据，并
在lcd_show_ascii函数中增加这个对应字库的字典。
x - x轴坐标
y - y轴坐标
xsize - 字体宽度
ysize - 字体高度
str - 待显示的 ASCII 字符串
fc - 字体颜色，RGB565
bc - 背景颜色，RGB565
'''
def lcd_show_ascii_str(x, y, xsize, ysize, str, fc, bc):
    xs = x
    ys = y
    if (len(str) * xsize + x) > LCD_WIDTH:
        #print('str length is %d\n'%(len(str) * xsize + x))
        #print('str is %s\n' % str)
        raise Exception('Display out of range')
    for ch in str:
        lcd_show_ascii(xs, ys, xsize, ysize, ch, fc, bc)
        xs += xsize



def hx711_read(sck , dout):
    count = 0
    sck.write(0) #拉低sck 使能AD转换
    while dout.read(): #等待AD转换完成
        utime.sleep_ms(50)
    for i in range(0,24):
        sck.write(1)
        count = count << 1
        sck.write(0)
        if dout.read():
            count = count+1
    sck.write(1)
    #print('count is %x ' % count)
    #count = count ^ 0x800000不用
    if(count & 0x800000): #负数
        count = count & 0x7fffff
        count -= 1 #反码
        count = ~count #原码 不带符号
        bb = int(count)*-1
        #print('count is %d ' % bb)
        #print('count is %x ' % bb)
    sck.write(0)
    return  count




#微信公众号关注 白话物联网 获取持续更新  淘宝iotnow.taobao.com
if __name__ == '__main__':

    lcd_invalid_data = bytearray(lcd_invalid_data)

    lcd.lcd_init(test1, 132, 132, 13000, 1, 3, 0, lcd_invalid_data, None, None, None)

    #lcd.lcd_clear(0xf800)#RED
    #utime.sleep(1)
    #lcd.lcd_clear(0x07E0)#GREEN
    #utime.sleep(1)
    #lcd.lcd_clear(0x001F)#BLUE
    #utime.sleep(1)
    #lcd.lcd_clear(0xFFFF)#white

    # logo_buffer = bytearray(qq_logo_40x40.logo_buffer)
    # lcd.lcd_write(logo_buffer,10,10,49,49)

    lcd.lcd_clear(0x00) #black
    lcd_bg_gpio14 = Pin(Pin.GPIO14, Pin.OUT, Pin.PULL_DISABLE, 1) # 高电平点亮LCD背光，PIN61对应python gpio14 对应CSDK gpio16
    led_gpio8 = Pin(Pin.GPIO8, Pin.OUT, Pin.PULL_DISABLE, 0)  # GPIO8配置成输出模式，默认输出0,LED灯控制，PIN39 对应python gpio8 对应CSDK GPIO121
    lcd_show_image_file("/usr/image.bin", 0, 0, 132, 132, 15)  # 显示开机画面

    '''
           小白派EC600S V1.0开发板 
           外接喇叭播放时，需要使能对应的引脚（引脚70，对应PWM2），给低电平才能发声,这里由于这个GPIO没有开放出来，而是给的PWM，所以用1/1024占空比作为低电平
    '''


    # 参数1：device 0 - 听筒，1 - 耳机，2 - 喇叭
    tts = TTS(0)

    # 获取当前播放音量大小
    #volume_num = tts.getVolume()
    #tts_Log.info("Current TTS volume is %d" % volume_num)

    # 设置音量为8
    volume_num = 8
    tts.setVolume(volume_num)
    #  参数1：优先级 (0-4)
    #  参数2：打断模式，0表示不允许被打断，1表示允许被打断
    #  参数3：模式 （1：UNICODE16(Size end conversion)  2：UTF-8  3：UNICODE16(Don't convert)）
    #  参数4：数据字符串 （待播放字符串）
    pa_pwm = PWM(PWM.PWM2, PWM.ABOVE_MS, 1, 1024)  # 设置PWM 0% 就是低电平,打开PA
    pa_pwm.open()  # 开启PWM输出
    tts.play(1, 1, 2, '.欢迎使用小白派四巨智能电子秤')  # 执行播放
    pa_pwm = PWM(PWM.PWM2, PWM.ABOVE_MS, 1024, 1024)  # 设置PWM 100% 就是高电平,关闭PA
    tts.close()  # 关闭TTS功能

    utime.sleep(4)
    lcd.lcd_clear(0xFFFF)  # white

    fc = 0x001F  # 字体颜色 黑色 可根据需要修改
    #fc = 0x0000  # 字体颜色 黑色 可根据需要修改
    bc = 0xffff  # 背景颜色 白色 可根据需要修改

    #lcd_show_char(50, 30, 16, 32, fonts.ascii_16x32_dict['8'], fc, bc)


    #lcd_show_ascii_str(20, 80, 16, 32, '1000.', fc, bc)
    #lcd_show_ascii_str(20+4*16+8, 80, 16, 32, '0g', fc, bc)

    #hx711_sck_gpio12 = Pin(Pin.GPIO12, Pin.OUT, Pin.PULL_PU , 1)  # sck 接PIN59 对应python gpio12 对应CSDK gpio19
    #hx711_dout_gpio11 = Pin(Pin.GPIO11, Pin.IN, Pin.PULL_PU, 1)  # dout 接PIN58 对应python gpio11 对应CSDK gpio17
    zero_ad_val = 264963
    scal_factor = 2088.4 # 初始状态0g-->0X40FF5(266229)   放置510g-->0x145007(1331207)   差值1064978   f=1064978/510=2088.2

    DIS_X_START = 20
    DIS_Y_START = 60
    DIS_MAX_CHAR_NUM = 6  #最大显示9999.9
    # 微信公众号关注 白话物联网 获取持续更新  淘宝iotnow.taobao.com
    while 1:
        #print('dout is {}'.format(hx711_dout_gpio11.read()))
        # ad_val = hx711_read(hx711_sck_gpio12, hx711_dout_gpio11)
        # print('ad_val is 0x%x ' % ad_val)
        # deta_ad = ad_val-zero_ad_val
        # print('deta_ad is %d ' % deta_ad)
        # weight1 = deta_ad / scal_factor
        # weight = round(weight1,1)
        weight = 1688.8
        print('weight is %.1f g' % weight)
        char_len = len(str(weight))
        # print('char_len is %d'%char_len)



        if(char_len > DIS_MAX_CHAR_NUM):
            lcd_show_ascii_str(DIS_X_START, DIS_Y_START, 16, 32, 'OVER-E', fc, bc) #超过量程
        elif(char_len > 5): #6位
            lcd_show_ascii_str(DIS_X_START, DIS_Y_START, 16, 32, str(weight), fc, bc)
        elif (char_len > 4):  # 5位
            lcd_show_ascii_str(DIS_X_START, DIS_Y_START, 16, 32, ' ', fc, bc)
            lcd_show_ascii_str(DIS_X_START+16, DIS_Y_START, 16, 32, str(weight), fc, bc)
        elif (char_len > 3):  # 4位
            lcd_show_ascii_str(DIS_X_START, DIS_Y_START, 16, 32, '  ', fc, bc)
            lcd_show_ascii_str(DIS_X_START+16*2, DIS_Y_START, 16, 32, str(weight), fc, bc)
        elif (char_len > 2):  # 3位
            lcd_show_ascii_str(DIS_X_START, DIS_Y_START, 16, 32, '   ', fc, bc)
            lcd_show_ascii_str(DIS_X_START+16*3, DIS_Y_START, 16, 32, str(weight), fc, bc)
        else:
            lcd_show_ascii_str(DIS_X_START, DIS_Y_START, 16, 32, str(weight), fc, bc)
        lcd_show_ascii_str(110, 95, 16, 32, 'g', fc, bc)
        utime.sleep_ms(200)


    # while True:
    #     led_gpio8.write(1)  # LED 亮
    #     #print("Led blink test function ON")
    #     utime.sleep(1)
    #     led_gpio8.write(0)  # LED 灭
    #     #print("Led blink test function OFF")
    #     utime.sleep(1)






