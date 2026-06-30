# TVSEP Shocks & Coping Strategies Longitudinal Panel Dataset (2007–2024)

เอกสารกำกับชุดข้อมูล (Data Documentation) และระเบิบวิธีประมวลผลข้อมูล (Data Harmonization Workflow) สำหรับโครงการทำความสะอาดและผูกข้อมูลภัยพิบัติและการรับมือเชิงประวัติศาสตร์ (Longitudinal Unbalanced Panel Data) ของโครงการสํารวจระดับครัวเรือน TVSEP (Thailand Vietnam Socio-Economic Panel) ตั้งแต่ปี 2007 ถึง 2024

---

## 1. ที่มาและความสำคัญของปัญหา (Problem Statement)
ข้อมูลภัยพิบัติ (Shock Module) ของ TVSEP ตลอดระยะเวลาเกือบ 20 ปี มีการปรับเปลี่ยนระบบและเครื่องมือในการจัดเก็บข้อมูลอย่างมีนัยสำคัญ ส่งผลให้โครงสร้างตารางและชื่อตัวแปรไม่เหมือนกัน โดยแบ่งออกเป็น 2 ยุคหลัก:
1. **ยุคกระดาษ (PAPI - ปี 2007 ถึง 2017):** จัดเก็บในรูปแบบตารางเดี่ยวแนวแบน (Flat Table) ตัวแปรการรับมือ (Coping) ถูกบันทึกในรูป "ลำดับความสำคัญ 3 อันดับ" ลงในคอลัมน์ระบบดั้งเดิม (`_x31008`, `_x31009`, `_x31010`) 
2. **ยุคดิจิทัล (CAPI - ปี 2019 ถึง 2024):** ใช้ซอฟต์แวร์ Survey Solutions จัดเก็บข้อมูลแบบฐานข้อมูลเชิงสัมพันธ์แยกตารางแม่-ลูก (`shocks.dta` และ `shocks_detail.dta`) ไม่มีรหัสประจำครัวเรือนดั้งเดิม (`QID`) ติดมาในตารางภัยพิบัติ และข้อมูล Coping บันทึกในรูป Checkbox ลำดับความสำคัญ (`v31108a__1` ถึง `v31108a__3`) 

**เป้าหมายของโครงการนี้:** ทำความสะอาด ดึงข้อมูลที่สูญหาย (Data Loss) กลับคืนมา และยุบรวมคอลัมน์ขนานให้กลายเป็น **Master Unbalanced Panel Dataset** ตารางเดียวที่เสมอกันทุกระลอกปี พร้อมส่งเข้าโมเดลสถิติชั้นสูง เช่น Fixed-Effects (FE) หรือ Random-Effects (RE) Regression ได้ทันที

---

## 2. โครงสร้างรหัสมาตรฐานการรับมือ (Standardized Coping Codebook)
เพื่อให้พฤติกรรมการรับมือข้ามเวลากว่า 17 ปี วิ่งเข้าคอลัมน์เดียวกัน ชุดคำสั่งจะแปลงคำตอบทั้งหมดให้อยู่ในฟอร์แมต Dummy (0 หรือ 1) โดยอิงตามรหัสเล่มคู่มือ 2017 ดั้งเดิม ทั้งหมด 45 กิจกรรมหลัก:

* **1) Livelihood & Production:** `coping_3` (Diversify Portfolio), `coping_4` (Substitute Crops), `coping_5` (Reduced Inputs), `coping_40` (Agri Wage), `coping_41` (Business), `coping_42` (Non-farm Wage), `coping_43` (More Farm Time)
* **2) Collective & Resource Management:** `coping_62` (Infrastructure Action), `coping_63` (Common Property Resource)
* **3) Demographics:** `coping_6` (Out of School), `coping_7` (Children to Relatives), `coping_8` (Adult Migrated for Job), `coping_9` (Adult Migrated to Relatives), `coping_10` (Migrated to Marry)
* **4) Asset Sale:** `coping_11` (Livestock), `coping_12` (Land), `coping_13` (Storage/Rice), `coping_14` (Other Assets)
* **5) Borrowing & Financial:** `coping_15` (Savings), `coping_16` (Insurance), `coping_17` (Relatives), `coping_18` (Neighbours), `coping_19` (Pawnshop), `coping_20` (Informal Lender), `coping_21` (Village Funds), `coping_22` (Other Banks), `coping_23` (BAAC TH), `coping_24` (GSB TH), `coping_25` (Village Bank TH), `coping_26` (VBSP VN), `coping_27` (VBARD VN)
* **6) Grants / Assistance:** `coping_28` (Government), `coping_29` (NGOs), `coping_30` (Relatives Grant), `coping_31` (Friends Grant)
* **7) Energy & Services:** `coping_48` (Lighting)
* **8) Crime Prevention:** `coping_49` (Locks), `coping_50` (Alarm), `coping_51` (Guard), `coping_52` (Watch Dog), `coping_53` (Hiding), `coping_54` (Neighbourhood Watch), `coping_55` (Weapon Self-defense)
* **9) No Response & Other:** `coping_1` (Did Nothing), `coping_90` (Other, specify)
* *หมายเหตุ: รหัสควบคุม `60` (No second activity), `61` (No third activity) จะถูกมองข้าม และรหัส `98` (No Answer) จะส่งผลให้ Dummy ทั้งแถวกลายเป็นค่าว่าง `NaN` โดยอัตโนมัติเพื่อป้องกันอคติเชิงสถิติ*

---

## 3. สรุปกระบวนการทำงานของสคริปต์รายยุค (Data Pipelines Workflow)

### 📌 คลีนนิ่งยุคเก่า (2007 - 2017)
* **Engine การโหลด:** `pyreadstat` รันบน Binary Mode เพื่อข้าม Error คำอธิบายตัวแปรซ้ำ (Duplicate Labels Error)
* **การประมวลผล Coping:** ใช้ตรรกะกวาดดู 3 ช่องเรียงอันดับความสำคัญพร้อมกันด้วยคำสั่ง `.isin([code]).any(axis=1)` ถ้ารหัสตรงกับกิจกรรมใด จะบันทึกในช่อง `coping_xx` ใหม่เป็น `1` หากไม่เจอเลยเป็น `0`
* **การจัดการความถูกต้อง:** ตรวจจับรหัสระบุตัวตนหลัก ย้ายคอลัมน์ `QID` และ `hhid` มาล็อกตำแหน่งไว้ที่ 2 ช่องแรกสุดของตาราง

### 📌 คลีนนิ่งยุคดิจิทัล (2019 - 2024) [3-Way Intersect Fix]
* **การแก้ปัญหาข้อมูลภัยพิบัติหาย (Data Loss Prevention):** เปลี่ยนมาใช้ไฟล์ระดับรายละเอียด (`_shocks_detail.dta`) เป็นแกนตั้งต้นแทนไฟล์ระดับสกรีนนิ่ง เพื่อรักษายอดเหตุการณ์ภัยพิบัติจริงไว้สูงสุด
* **การประกบประเภทภัยและรหัสครัวเรือน:**
    * ทำคำสั่ง `pd.merge()` ดึงประเภทภัย (`v31102b`) จากไฟล์แม่ (`_shocks.dta`) มาเสียบในตารางรายละเอียด
    * ทำคำสั่ง `pd.merge()` ผูก `interview__key` เข้ากับทะเบียนกลาง (`TVSEPXXXX.dta`) เพื่อดึงคอลัมน์รหัสประจำครัวเรือนดั้งเดิม **`QID`** กลับคืนมาประกบที่หัวตารางสำเร็จ
* **การแกะรหัส Coping ยุคใหม่:** ปรับปรุงมาใช้ตรรกะ **Numpy Matrix Exact Match** สแกนผ่านอาร์เรย์ของช่อง `v31108a__1` ถึง `v31108a__3` แก้ไขอาการตรวจจับพลาดและรหัสบิดเบือนจาก Labels ส่งผลให้ค่า Dummy วิ่งเข้าล็อก `coping_1` ถึง `coping_90` อย่างแม่นยำ

---

## 4. โครงสร้างตารางหลังการควบรวม (Panel Harmonization Structure)
เมื่อทำการผูกไฟล์แนวตั้ง (Vertical Append) ข้อมูลภัยพิบัติของทุกปีเข้าด้วยกันเป็นไฟล์ **`TVSEP_Shocks_Unbalanced_Master_Panel_2007_2024.csv`** เนื่องจากเป็นชุดข้อมูลแบบ **Unbalanced Panel** คอลัมน์เฉพาะของแต่ละยุคจะขนานคู่กันไป (เช่น ปีเก่าขึ้นคอลัมน์เงินด้วยชื่อ `_x31005a` ปีใหม่ขึ้นด้วย `v31105a`) ดังนั้น ตัวสคริปต์สเต็ปสุดท้ายจะทำหน้าที่สร้าง **"คอลัมน์ตัวแปรกลาง (Harmonized Central Columns)"** ดึงข้อมูลข้ามระลอกปีให้มาไหลรวมอยู่ในช่องเดียวกันที่หน้าตาราง ดังนี้:

| ชื่อคอลัมน์กลาง | คำอธิบายคุณลักษณะ (Variable Description) | ที่มาจากระลอกปีเก่า (2007-2017) | ที่มาจากระลอกปีใหม่ (2019-2024) |
| :--- | :--- | :--- | :--- |
| **`QID`** | รหัสประจำครัวเรือน TVSEP สากล (ล็อกหน้าสุด) | คอลัมน์ `QID` / `hhid` | ได้จากไฟล์ `TVSEPXXXX.dta` (Crosswalk) |
| **`survey_year`** | ปีคริสต์ศักราชที่ทำการออกสำรวจเก็บข้อมูล | สกัดจากชื่อคลื่น Waves | บันทึกตรงผ่านระบบระบบตัวเลข |
| **`shock_code`** | รหัสตัวเลขระบุประเภทภัยพิบัติที่เกิดขึ้น | คอลัมน์ `_x31002` | คอลัมน์ `v31102d` / `v31102b` |
| **`loss_primary`** | มูลค่าความเสียหายตัวเงินหลัก (ล้าง 'none' เป็น 0) | คอลัมน์ `_x31005a` / `_x31005` | คอลัมน์ `v31105a` |
| **`recovery_time`** | ระยะเวลากิจกรรมฟื้นตัวดิบจากภัยพิบัติ | คอลัมน์ `_x31012a` / `_x31012` | คอลัมน์ `v31112a` |
| **`shocks_Group`** | ประเภทกลุ่มภัยพิบัติแบบกว้าง (Agri / Econ / Social / Demo) | จัดกลุ่มโดยใช้แมปปิ้งรหัส `_x31002` | จัดกลุ่มโดยใช้แมปปิ้งรหัส `v31102d` |
| **`coping_1` ถึง ``coping_90`` | ตัวแปรหุ่น Dummy พฤติกรรมการรับมือ (0 หรือ 1) | แกะจาก `_x31008` ถึง `_x31010` | แกะจาก Matrix `v31108a__1` ถึง `__3` |

---

## 5. คู่มือแนวทางการนำไปวิเคราะห์ผลสถิติใน Stata (Econometric Specification)
ชุดข้อมูลสุดท้ายถูกจัดให้อยู่ในฟอร์แมต **Long-format Unbalanced Panel Data** ในระดับเหตุการณ์ (Event-level) เนื่องจากครัวเรือนหนึ่งสามารถพบภัยพิบัติซ้ำได้ในปีประเมินผลเดียวกัน เวลาวิเคราะห์ในโปรแกรมสถิติ (Stata) แนะนำให้รันตามลำดับขั้นตอนดังนี้:

```stata
* 1. นำเข้าไฟล์ Master Unbalanced Panel ตัวจบที่มีคอลัมน์กลางเรียบร้อยแล้ว
import delimited "TVSEP_Shocks_Panel_Ready_To_Regress.csv", clear

* 2. สร้างรหัสลำดับเหตุการณ์ย่อยเพื่อไม่ให้คู่ QID และ ปี เกิดค่าซ้ำซ้อนจนโปรแกรมปฏิเสธระบบ
bysort qid survey_year: gen event_id = _n
egen panel_id = group(qid)

* 3. ประกาศขอบเขตโครงสร้าง Panel Data
xtset panel_id survey_year

* 4. ตัวอย่างการรันสมการ Regression แบบ Fixed-Effects คุมอคติระดับครัวเรือนและเวลา
* สมการดูผลกระทบของขนาดมูลค่าเงินเสียหาย (loss_primary) ต่อการนำเงินออมมาใช้รับมือ (coping_1)
* โดยใส่ i.survey_year เพื่อทำ Time Fixed Effects ควบคุมปัจจัยมหภาครายปี
xtreg coping_1 loss_primary i.survey_year, fe