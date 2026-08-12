# Beginner's Guide — Computer Troubleshooting Expert System

**Note:** This guide is for developers who are new to the project or to expert
systems. It is NOT part of the academic submission — the graded documentation
lives in the `docs/` folder (`problem_analysis.md`, `knowledge_base.md`,
`inference_design.md`, `testing_evaluation.md`, `report_outline.md`).

---

## 1. What is this project?

A small **command-line program** written in plain Python. You tell it what is
wrong with your computer (for example "the screen is blank"), answer a few
**Yes/No questions**, and it suggests possible causes (diagnoses) such as a
"Display problem" or a "Power problem", together with a short explanation and
a safe recommendation.

The program is a classic **expert system**. An expert system is software that
stores human knowledge (rules) in a separate file and uses a "brain" (an
inference engine) to reason with that knowledge.

### The three big ideas

1. **Facts** — small pieces of information, e.g. `screen_blank`, `fans_not_running`.
2. **Rules** — "IF these facts are true THEN this new fact is true".
3. **Inference engine** — a generic loop that applies the rules to the facts
   to draw conclusions.

---

## 2. Project structure (what each file does)

```
computer-troubleshooting-expert-system/
├── main.py                 # Entry point. Runs the CLI (menu, questions, results).
├── engine.py               # The inference engine (the "brain"). Generic, no domain logic.
├── questionnaire.py        # Asks the relevant questions, converts answers into facts.
├── knowledge_base.py       # Loads + validates the JSON data files.
├── models.py               # Small data structures: Rule, Question, WorkingMemory.
├── data/
│   ├── knowledge_base.json # ALL the expert rules (the domain knowledge).
│   └── questions.json      # The main menu + question definitions.
├── evaluation/
│   ├── cases.py            # The 10 (+1) test scenarios.
│   └── run_evaluation.py   # Runs the scenarios automatically.
├── docs/                   # The academic documentation.
└── README.md
```

**Key point:** `engine.py` contains **no** computer knowledge. All knowledge
("if the screen is blank and fans run, it may be a display problem") lives in
`data/knowledge_base.json`. If you want to teach the system something new, you
edit the JSON file — you never touch the engine.

---

## 3. How the program works (step by step)

```
You            → Questionnaire → Facts → Inference Engine → Diagnoses
                                              │
                                     reads rules from
                                              │
                                   knowledge_base.json
```

1. The program shows a menu: **"What is your main problem?"** (9 options).
2. You pick one, e.g. "Computer does not turn on".
3. The **questionnaire** asks only the questions related to that problem
   (4–6 questions, each answered Yes/No). No irrelevant questions.
4. Each answer becomes a **fact** in **working memory**
   (e.g. Yes to "Is the power cable firmly connected?" → `power_cable_ok`).
5. The **inference engine** looks at the facts, finds rules whose conditions
   are satisfied, and fires them. Firing a rule adds its conclusion to the
   facts. It repeats this until nothing new can be inferred.
6. Facts starting with `diagnosis_` are the **final diagnoses**. They are
   displayed with their human-readable explanation and recommendation.
7. If no diagnosis is reached, the program says the evidence is **insufficient**
   and shows any partial conclusions.
8. You can optionally view a **detailed reasoning trace** — every rule that
   fired, in order.

### Example walkthrough

Menu choice: "Computer gets hot or shuts down"

Answers:
- Does the computer switch on and stay running? → **Yes** → `computer_running`
- Does it become unusually hot? → **Yes** → `computer_hot`
- Do the fans spin? → **No** → `fans_not_running`
- Does it shut down unexpectedly? → **Yes** → `shuts_down_unexpectedly`

The engine now finds:
```
Rule O1: IF computer_running AND computer_hot AND fans_not_running
         THEN cooling_problem                     ← new intermediate fact
Rule O3: IF cooling_problem AND shuts_down_unexpectedly
         THEN diagnosis_overheating               ← final diagnosis
```

Result:
```
Possible diagnosis: Overheating problem
Reasoning:
  - The system first inferred a cooling problem, which combined with
    unexpected shutdowns supports an overheating diagnosis.
Recommendation:
  - Check that the cooling vents are not blocked and verify that the
    cooling fans are operating normally.
```

This is **forward chaining**: starting from facts and working forward to a
conclusion, letting one inferred fact (`cooling_problem`) activate another
rule.

---

## 4. How to use it

### Requirements

- Python 3.9 or newer
- Nothing else — only the standard library.

### Run the interactive program

```bash
cd /Users/omarabbadi/Desktop/AI-project/computer-troubleshooting-expert-system
python3 main.py
```

Then:
1. Choose the machine type (1 = Desktop, 2 = Laptop).
2. Choose your main problem (1–9).
3. Answer each question with `yes` / `no` (or `y` / `n`).
4. Read the diagnosis, reasoning and recommendation.
5. Answer `yes` if you want to see the detailed reasoning trace.

### Run the evaluation cases automatically

```bash
python3 -m evaluation.run_evaluation
```

This runs all 10 (+1) predefined scenarios through the real questionnaire and
engine and prints a table with PASS/FAIL results. The app itself never uses
these cases.

### Try different scenarios to experiment

| Symptom | Choose menu item | Suggest answering |
|---------|------------------|-------------------|
| Machine dead, no lights | Computer does not turn on | No LED, No fans, Cable ok, Outlet ok |
| Black screen but machine runs | Computer turns on but the screen is blank | Runs, Blank, No logo at startup |
| Blue screen at startup | Computer does not boot properly | Runs, Logo appears, Loading appears, Blue screen yes |
| Slow + full disk | Computer is slow | Slow start, Slow programs, Disk full yes, Disk busy yes |
| Hot + shuts down | Computer gets hot or shuts down | Runs, Hot, Shuts down, Fans not spinning |
| No internet but router works | Internet/network is not working | Connected, Reaches router, No internet |

---

## 5. Common questions

**Why is the knowledge base a JSON file and not Python code?**
Because it keeps *what the system knows* separate from *how it reasons*. This
is a core idea in expert systems: you can change the rules without changing
the program, and the same engine could reason about a totally different domain.

**What is working memory?**
A small set that stores the facts collected from you plus the facts inferred
by rules during the session.

**What are "intermediate facts"?**
Facts that are neither your direct answers nor final diagnoses — they are
stepping stones. Example: `cooling_problem` is inferred from your answers and
later used to infer the diagnosis.

**Why can there be several diagnoses at once?**
If several rules fire, the program reports all conclusions it can support. It
never invents probabilities or forces a single answer.

**How does the engine stop?**
It fires rules only while they can produce a new fact. Once no rule can add
anything new, the loop stops (this is called reaching a *fixed point*).

---

---

# دليل المبتدئين — نظام الخبراء لتشخيص أعطال الحاسوب

**ملاحظة:** هذا الدليل موجّه للمطوّرين المبتدئين ولن يفهموا من المشروع أو من
الأنظمة الخبيرة. هو **ليس جزءًا من التسليم الأكاديمي** — الوثائق المقيَّمة موجودة
في مجلد `docs/`.

---

## 1. ما هو هذا المشروع؟

هو **برنامج صغير يعمل من سطر الأوامر** مكتوب بلغة بايثون. تخبره بما هو معطّل في
حاسوبك (مثلًا "الشاشة سوداء")، فيسألك أسئلة **نعم/لا** قليلة، ثم يقترح أسبابًا
محتملة (تشخيصات) مثل "مشكلة في العرض" أو "مشكلة في الطاقة"، مع شرح قصير
وتوصية آمنة.

البرنامج هو **نظام خبير** تقليدي. النظام الخبير هو برنامج يخزّن المعرفة البشرية
(قواعد) في ملف منفصل، ويستخدم "عقلًا" (محرك الاستدلال) للتفكير بناءً على هذه
المعرفة.

### الفكرة الرئيسية: ثلاثة مكوّنات

1. **الحقائق (Facts)** — قطع معلومات صغيرة مثل `screen_blank` (الشاشة فارغة)،
   `fans_not_running` (المراوح لا تدور).
2. **القواعد (Rules)** — "إذا كانت هذه الحقائق صحيحة فإن هذه الحقيقة الجديدة صحيحة".
3. **محرك الاستدلال (Inference Engine)** — حلقة برمجية عامة تطبّق القواعد على
   الحقائق للوصول إلى استنتاجات.

---

## 2. بنية المشروع (ماذا يفعل كل ملف)

```
computer-troubleshooting-expert-system/
├── main.py                 # نقطة البداية. يشغّل الواجهة (القائمة، الأسئلة، النتائج).
├── engine.py               # محرك الاستدلال ("العقل"). عام ولا يحتوي أي منطق تشخيصي.
├── questionnaire.py        # يطرح الأسئلة ذات الصلة ويحوّل الإجابات إلى حقائق.
├── knowledge_base.py       # يقرأ ملفات JSON ويتحقق من سلامتها.
├── models.py               # هياكل بيانات صغيرة: Rule, Question, WorkingMemory.
├── data/
│   ├── knowledge_base.json # جميع قواعد الخبير (المعرفة نفسها).
│   └── questions.json      # القائمة الرئيسية وتعريفات الأسئلة.
├── evaluation/
│   ├── cases.py            # سيناريوهات الاختبار (10 + 1).
│   └── run_evaluation.py   # تشغيل السيناريوهات تلقائيًا.
├── docs/                   # الوثائق الأكاديمية.
└── README.md
```

**نقطة مهمة:** ملف `engine.py` **لا يحتوي أي معرفة** عن الحاسوب. كل المعرفة
("إذا كانت الشاشة فارغة والمراوح تعمل فقد تكون مشكلة عرض") موجودة في
`data/knowledge_base.json`. إذا أردت تعليم النظام شيئًا جديدًا، تعدّل ملف
JSON — ولا تلمس المحرك أبدًا.

---

## 3. كيف يعمل البرنامج (خطوة بخطوة)

```
أنت → الاستبيان → حقائق → محرك الاستدلال → التشخيصات
                              │
                    يقرأ القواعد من
                              │
                     knowledge_base.json
```

1. يعرض البرنامج قائمة: **"ما المشكلة الرئيسية؟"** (9 خيارات).
2. تختار واحدًا، مثلًا "الحاسوب لا يعمل".
3. يسأل **الاستبيان** فقط الأسئلة المتعلقة بهذه المشكلة (4–6 أسئلة، كلٌّ
   بنعم/لا). لا يطرح أسئلة غير ذات صلة.
4. كل إجابة تصبح **حقيقة** في **الذاكرة العاملة** (مثلًا "هل كابل الطاقة موصول
   بإحكام؟" ← نعم ← `power_cable_ok`).
5. ينظر **محرك الاستدلال** إلى الحقائق، ويجد القواعد المُشبَعة الشروط،
   ويُفعِّلها (fires). تفعيل قاعدة يضيف نتيجتها إلى الحقائق، ثم تتكرر العملية
   حتى لا يمكن استنتاج شيء جديد.
6. الحقائق التي تبدأ بـ `diagnosis_` هي **التشخيصات النهائية**، وتُعرض مع
   شرحها وتوصيتها.
7. إذا لم يصل النظام إلى تشخيص، يقول إن الأدلة **غير كافية** ويعرض الاستنتاجات
   الجزئية إن وجدت.
8. يمكنك اختياريًا عرض **أثر التفكير التفصيلي** — كل قاعدة تم تفعيلها بالترتيب.

### مثال توضيحي

اختيار من القائمة: "الحاسوب يسخن أو ينطفئ"

الإجابات:
- هل يعمل الحاسوب ويبقى شغّالًا؟ → **نعم** → `computer_running`
- هل يسخن بشكل غير طبيعي؟ → **نعم** → `computer_hot`
- هل تدور المراوح؟ → **لا** → `fans_not_running`
- هل ينطفئ فجأة؟ → **نعم** → `shuts_down_unexpectedly`

يقوم المحرك الآن بالاستنتاج:
```
القاعدة O1: إذا computer_running و computer_hot و fans_not_running
            فإن cooling_problem                        ← حقيقة وسيطة جديدة
القاعدة O3: إذا cooling_problem و shuts_down_unexpectedly
            فإن diagnosis_overheating                  ← التشخيص النهائي
```

النتيجة:
```
التشخيص المحتمل: مشكلة ارتفاع الحرارة
الشرح:
  - استنتج النظام أولًا وجود مشكلة تبريد، ومع حدوث إيقاف مفاجئ
    يدعم ذلك تشخيص ارتفاع الحرارة.
التوصية:
  - تأكد من عدم انسداد فتحات التهوية ومن عمل مراوح التبريد بشكل طبيعي.
```

هذا هو **الاستدلال التوجيهي الأمامي (Forward Chaining)**: نبدأ من الحقائق
ونتقدّم نحو النتيجة، ونجعل حقيقة مستنتَجة (`cooling_problem`) تُفعّل قاعدة أخرى.

---

## 4. كيفية الاستخدام

### المتطلبات

- بايثون 3.9 أو أحدث
- لا شيء آخر — فقط المكتبة القياسية.

### تشغيل البرنامج التفاعلي

```bash
cd /Users/omarabbadi/Desktop/AI-project/computer-troubleshooting-expert-system
python3 main.py
```

ثم:
1. اختر نوع الحاسوب (1 = حاسوب مكتبي، 2 = حاسوب محمول).
2. اختر مشكلتك الرئيسية (1–9).
3. أجب عن كل سؤال بـ `yes` / `no` (أو `y` / `n`).
4. اقرأ التشخيص والشرح والتوصية.
5. أجب بـ `yes` إذا أردت رؤية أثر التفكير التفصيلي.

### تشغيل حالات الاختبار تلقائيًا

```bash
python3 -m evaluation.run_evaluation
```

يُشغّل هذا السيناريوهات العشرة (+1) من خلال الاستبيان والمحرك الحقيقيين
ويطبع جدولًا بنتائج PASS/FAIL. لا يستخدم التطبيق نفسه هذه الحالات أبدًا.

### جرّب سيناريوهات مختلفة للتجربة

| العرض | اختر من القائمة | إجابات مقترحة |
|-------|-----------------|---------------|
| الحاسوب ميت ولا توجد أضواء | الحاسوب لا يعمل | لا LED، لا مراوح، الكابل جيد، المقبس جيد |
| شاشة سوداء لكن الجهاز يعمل | يعمل لكن الشاشة فارغة | يعمل، شاشة فارغة، لا شعار عند الإقلاع |
| شاشة زرقاء عند الإقلاع | لا يقلع بشكل صحيح | يعمل، الشعار يظهر، شاشة التحميل تظهر، شاشة زرقاء نعم |
| بطيء والقرص ممتلئ | الحاسوب بطيء | إقلاع بطيء، برامج بطيئة، قرص ممتلئ، قرص مشغول نعم |
| يسخن وينطفئ | يسخن أو ينطفئ | يعمل، حار، ينطفئ، المراوح لا تدور |
| لا إنترنت مع أن الراوتر يعمل | الإنترنت لا يعمل | متصل، يصل للراوتر، لا إنترنت |

---

## 5. أسئلة شائعة

**لماذا قاعدة المعرفة ملف JSON وليست كود بايثون؟**
لأن ذلك يفصل *ما يعرفه النظام* عن *كيف يفكّر*. هذه فكرة أساسية في الأنظمة
الخبيرة: يمكنك تغيير القواعد دون تغيير البرنامج، ويمكن للمحرك نفسه أن يفكّر
في مجال مختلف تمامًا.

**ما هي الذاكرة العاملة؟**
مجموعة صغيرة تخزّن الحقائق التي جمعت منك، بالإضافة إلى الحقائق التي استنتجها
المحرك أثناء الجلسة.

**ما هي الحقائق الوسيطة؟**
حقائق ليست إجابات مباشرة ولا تشخيصات نهائية، بل خطوات وسيطة. مثال: `cooling_problem`
مستنتَجة من إجاباتك ثم تُستخدم لاستنتاج التشخيص.

**لماذا قد تظهر عدة تشخيصات في وقت واحد؟**
إذا تفعّلت عدة قواعد، يعرض البرنامج كل الاستنتاجات التي يمكن دعمها. لا يخترع
احتمالات ولا يفرض إجابة واحدة.

**كيف يتوقف المحرك؟**
يُفعّل القواعد فقط ما دامت قادرة على إنتاج حقيقة جديدة. عندما لا تستطيع أي
قاعدة إضافة شيء جديد، تتوقف الحلقة (يُسمّى هذا الوصول إلى "نقطة ثابتة").
