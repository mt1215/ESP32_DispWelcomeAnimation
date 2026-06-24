from machine import I2C, Pin
import lvgl as lv


class FT6X36:

    def __init__(
        self,
        sda=6,
        scl=7,
        addr=0x38,
        freq=400000,
        width=480,
        height=320,
        inv_x=False,
        inv_y=False,
        swap_xy=False,
    ):

        self.i2c = I2C(
            0,
            sda=Pin(sda),
            scl=Pin(scl),
            freq=freq,
        )

        self.addr = addr
        self.width = width
        self.height = height

        self.inv_x = inv_x
        self.inv_y = inv_y
        self.swap_xy = swap_xy

        self.indev = None

    def scan(self):
        return self.i2c.scan()

    def touched(self):
        try:
            return self.i2c.readfrom_mem(self.addr, 0x02, 1)[0]
        except:
            return 0

    def get_point(self):

        if self.touched() == 0:
            return None

        try:
            d = self.i2c.readfrom_mem(self.addr, 0x03, 4)
        except:
            return None

        x = ((d[0] & 0x0F) << 8) | d[1]
        y = ((d[2] & 0x0F) << 8) | d[3]

        if self.swap_xy:
            x, y = y, x

        if self.inv_x:
            x = self.width - 1 - x

        if self.inv_y:
            y = self.height - 1 - y

        return (x, y)

    # LVGL read callback
    def read(self, indev_drv, data):

        p = self.get_point()

        if p is None:
            data.state = lv.INDEV_STATE.RELEASED
        else:
            data.state = lv.INDEV_STATE.PRESSED
            data.point.x = p[0]
            data.point.y = p[1]

        return False

    # 註冊成 LVGL Input Device
    def register_lvgl(self):

        drv = lv.indev_drv_t()
        drv.init()

        drv.type = lv.INDEV_TYPE.POINTER
        drv.read_cb = self.read

        self.indev = drv.register()

        return self.indev