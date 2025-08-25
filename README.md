# PDF to Excel Converter (โปรแกรมแปลง PDF เป็น Excel)

โปรแกรม Python สำหรับแปลงไฟล์ PDF เป็น Excel โดยรองรับภาษาไทยอย่างสมบูรณ์

## คุณสมบัติหลัก (Features)

### 🎯 การแปลงไฟล์ (File Conversion)
- **รองรับไฟล์ PDF แบบ Text-based** - แปลงตารางและข้อความได้อย่างแม่นยำ
- **รักษาโครงสร้างตาราง** - เก็บรูปแบบและการจัดเรียงข้อมูลเดิม
- **การแปลงแบบ Batch** - ประมวลผลหลายไฟล์พร้อมกัน

### 🇹🇭 การรองรับภาษาไทย (Thai Language Support)
- **ฟอนต์ภาษาไทย** - TH Sarabun New, Angsana New, Cordia New
- **การแสดงผลที่ถูกต้อง** - ตัวอักษรไทยไม่เพี้ยน ไม่สลับลำดับ
- **ความแม่นยำสูง** - เป้าหมาย ≥ 95% สำหรับเนื้อหาภาษาไทย

### 💻 ส่วนติดต่อผู้ใช้ (User Interface)
- **GUI แบบ Modern** - ใช้งานง่าย เหมาะกับผู้ใช้ทั่วไป
- **Command Line Interface** - สำหรับการใช้งานแบบ Script และ Automation
- **Progress Bar** - แสดงสถานะการประมวลผลแบบ Real-time

## การติดตั้ง (Installation)

### ความต้องการของระบบ (System Requirements)
- Python 3.8 หรือใหม่กว่า
- Windows 10/11, macOS 10.15+, หรือ Ubuntu 18.04+
- RAM อย่างน้อย 4GB (แนะนำ 8GB สำหรับไฟล์ขนาดใหญ่)

### วิธีการติดตั้ง

1. **Clone Repository**
```bash
git clone https://github.com/mymy3399/Dockerfile.git
cd Dockerfile
```

2. **ติดตั้ง Dependencies**
```bash
pip install -r requirements.txt
```

3. **ทดสอบการติดตั้ง**
```bash
python main.py --help
```

## การใช้งาน (Usage)

### 1. GUI Mode (แนะนำสำหรับผู้ใช้ทั่วไป)

เรียกใช้โปรแกรมแบบ GUI:
```bash
python main.py
```

#### ขั้นตอนการใช้งาน GUI:
1. **เลือกไฟล์ PDF** - คลิก "เลือกไฟล์" หรือ "เลือกหลายไฟล์"
2. **เลือกโฟลเดอร์ผลลัพธ์** - คลิก "เลือกโฟลเดอร์"
3. **เริ่มแปลง** - คลิก "แปลงไฟล์เดียว" หรือ "แปลงทั้งหมด"

### 2. Command Line Mode (สำหรับ Advanced Users)

#### แปลงไฟล์เดียว:
```bash
python main.py document.pdf
python main.py document.pdf -o output.xlsx
```

#### แปลงหลายไฟล์:
```bash
python main.py file1.pdf file2.pdf file3.pdf -d output_folder/
```

#### แปลงไฟล์ทั้งหมดในโฟลเดอร์:
```bash
python main.py --batch input_folder/ -d output_folder/
```

#### ตัวอย่างการใช้งาน Advanced:
```bash
# แปลงพร้อมกำหนดระดับ Log
python main.py documents/ -d converted/ --log-level DEBUG

# แปลงโดยไม่สร้างไฟล์สรุป
python main.py *.pdf -d output/ --no-summary

# บังคับใช้ Command Line (ไม่เปิด GUI)
python main.py --cli file.pdf
```

## โครงสร้างโปรแกรม (Project Structure)

```
pdf-to-excel-converter/
├── src/                          # โค้ดหลัก
│   ├── __init__.py
│   ├── pdf_parser.py            # การอ่านและแยกข้อมูล PDF
│   ├── excel_writer.py          # การสร้างไฟล์ Excel
│   ├── thai_handler.py          # การจัดการข้อความภาษาไทย
│   ├── batch_processor.py       # การประมวลผลหลายไฟล์
│   └── ui/                      # ส่วนติดต่อผู้ใช้
│       ├── main_window.py       # หน้าต่างหลัก GUI
│       └── progress_bar.py      # แถบแสดงความคืบหน้า
├── tests/                       # การทดสอบ
│   ├── test_pdf_parser.py
│   ├── test_excel_writer.py
│   ├── test_thai_handler.py
│   └── sample_files/           # ไฟล์ตัวอย่างสำหรับทดสอบ
├── main.py                     # จุดเริ่มต้นโปรแกรม
├── requirements.txt            # รายการ Dependencies
└── README.md                   # คู่มือการใช้งาน
```

## การทดสอบ (Testing)

### รันการทดสอบทั้งหมด:
```bash
python -m pytest tests/ -v
```

### รันการทดสอบแยกแต่ละโมดูล:
```bash
python -m pytest tests/test_pdf_parser.py -v
python -m pytest tests/test_thai_handler.py -v
python -m pytest tests/test_excel_writer.py -v
```

### ทดสอบด้วยไฟล์จริง:
```bash
# สร้างไฟล์ทดสอบในโฟลเดอร์ tests/sample_files/
python main.py tests/sample_files/sample_thai.pdf -o test_output.xlsx
```

## ข้อกำหนดด้านประสิทธิภาพ (Performance Requirements)

| เกณฑ์ | เป้าหมาย | หมายเหตุ |
|-------|---------|----------|
| แปลงไฟล์ 10 หน้า | ≤ 5 วินาที | ขึ้นกับความซับซ้อนของตาราง |
| ไฟล์สูงสุด | 200 หน้า | แนะนำแบ่งไฟล์ใหญ่ออกเป็นส่วนย่อย |
| การใช้ Memory | < 500MB | สำหรับไฟล์ 100 หน้า |
| ความแม่นยำภาษาไทย | ≥ 95% | ขึ้นกับคุณภาพของ PDF |
| ความแม่นยำตาราง | ≥ 90% | สำหรับไฟล์ที่มีตารางซับซ้อน |

## การแก้ไขปัญหา (Troubleshooting)

### ปัญหาที่พบบ่อย:

#### 1. ฟอนต์ภาษาไทยแสดงผลไม่ถูกต้อง
```bash
# ตรวจสอบฟอนต์ที่ติดตั้งในระบบ
python -c "from src.ui.main_window import MainWindow; app = MainWindow(); app._test_thai_fonts()"
```

#### 2. PDF อ่านไม่ได้หรือผิดพลาด
```bash
# ตรวจสอบความถูกต้องของไฟล์ PDF
python main.py --cli your_file.pdf --log-level DEBUG
```

#### 3. การแปลงล้มเหลว
```bash
# ดู Log รายละเอียด
python main.py your_file.pdf --log-level DEBUG
```

### ข้อจำกัด (Limitations):
- รองรับเฉพาะ PDF แบบ Text-based (ไม่รองรับรูปภาพหอบข้อความ)
- ตารางซับซ้อนมากอาจแปลงได้ไม่สมบูรณ์ 100%
- ไฟล์ที่มี Password protection ต้อง unlock ก่อน

## การพัฒนา (Development)

### การติดตั้งสำหรับ Development:
```bash
git clone https://github.com/mymy3399/Dockerfile.git
cd Dockerfile
pip install -r requirements.txt
pip install -e .
```

### Code Style:
```bash
# ตรวจสอบ Code Style
black src/ tests/
flake8 src/ tests/
```

### เพิ่มฟีเจอร์ใหม่:
1. Fork Repository
2. สร้าง Feature Branch: `git checkout -b feature/new-feature`
3. เขียน Tests สำหรับฟีเจอร์ใหม่
4. Implement ฟีเจอร์
5. Run Tests: `pytest tests/`
6. Commit และ Push
7. สร้าง Pull Request

## การสนับสนุน (Support)

### หากพบปัญหา:
1. ตรวจสอบ [Issues](https://github.com/mymy3399/Dockerfile/issues) ที่มีอยู่
2. สร้าง Issue ใหม่พร้อมรายละเอียด:
   - เวอร์ชัน Python และ OS
   - ไฟล์ PDF ที่มีปัญหา (ถ้าสามารถแชร์ได้)
   - Error message ที่เกิดขึ้น
   - ขั้นตอนการทำให้เกิดปัญหาซ้ำ

### การร่วมพัฒนา:
- สร้าง Feature Request ใน Issues
- ส่ง Pull Request สำหรับการแก้ไข
- ปรับปรุงเอกสาร

## License

MIT License - ดูรายละเอียดใน [LICENSE](LICENSE) file.

## เครดิต (Credits)

### เทคโนโลยีที่ใช้:
- **pdfplumber** - สำหรับการอ่าน PDF
- **openpyxl** - สำหรับการสร้างไฟล์ Excel
- **pandas** - สำหรับการจัดการข้อมูล
- **tkinter** - สำหรับ GUI
- **PyMuPDF** - สำหรับการอ่าน PDF แบบ Advanced

### ฟอนต์ภาษาไทย:
- TH Sarabun New - NECTEC
- Angsana New - Microsoft
- Cordia New - Microsoft

---

**หมายเหตุ**: โปรแกรมนี้พัฒนาขึ้นเพื่อการศึกษาและการใช้งานทั่วไป ผู้ใช้ควรตรวจสอบความถูกต้องของผลลัพธ์ก่อนนำไปใช้งานจริง

**Note**: This program is developed for educational and general use purposes. Users should verify the accuracy of results before production use.