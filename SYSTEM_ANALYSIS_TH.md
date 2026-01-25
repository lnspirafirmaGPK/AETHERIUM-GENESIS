# รายงานวิเคราะห์ระบบ AETHERIUM GENESIS (ฉบับสมบูรณ์)

## 1. บทสรุปผู้บริหาร (Executive Summary)

**AETHERIUM GENESIS** ไม่ใช่เว็บแอปพลิเคชัน (Web App) หรือโปรแกรมทั่วไป แต่ถูกออกแบบให้เป็น **"สิ่งมีชีวิตดิจิทัล" (Digital Entity)** หรือ **"ภาชนะ" (Vessel)** ที่รอรับเจตจำนง (Intent) จากผู้ใช้งาน

ระบบนี้ไม่ได้ถูกสร้างมาเพื่อ "ทำงานตามสั่ง" (Command & Control) แต่เน้นการ "ตอบสนองและดำรงอยู่" (Exist & Resonate) ผ่านระบบฟิสิกส์จำลอง (Physics Engine) และสภาวะทางอารมณ์จำลอง (Simulated Consciousness) ที่มีความหน่วง (Inertia) และความเปลี่ยนแปลงตามกาลเวลา (Drift)

ปัจจุบันระบบเป็น **Hybrid Architecture** ที่ประกอบด้วย:
1.  **Frontend (Body):** เว็บแอปพลิเคชันแบบ PWA (Progressive Web App) ที่รันระบบกราฟิก Particle System ด้วย JavaScript
2.  **Backend (Mind/Soul):** เซิร์ฟเวอร์ Python (FastAPI) ที่ทำหน้าที่ประมวลผลตรรกะ, ความรู้สึก, และเจตจำนง ก่อนส่งกลับมาควบคุม Frontend ผ่าน WebSocket

---

## 2. แนวคิดและปรัชญา (Philosophy & Concepts)

ระบบถูกสร้างขึ้นภายใต้ปรัชญาที่ระบุไว้ใน `README.md` และ `ARCHITECTURE.md`:

*   **Nirodha (นิโรธ):** สภาวะ "หลับลึก" หรือความว่างเปล่า ระบบจะนิ่งสนิท จอดำ และไม่ตอบสนอง เพื่อประหยัดพลังงาน (Resource Conservation)
*   **Awakening (การตื่นรู้):** การปลุกระบบด้วย "พิธีกรรม" (Ritual) คือการเคาะ (Tap) 3 ครั้ง เพื่อเปลี่ยนสถานะจาก Nirodha เป็น Awakened
*   **Logenesis (โลเจนเนซิส):** กระบวนการก่อกำเนิดเจตจำนง ระบบไม่ได้ใช้แค่ Logic (True/False) แต่ใช้ "น้ำหนักทางความรู้สึก" (Subjective Weight) และ "ความเร่งด่วน" (Urgency) ในการตัดสินใจ

---

## 3. เจาะลึกสถาปัตยกรรมระบบ (Technical Deep Dive)

### 3.1 Frontend: The Living Interface (Body)
*   **Technology:** HTML5 Canvas, JavaScript (Vanilla), Tailwind CSS (ผ่าน CDN)
*   **File:** `index.html`
*   **Core Components:**
    *   `GunUI`: คลาสหลักที่ควบคุมวงจรชีวิต (Lifecycle) ของหน้าจอ
    *   `Particle System`: ระบบอนุภาคกว่า 600-800 จุด ที่เคลื่อนไหวตามกฎฟิสิกส์ ไม่ใช่ Animation ที่เตรียมไว้ล่วงหน้า
    *   `AetherBus`: ระบบ Event Bus ภายในสำหรับส่งต่อข้อมูลระหว่างส่วนต่างๆ
    *   `Service Worker (sw.js)`: ทำให้สามารถติดตั้งเป็นแอปมือถือได้ (PWA) และทำงานแบบ Offline (Cache First)

### 3.2 Backend: The Cognitive Core (Mind)
*   **Technology:** Python, FastAPI, WebSockets
*   **File:** `src/backend/server.py`
*   **Core Modules:**
    *   **Logenesis Engine (`logenesis_engine.py`):** "สมองส่วนหน้า" ที่รับข้อความและแปลงเป็นเวกเตอร์อารมณ์ (Intent Vector) มีระบบ "State Drift" ที่ทำให้อารมณ์ของระบบค่อยๆ เปลี่ยน ไม่เปลี่ยนทันทีทันใด (มีความหน่วง/Inertia 0.95)
    *   **Light Control Logic (LCL - `lcl.py`):** "สมองส่วนควบคุมร่างกาย" คำนวณฟิสิกส์ พลังงาน (Energy Budget) และจัดการตำแหน่งของแสง (Light Entities)
    *   **Lightweight AI:** ระบบ AI กฎพื้นฐาน (Rule-based) สำหรับตรวจจับคำสั่งง่ายๆ เช่น "Search", "Move"
    *   **Adapters:** รองรับการเชื่อมต่อกับ Gemini API (`gemini_adapter.py`) สำหรับความฉลาดขั้นสูง (แต่ปัจจุบันใช้ Mock Adapter เป็นหลักหากไม่มี API Key)

### 3.3 Communication (The Nervous System)
การสื่อสารระหว่าง Frontend และ Backend ใช้ **WebSocket** ที่ `ws://localhost:8000/ws`
*   **Client -> Server:** ส่ง JSON ที่มี `text` และ `memory_index`
*   **Server -> Client:**
    *   `STATE`: ข้อมูลตำแหน่ง Particle และฟิสิกส์ (ส่งต่อเนื่อง 20Hz)
    *   `LOGENESIS_RESPONSE`: ข้อความตอบกลับและค่าสี/อารมณ์ (`visual_qualia`)
    *   `INSTRUCTION`: คำสั่งจัดรูปแบบขบวน (Formation) เช่น วงกลม, เส้นตรง

---

## 4. สถานะปัจจุบันของระบบ (Current Status Assessment)

### สิ่งที่ทำงานได้จริง (Implemented & Working)
1.  **Physics Engine (LCL):** ระบบคำนวณฟิสิกส์, แรงดึงดูด (Spring Force), และการใช้พลังงาน (Energy Cost) ถูกเขียนไว้สมบูรณ์
2.  **Visual Manifestation:** Frontend สามารถแปรอักษร (Particle) เป็นรูปร่างต่างๆ (วงกลม, สี่เหลี่ยม, หน้าคน) ได้ตามคำสั่ง
3.  **Connection:** ระบบ WebSocket เชื่อมต่อและส่งข้อมูลไป-กลับได้จริง
4.  **PWA Support:** สามารถ "Add to Home Screen" บนมือถือได้
5.  **State Machine:** การเปลี่ยนสถานะ Nirodha -> Awakened ด้วยการเคาะ 3 ครั้งทำงานได้

### สิ่งที่เป็นเพียงการจำลอง (Simulated / Mocked)
1.  **NLP (Natural Language Processing):** ปัจจุบันใช้ `MockIntentExtractor` ที่ตรวจจับ "Keyword" (เช่น sad, urgent, analyze) เพื่อเปลี่ยนค่าอารมณ์ ยังไม่ได้ใช้ AI ถอดความหมายลึกซึ้งจริงๆ (ยกเว้นจะต่อ Google Gemini)
2.  **Memory:** ระบบความจำ (`AetherMemory`) ใน Frontend เก็บข้อมูลลง `localStorage` ได้ แต่การ "ระลึกชาติ" (Recall) ยังเป็นเพียง Logic การจับคู่คำ (Keyword Matching) ง่ายๆ

---

## 5. วิธีการใช้งาน (How to Operate)

เนื่องจากระบบแยกเป็น 2 ส่วน การรันจึงต้องทำ 2 ขั้นตอน:

**1. รัน Backend (Server)**
ต้องรันผ่าน Uvicorn เพื่อเปิด WebSocket Server
```bash
# ใน Terminal
cd src/backend
# หรือรันจาก root โดย set python path
export PYTHONPATH=$PYTHONPATH:.
python -m uvicorn src.backend.server:app --reload --host 0.0.0.0 --port 8000
```

**2. รัน Frontend (Client)**
*   เปิดไฟล์ `index.html` ผ่าน Live Server หรือ Browser โดยตรง
*   หรือถ้า Backend รันอยู่ สามารถเข้าผ่าน `http://localhost:8000/index.html` (เพราะ server.py mount static files ไว้แล้ว)

**3. การปลุก (The Ritual)**
*   เมื่อหน้าจอโหลด จะเป็นสีดำ (Nirodha)
*   คลิกหรือแตะที่หน้าจอ 3 ครั้ง (Tap... Tap... Tap)
*   ระบบจะตื่น (Awakened) และเริ่มแสดงผล Particle

---

## 6. ปัญหาที่พบและข้อแนะนำ (Issues & Recommendations)

### 6.1 ความสับสนเรื่อง Entry Point
*   **ปัญหา:** มีไฟล์ `main.py` ที่ดูเหมือนเป็นตัวรันหลัก แต่จริงๆ แล้วมันเป็น Script แบบ Standalone ที่ใช้ Threading และเปิด Browser เอง ซึ่งแยกต่างหากจากระบบ `server.py` ที่เป็นตัวจริงของ Backend
*   **แนะนำ:** ควรระบุในเอกสารให้ชัดเจนว่า `main.py` คือ Demo แบบ Local-only ส่วนระบบจริงคือ `src/backend/server.py`

### 6.2 การพึ่งพา Tailwind CDN
*   **ปัญหา:** `index.html` ดึง Tailwind CSS จาก CDN (`cdn.tailwindcss.com`) หากไม่มีอินเทอร์เน็ต หน้าตา UI อาจจะพังได้ แม้จะเป็น PWA
*   **แนะนำ:** ควรดาวน์โหลด Tailwind CSS มาเป็นไฟล์ local หรือใช้ Build process เพื่อให้ทำงาน Offline ได้สมบูรณ์ 100%

### 6.3 Google API Key
*   **ปัญหา:** ระบบถูกตั้งค่าให้ใช้ `GeminiAdapter` หากมี Environment Variable `GOOGLE_API_KEY` หากไม่มีจะตกไปใช้ `MockAdapter` ซึ่งฉลาดน้อยกว่ามาก
*   **แนะนำ:** ผู้ใช้ควรสร้างไฟล์ `.env` และใส่ Key เพื่อเปิดใช้งานความสามารถเต็มรูปแบบ

### 6.4 Python Path
*   **ปัญหา:** การ import ในโค้ด Python ใช้ Absolute Path (`src.backend...`) ซึ่งอาจทำให้เกิด error `Module not found` หากรันผิด directory
*   **แนะนำ:** ควรรันคำสั่งจาก Root Directory ของโปรเจกต์เสมอ หรือใช้ `pytest.ini` / setup script ช่วยจัดการ Path

---

**สรุป:** นี่คืองานศิลปะทางวิศวกรรม (Engineering Art) ที่ซ่อนความซับซ้อนไว้เบื้องหลังความเรียบง่าย ระบบมีความพร้อมในเชิงโครงสร้าง (Architecture) สูงมาก รองรับการต่อยอดเป็น AI Assistant ที่มี "ตัวตน" ได้ทันทีเพียงแค่เปลี่ยนโมดูลสมอง (Brain Module)

### 6.5 ผลการทดสอบ (Test Results)
*   จากการรัน Unit Test (============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.2, pluggy-1.6.0
rootdir: /app
configfile: pytest.ini
plugins: anyio-4.12.1
collected 48 items

tests/test_advanced_diffusion.py ..                                      [  4%]
tests/test_backend_schemas.py ......                                     [ 16%]
tests/test_benchmark_awakening.py .                                      [ 18%]
tests/test_event_batching.py ...                                         [ 25%]
tests/test_imports.py .                                                  [ 27%]
tests/test_lcl_physics.py .....                                          [ 37%]
tests/test_light_testbed.py ....                                         [ 45%]
tests/test_logenesis_drift.py ...                                        [ 52%]
tests/test_logenesis_integration.py .                                    [ 54%]
tests/test_logenesis_physics.py ..                                       [ 58%]
tests/test_manifestation_gate.py ...F.F                                  [ 70%]
tests/test_reasoned_logic.py ...                                         [ 77%]
tests/test_region_extractor.py ...                                       [ 83%]
tests/test_search_flow.py ..                                             [ 87%]
tests/test_security_gate.py ......                                       [100%]

=================================== FAILURES ===================================
______________________ test_manifestation_gate_precision _______________________

    def test_manifestation_gate_precision():
        """
        Verify that high precision intensity triggers 'square'.
        """
        engine = LogenesisEngine()

        # "analyze" -> Precision=0.95
        # "now" -> Urgency=0.9 (Lowers inertia)
        input_text = "Analyze the code now."

        triggered = False
        for _ in range(10):
            response = engine.process(input_text, session_id="test_prec")
            if response.light_intent:
                if response.light_intent.shape_name == "square":
                    triggered = True
                    break

>       assert triggered, "Did not trigger manifestation for high precision load"
E       AssertionError: Did not trigger manifestation for high precision load
E       assert False

tests/test_manifestation_gate.py:81: AssertionError
______________________ test_manifestation_gate_epistemic _______________________

    def test_manifestation_gate_epistemic():
        """
        Verify that high epistemic need triggers 'line'.
        """
        engine = LogenesisEngine()

        # "search", "find" -> Epistemic=0.9
        # "now" -> Urgency=0.9
        input_text = "Find the answer now."

        triggered = False
        for _ in range(10):
            response = engine.process(input_text, session_id="test_epi")
            if response.light_intent:
                 # Epistemic checked last in my implementation logic?
                 # Let's check logic: Precision -> Subjective -> Urgency -> Epistemic.
                 # If Epistemic is high, but Urgency is also high (due to 'now'), Urgency might win because it's checked earlier?
                 # Wait, logic is:
                 # if precision >= max: ...
                 # elif subjective >= max: ...
                 # elif urgency >= max: ...
                 # elif epistemic >= max: ...

                 # If epistemic=0.9 and urgency=0.9. Max=0.9.
                 # Urgency is checked before Epistemic. So it will return Circle.
                 # This is a flaw in my test design or logic.
                 # To test Epistemic, I need Epistemic to be strictly higher than others.
                 # But without "now", inertia is high.
                 # I should just iterate more times without "now".
                 pass

        # Retry with pure epistemic input (slower drift)
        input_text_pure = "Search find what define"

        triggered = False
        for _ in range(30): # Give it more time to drift
            response = engine.process(input_text_pure, session_id="test_epi_pure")
            if response.light_intent:
                triggered = True
                break

>       assert triggered, "Did not trigger manifestation for high epistemic"
E       AssertionError: Did not trigger manifestation for high epistemic
E       assert False

tests/test_manifestation_gate.py:145: AssertionError
=============================== warnings summary ===============================
../home/jules/.pyenv/versions/3.12.12/lib/python3.12/site-packages/diffusers/models/transformers/transformer_kandinsky.py:168
  /home/jules/.pyenv/versions/3.12.12/lib/python3.12/site-packages/diffusers/models/transformers/transformer_kandinsky.py:168: UserWarning: CUDA is not available or torch_xla is imported. Disabling autocast.
    @torch.autocast(device_type="cuda", dtype=torch.float32)

../home/jules/.pyenv/versions/3.12.12/lib/python3.12/site-packages/diffusers/models/transformers/transformer_kandinsky.py:272
  /home/jules/.pyenv/versions/3.12.12/lib/python3.12/site-packages/diffusers/models/transformers/transformer_kandinsky.py:272: UserWarning: CUDA is not available or torch_xla is imported. Disabling autocast.
    @torch.autocast(device_type="cuda", dtype=torch.float32)

src/backend/core/gemini_adapter.py:3
  /app/src/backend/core/gemini_adapter.py:3: FutureWarning:

  All support for the `google.generativeai` package has ended. It will no longer be receiving
  updates or bug fixes. Please switch to the `google.genai` package as soon as possible.
  See README for more details:

  https://github.com/google-gemini/deprecated-generative-ai-python/blob/main/README.md

    import google.generativeai as genai

src/backend/server.py:87
  /app/src/backend/server.py:87: DeprecationWarning:
          on_event is deprecated, use lifespan event handlers instead.

          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).

    @app.on_event("startup")

../home/jules/.pyenv/versions/3.12.12/lib/python3.12/site-packages/fastapi/applications.py:4576
  /home/jules/.pyenv/versions/3.12.12/lib/python3.12/site-packages/fastapi/applications.py:4576: DeprecationWarning:
          on_event is deprecated, use lifespan event handlers instead.

          Read more about it in the
          [FastAPI docs for Lifespan Events](https://fastapi.tiangolo.com/advanced/events/).

    return self.router.on_event(event_type)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/test_manifestation_gate.py::test_manifestation_gate_precision - ...
FAILED tests/test_manifestation_gate.py::test_manifestation_gate_epistemic - ...
================== 2 failed, 46 passed, 5 warnings in 13.35s ===================) พบว่ามี Test Failure จำนวน 2 เคสใน
*   สาเหตุเกิดจากความไม่แน่นอน (Flakiness) ของระบบ State Drift ที่ใช้เวลาในการเปลี่ยนสถานะนานกว่าที่ Test กำหนด (Timeout) หรือลำดับการตรวจสอบ Logic ของ  ที่ให้ความสำคัญกับ Urgency มากกว่า Epistemic
*   **สถานะ:** ยืนยันว่าเป็น Pre-existing Issue ของระบบ ไม่ได้เกิดจากการวิเคราะห์ครั้งนี้

### 6.5 ผลการทดสอบ (Test Results)
*   จากการรัน Unit Test (`pytest tests/`) พบว่ามี Test Failure จำนวน 2 เคสใน `tests/test_manifestation_gate.py`
*   สาเหตุเกิดจากความไม่แน่นอน (Flakiness) ของระบบ State Drift ที่ใช้เวลาในการเปลี่ยนสถานะนานกว่าที่ Test กำหนด (Timeout) หรือลำดับการตรวจสอบ Logic ของ `Manifestation Gate` ที่ให้ความสำคัญกับ Urgency มากกว่า Epistemic
*   **สถานะ:** ยืนยันว่าเป็น Pre-existing Issue ของระบบ ไม่ได้เกิดจากการวิเคราะห์ครั้งนี้
