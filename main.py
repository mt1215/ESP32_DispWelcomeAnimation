import lvgl as lv
import time
from machine import Pin
from espidf import HSPI_HOST
from ili9XXX import ili9488
from my_ft6x36 import FT6X36

# -------------------------
# 背光
# -------------------------
Pin(16, Pin.OUT).value(1)

# -------------------------
# LCD 初始化
# -------------------------
disp = ili9488(
    miso=13,
    mosi=11,
    clk=12,
    cs=10,
    dc=17,
    rst=18,
    spihost=HSPI_HOST,
    mhz=20,
    power=-1,
    backlight=-1,
    factor=16,
    hybrid=True,
    width=320,
    height=480,
    invert=False,
    double_buffer=True,
    half_duplex=False,
)

# -------------------------
# Touch 初始化
# -------------------------
touch = FT6X36(
    sda=6,
    scl=7,
    width=480,
    height=320,
)

touch.register_lvgl()

# 建立開始頁
startup_scr = lv.obj()

# 建立圖片元件
img = lv.img(startup_scr)
img.center()

# 預先載入 5 張 PNG
frames = []

for i in range(1, 6):
    with open("frame%d.png" % i, "rb") as f:
        png = f.read()

    dsc = lv.img_dsc_t({
        "data_size": len(png),
        "data": png
    })

    frames.append(dsc)

# 顯示第一張
img.set_src(frames[0])

lv.scr_load(startup_scr)

start_time = time.ticks_ms()
startup_done = False

# 開機動畫控制
frame_index = 0
last_frame_time = time.ticks_ms()


# =====================================================
# 建立 Main Screen
# =====================================================

main_scr = lv.obj()

coord = lv.label(main_scr)
coord.align(lv.ALIGN.TOP_LEFT, 10, 10)
coord.set_text("X=--- Y=---")

slider = lv.slider(main_scr)
slider.set_width(220)
slider.align(lv.ALIGN.CENTER, 0, 40)

slider_label = lv.label(main_scr)
slider_label.align_to(slider, lv.ALIGN.OUT_TOP_MID, 0, -10)
slider_label.set_text("Slider")

btn = lv.btn(main_scr)
btn.set_size(120, 50)
btn.align(lv.ALIGN.BOTTOM_MID, 0, -20)

btn_text = lv.label(btn)
btn_text.set_text("BARCODE")
btn_text.center()

# =====================================================
# 建立 Barcode Screen
# =====================================================

barcode_scr = lv.obj()
#背景加入
bg_color = lv.palette_lighten(lv.PALETTE.LIGHT_BLUE, 5)
fg_color = lv.palette_darken(lv.PALETTE.BLUE, 4)

qr = lv.qrcode(barcode_scr)
qr.set_size(150)
qr.set_dark_color(fg_color)
qr.set_light_color(bg_color)

# QR Code 內容
data = "https://opto-bt.com/index.html"
qr.update(data, len(data))
qr.center()

# 邊框
qr.set_style_border_color(bg_color, 0)
qr.set_style_border_width(5, 0)

qr_label = lv.label(barcode_scr)
qr_label.set_text("Opto_BT website\nTouch Anywhere")
qr_label.align_to(qr, lv.ALIGN.OUT_TOP_MID, 0, -10)

#label.set_text("BARCODE PAGE\nTouch Anywhere")
#label.center()

# 任意點一下返回 Main
def barcode_event(e):
    if e.get_code() == lv.EVENT.CLICKED:
        lv.scr_load(main_scr)

barcode_scr.add_event_cb(
    barcode_event,
    lv.EVENT.CLICKED,
    None
)

# Main Button → Barcode
def btn_event(e):
    if e.get_code() == lv.EVENT.CLICKED:
        lv.scr_load(barcode_scr)

btn.add_event_cb(
    btn_event,
    lv.EVENT.CLICKED,
    None
)

# 顯示 Main
#lv.scr_load(main_scr)

# =====================================================
# 主迴圈
# =====================================================

last = ""

while True:

    # -------------------------
    # 播放開機 PNG 動畫
    # -------------------------
    if not startup_done:

        if (frame_index < len(frames) - 1 and
                time.ticks_diff(time.ticks_ms(), last_frame_time) >= 2080):

            frame_index += 1
            img.set_src(frames[frame_index])
            last_frame_time = time.ticks_ms()

    # 開機畫面停留 3 秒後切到主畫面
    if (not startup_done and
            time.ticks_diff(time.ticks_ms(), start_time) >= 12000):
        lv.scr_load(main_scr)
        
       # lv.scr_load_anim( main_scr, lv.SCR_LOAD_ANIM.OVER_LEFT,800, 0, False )
          
# MOVE_LEFT	新頁面由右往左滑入（推薦）
# MOVE_RIGHT	新頁面由左往右滑入
# MOVE_TOP	由下往上滑入
# MOVE_BOTTOM	由上往下滑入
# FADE_IN	淡入
# FADE_OUT	淡出
# OVER_LEFT	覆蓋式左滑
# OVER_RIGHT	覆蓋式右滑
        
        
        startup_done = True

    #lv.scr_load(main_scr)
    p = touch.get_point()

    if lv.scr_act() == main_scr:
        if p:
            txt = "X=%d Y=%d" % (p[0], p[1])
        else:
            txt = "X=--- Y=---"

        if txt != last:
            coord.set_text(txt)
            last = txt

    try:
        lv.task_handler()
    except:
        pass

    time.sleep_ms(20)