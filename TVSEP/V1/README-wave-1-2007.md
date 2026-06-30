# Data Harmonization: TVSEP Shocks Analysis (Wave 1 - 2007 Baseline)

## 1. ข้อมูลภาพรวม (Data Overview)
- **Source File:** `wave-1-shocksclean.dta` (Baseline Year)
- **Observation Count:** 2,916 แถว (เหตุการณ์)
- **Reference Period:** พฤษภาคม 2549 - เมษายน 2550
- **สถานะ:** ข้อมูลปีฐานที่เป็นจุดเริ่มต้นของชุดข้อมูล Panel ทั้งหมด

## 2. การจัดการตัวแปร (Variable Mapping)
- **Shock Type:** ใช้รหัส `_x31002` (เทียบเท่า `shocks__id` ในปี 2022)
- **Financial Mapping:** - `_x31005`: มูลค่าความเสียหายรวม (Total Value of Loss)
    - มีการจัดการค่า 'none' และรหัส Stata Missing (-9, -99) ให้เป็นมาตรฐานเดียวกับ Wave อื่นๆ
- **Coping Strategy:** เจาะลึกตัวแปร `_x31008` ถึง `_x31010` เพื่อทำ Binary Indicators

## 3. การเพิ่มประสิทธิภาพ (Optimization)
- กำหนด dtypes เป็น `category` สำหรับตัวแปรเชิงคุณภาพเพื่อลดการใช้ Memory
- ใช้ Vectorized operations ในการ Map กลุ่ม Shock เพื่อความรวดเร็ว

## 🛠 Revised Variable Logic (Wave 1 - 2007)
1. **Total Loss Calculation:** Summation of `_x31005n` (Asset/Income loss) and `_x31006n` (Extra expenses).
2. **Recovery Status (_x31012):** วัดระยะเวลาการฟื้นตัว (0=<1ปี, 1=1ปี, 2=>1ปีแต่ฟื้นแล้ว, 3=ยังไม่ฟื้น).
3. **Consumption Reduction (_x31011):** ตรวจสอบว่าครัวเรือนมีการลดค่าใช้จ่ายการบริโภคหรือไม่ (1=ลด, 2=ไม่ลด).

# Data Harmonization & Descriptive Analytics: TVSEP Wave 6 (2017)

## 1. ข้อมูลภาพรวม (Data Overview)
- **ปีที่สำรวจ:** 2017 (พุทธศักราช 2560)
- **จำนวนตัวอย่าง:** 3,323 เหตุการณ์ (Shocks)
- **ระบบจัดเก็บ:** Stata (.dta) โดยใช้รหัสตัวแปรมาตรฐาน `_x31xxx`
- **สถานะ:** ทำความสะอาดข้อมูล (Cleaned) และพร้อมสำหรับการวิเคราะห์ Panel Data

## 2. นิยามและการคำนวณตัวแปร (Variable Logic)

### 💰 การวัดมูลค่าความเสียหาย (Financial Impact)
เพื่อให้เห็นมิติของความสูญเสียที่แตกต่างกัน เราจึงคำนวณ 2 รูปแบบ:
1. **Total Impact (3-way Sum):** `_x31005a + _x31005b + _x31006a` 
   - ครอบคลุมทั้ง รายได้ที่หายไป + รายจ่ายที่เพิ่มขึ้น + ทรัพย์สินที่เสียหาย
2. **Core Loss (2-way Sum):** `_x31005a + _x31006a`
   - เน้นเฉพาะความเสียหายเชิงโครงสร้างเศรษฐกิจ (รายได้และทรัพย์สิน) โดยตัดค่าใช้จ่ายแฝงออก

### ⏳ การฟื้นตัว (Recovery Analysis)
- **ตัวแปรต้นทาง:** `_x31012a` (หน่วย: จำนวนเดือน)
- **การวิเคราะห์:** - แสดงการกระจายตัว (Distribution) ตามจำนวนเดือนจริง
  - ทำการ **Standardization** ปรับหมวดหมู่ให้เข้ากับ Wave 1 (0-3) เพื่อใช้เปรียบเทียบ Trend ข้ามทศวรรษ

### 🍽 การรัดเข็มขัด (Consumption Reduction)
- **ตัวแปร:** `_x31011`
- **ความหมาย:** ตรวจสอบว่าครัวเรือนต้องลดค่าใช้จ่ายการบริโภค (เช่น ลดปริมาณอาหาร) เพื่อรับมือกับ Shock หรือไม่

## 3. รายการกราฟวิเคราะห์ (Descriptive Outputs)
ไฟล์ภาพจะถูกบันทึกอัตโนมัติในโฟลเดอร์ `graphs_wave_2017/` ประกอบด้วย:
- **G1:** ความถี่ของเหตุการณ์แยกตามกลุ่ม (Frequency)
- **G2:** ค่าเฉลี่ยผลกระทบรวม (Mean Total Impact - 3 way)
- **G3:** ค่าเฉลี่ยความเสียหายหลัก (Mean Core Loss - 2 way)
- **G4:** สัดส่วนการใช้กลยุทธ์รับมือ (Coping Usage)
- **G5:** ความพยายามในการรับมือ (Coping Intensity)
- **G6:** การกระจายตัวของระยะเวลาฟื้นตัวรายเดือน (Recovery Months)
- **G7:** สถานะการฟื้นตัวแบบมาตรฐาน (Standardized Recovery)
- **G8:** สถิติการลดการบริโภค (Consumption Reduction)

## 4. หมายเหตุ (Technical Notes)
- รหัส **90** ในตัวแปร `_x31012a` ถูกนิยามว่าเป็น "ยังไม่ฟื้นตัว (Not yet recovered)"
- ค่า **'none'** ในคอลัมน์เงินทั้งหมดถูกแปลงเป็น **0** เพื่อความถูกต้องในการคำนวณค่าเฉลี่ย