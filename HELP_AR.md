# دليل استخدام VanitySearch (نسخة مُعدَّلة)

يوضِّح هذا الملف أهمّ الخيارات الجديدة والقديمة مع أمثلة عمليّة باللغة العربية. حاوَلنا جمع أكبر قدر ممكن من السيناريوهات الأكثر شيوعًا.

> ملاحظة: يفترض أنّك تعمل فى مجلد `VanitySearch-1.1` أو تستبدل المسار الكامل للبرنامج عند التنفيذ.

---
## 1. البحث عن قائمة عناوين باستخدام الـGPU (بطاقة واحدة)
```powershell
VanitySearch.exe -gpu -gpuId 0 -i in.txt -o out.txt --keyspace 1:+1000000
```
شرح:
* `-gpu`   يفعِّل الحساب على الـGPU.
* `-gpuId 0` يحدّد البطاقة رقم 0 (فى حال وجود أكثر من بطاقة).
* `-i in.txt` ملف يحتوى على عناوين بيتكوين، سطر لكل عنوان.
* `-o out.txt` يكتب المفاتيح والعناوين المطابقة هنا.
* `--keyspace 1:+1000000` يبدأ من المفتاح 1 ويجرى مليون مفتاح فقط (للاختبار).

---
## 2. ضبط حدّ تكرار الأنماط (القواعد 1-5)
```powershell
VanitySearch.exe -gpu -i targets.txt -r1 4 -r2 3 -r3 2 -r4 2 -r5 2
```
يمنع ظهور أكثر من:
* 4 تكرارات فردية متتالية (القاعدة1)
* 3 تكرارات ثنائية
* 2 تكرارات ثلاثية/رباعية/خماسية

القفز يقلّل الفراغات المرفوضة ويُسرِّع الفحص.

---
## 3. تحديد عدد أنوية الـCPU يدويًّا
```powershell
VanitySearch.exe 1abc -t 8
```
* `1abc` بادئة نصيّة (بحث "فانيتي").
* `-t 8` يستخدم 8 خيوط CPU فقط بدل العدد الافتراضى (كل الأنوية).

---
## 4. البحث فى بادئة نصية مع الحساب المزدوج (غير مضغوط + مضغوط)
```powershell
VanitySearch.exe 1Elon -b -gpu
```
* `-b` يفحص العناوين المضغوطة وغير المضغوطة معًا.
* `-gpu` لتسريع العملية.

---
## 5. البحث عن عنوان واحد كامل (مطابقة تامّة)
```powershell
VanitySearch.exe -i single_addr.txt -stop -gpu
```
* `single_addr.txt` يحتوى عنوانًا واحدًا.
* `-stop` ينهى البرنامج بعد إيجاد العنوان.

---
## 6. تشغيل أكثر من بطاقة رسوميّة
```powershell
VanitySearch.exe bc1q -gpu -gpuId 0,1 -g 2048x256,1024x128
```
* `-gpuId 0,1` يستخدم البطاقتين 0 و1.
* `-g` يدوّن حجم شبكة النواة لكل بطاقة (اختياري للتجريب).

---
## 7. استكمال مهمة سابقة داخل نفس النطاق
```powershell
VanitySearch.exe -i list.txt --keyspace ABCDEF:+1000000 -continue save.dat
```
يحفظ البرنامج تقدّمَه دورياً فى `save.dat` ويستأنف منه لو وجد الملف.

---
## 8. إنشاء زوج مفاتيح عشوائى (للاختبارات)
```powershell
VanitySearch.exe -kp
```
يطبع المفتاح الخاص (WIF وHEX) مع العنوان المقابل.

---
## 9. تحويل مفتاح خاص إلى عنوان
```powershell
VanitySearch.exe -cp 1E99423A4ED27608A15A...
```
`-cp` = compute public key + address من مفتاح خاص HEX.

---
## 10. تحويل مفتاح عام إلى عنوان
```powershell
VanitySearch.exe -ca 04FC970284...
```
`-ca` = compute address من مفتاح عام HEX.

---
## 11. اختبار صحة أنوية GPU مقابل CPU
```powershell
VanitySearch.exe -check -gpu
```
يقارن النتائج بين حساب CPU و GPU للتأكّد من صحة الكيرنل.

---
## 12. سرد البطاقات الرسوميّة المتوافرة
```powershell
VanitySearch.exe -l
```
يطبع قائمة الـGPU المدعومة ومواصفاتها.

---
## 13. مثال كامل شامل لكل الخيارات
```powershell
VanitySearch.exe -gpu -gpuId 0 -t 16 -i targets.txt -o hits.txt \
                -r1 4 -r2 3 -r3 2 -r4 2 -r5 2                   \
                --keyspace 80000000000000000:+FFFFFFFFFF         \
                -stop
```
يبحث داخل نطاق كبير، يستخدم 16 خيط CPU بالإضافة إلى GPU 0، ويقفز وفق القواعد 1-5، ويتوقف بمجرد العثور على جميع الأهداف، ويحفظ النتائج فى `hits.txt`.

---

> **تنبيه أمنى:** البحث عن مفاتيح خاصة حقيقية عملية حسابية شاقة ولا تضمن النجاح، ويجب استخدامها لأهداف تعليمية فقط.
cd "C:\Users\igfi\Desktop\vsearch_bitcrack\VanitySearch-1.1"

.\x64\Release\VanitySearch.exe `
    --keyspace 1:+174876E7FF `
    -b `
    -t 56 `
    -gpu `
    -i addresses.txt `
    -o results_full.txt `
    -r1 3 -r2 2 -r3 2 -r4 2 -r5 2cd "C:\Users\igfi\Desktop\vsearch_bitcrack\VanitySearch-1.1"
    
    .\x64\Release\VanitySearch.exe `
        --keyspace 1:+174876E7FF `
        -b `
        -t 56 `
        -gpu `
        -i addresses.txt `
        -o results_full.txt `
        -r1 3 -r2 2 -r3 2 -r4 2 -r5 2cd "C:\Users\igfi\Desktop\vsearch_bitcrack\VanitySearch-1.1"
        
        .\x64\Release\VanitySearch.exe `
            --keyspace 1:+174876E7FF `
            -b `
            -t 56 `
            -gpu `
            -i addresses.txt `
            -o results_full.txt `
            -r1 3 -r2 2 -r3 2 -r4 2 -r5 2