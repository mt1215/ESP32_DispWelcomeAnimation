

# ESP32 Display Welcome Animation

A MicroPython + LVGL startup animation demo.

## 🎥 Demo

![Startup Animation](./Result/result001.gif)

> High-quality video: [result001.mp4](./Result/result001.mp4)

# ESP32 Display Welcome Animation

A MicroPython + LVGL startup animation demo for **ESP32-S3** using an **ILI9488 (320×480)** TFT LCD and **FT6X36** capacitive touch controller.

## 🎥 Demo

### Startup Animation

![Startup Animation](./Result/result001.gif)

> 📹 High-quality video: [result001.mp4](./Result/result001.mp4)

---

## ✨ Features

* 🎬 Startup animation using **5 PNG frames**
* 📱 320×480 ILI9488 TFT LCD
* 👆 FT6X36 capacitive touch support
* 🔳 Built-in QR Code page
* 🔄 Multi-screen switching with LVGL
* 📍 Real-time touch coordinate display
* 🐍 Developed with MicroPython + LVGL 9.x

---

## 🖼 Startup Animation Flow

```text
frame1.png
    │
    ▼
frame2.png
    │
    ▼
frame3.png
    │
    ▼
frame4.png
    │
    ▼
frame5.png
    │
    ▼
Main Screen
```

Instead of using GIF decoding, the project preloads multiple PNG images and displays them sequentially to achieve a lightweight and stable startup animation.

---

## 📂 Project Structure

```text
.
├── boot.py
├── main.py
├── my_ft6x36.py
├── frame1.png
├── frame2.png
├── frame3.png
├── frame4.png
├── frame5.png
├── README.md
├── LVGL Bin
└── Result/
    ├── result001.gif
    └── result001.mp4
```

---

## 🛠 Hardware

| Component        | Description     |
| ---------------- | --------------- |
| MCU              | ESP32-S3        |
| Display          | ILI9488 TFT LCD |
| Resolution       | 320 × 480       |
| Touch Controller | FT6X36          |
| Framework        | MicroPython     |
| GUI Library      | LVGL 9.x        |

---

## 📋 Main Functions

### Startup Screen

* Displays a welcome animation using PNG frame sequence.
* Automatically switches to the main interface after playback.

### Main Screen

* Displays touch coordinates.
* Includes an LVGL slider widget.
* Provides a **BARCODE** button to open the QR Code page.

### Barcode Screen

* Displays a QR Code.
* Touch anywhere on the screen to return to the main interface.

---

## 🚀 Why PNG Frames Instead of GIF?

On embedded devices such as ESP32, GIF decoding may consume additional memory and CPU resources.

Using sequential PNG frames provides:

* Better compatibility
* Lower runtime overhead
* Faster startup
* Improved stability
* Easier customization


---

## 📄 License

This project is released under the MIT License.

---

## 👤 Author

Developed as an ESP32-S3 + LVGL startup animation demonstration project.
