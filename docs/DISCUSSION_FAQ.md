# Discussion FAQ — Expert System Project (English + Arabic)

Prepared answers for the most common questions a student may be asked during
the project discussion / oral presentation. Each entry has the question, a
short answer you can say out loud, and (where useful) a pointer to the code.

---

## English section

### Q1. What is an expert system?

An expert system is a computer program that imitates the decision-making
ability of a human expert. It stores human knowledge as rules and uses an
inference engine to reason over those rules. It has three main parts:
a knowledge base, working memory, and an inference engine.

### Q2. What is a fact in this project?

A fact is one small piece of information stored in working memory. It is
either given by the user (for example `screen_blank`) or inferred by a rule
(for example `cooling_problem`). Facts are just strings with a consistent
vocabulary, and they can be checked as rule conditions.

### Q3. Where is the knowledge base?

In the file `data/knowledge_base.json`. It contains all 34 IF-THEN rules,
the diagnosis names, explanations and recommendations. It is data, not code.

### Q4. What is a rule?

A rule is an IF-THEN statement. It has conditions (a list of facts that must
be present) and conclusions (facts that become true when the conditions are
satisfied). Example: `IF cooling_problem AND shuts_down_unexpectedly
THEN diagnosis_overheating`. Each rule also has a human-readable explanation
and an optional recommendation.

### Q5. Where is the inference engine?

In `engine.py` — the `InferenceEngine` class. It is completely generic: it
understands concepts like conditions and conclusions, but it
contains no computer-troubleshooting logic. All domain knowledge is injected
into it as `Rule` objects loaded from JSON.

### Q6. Why forward chaining?

Because we start from known facts (the user's symptoms) and work toward a
conclusion. That is data-driven reasoning: given the evidence, what can we
conclude? Forward chaining fits this exactly, and it also produces a natural
explanation chain (facts → intermediate fact → diagnosis) that is easy to show.

### Q7. How can one inferred fact activate another rule?

After a rule fires, its conclusions are added to working memory. In the next
cycle the engine re-checks every rule, so a newly added fact can make another
rule's conditions true. Example: rule O1 infers `cooling_problem`, and that
fact is what makes rule O3 applicable. That is multi-step forward chaining.

### Q8. How are simultaneously applicable rules handled?

The engine gathers all applicable rules and fires them in a deterministic
order (sorted by rule ID), so the result is the same on every run. This is a
simple, predictable strategy — no numeric priorities are used. Since
conclusions are only added, never removed, the firing order does not change
the final answer; it only affects the order of the explanation lines.

### Q9. Why is the knowledge base separate from the program logic?

So that domain knowledge and the mechanism that reasons over it are
independent. You can change or extend the rules without touching the code,
and the same engine could be reused for another domain. This separation is a
core academic requirement of expert-system design.

### Q10. How does the system explain its conclusion?

Every rule carries a plain-language `explanation`. When a diagnosis is
produced, the program shows the explanation of the rule(s) that reached it,
plus a recommendation.

### Q11. How does the engine avoid infinite loops?

A rule is only fired when it can add a fact that is not already present. Once
its conclusions exist in working memory, the same rule can never fire again.
Facts are only added, never removed, so the process must stop — it reaches a
fixed point where no rule can produce anything new.

### Q12. What is working memory?

The runtime state of a session. It stores the current set of facts and the
ordered list of fired rules used to build the explanation. It exists only
during a session and is represented by the `WorkingMemory` class.

### Q13. Why only Yes/No questions?

To keep the questionnaire simple and the facts unambiguous. Each answer maps
directly to one fact (Yes → fact A, No → fact B). It is easier to explain and
still enough to demonstrate the inference process.

### Q14. Why does the system sometimes give more than one diagnosis?

Because forward chaining fires every rule that is applicable. If several
conclusions are supported by the evidence, all of them are reported. The
project deliberately avoids inventing confidence percentages or forcing a
single answer.

### Q15. What happens when there is not enough evidence?

If no rule reaches a `diagnosis_*` fact, the program says that no conclusion
could be drawn from the answers given. This is the same "no solution" case a
simple expert system produces when the evidence cannot satisfy any diagnosis
rule.

### Q16. Why does it give broad diagnoses instead of the exact broken part?

The project scope is deliberately broad. Diagnosing the exact failed
component (e.g., "the motherboard capacitor is damaged") would require many
more rules, precise measurements, and risky assumptions. A broad category
like "Power problem" is safer, simpler, and still useful.

### Q17. How many rules are there and how are they organized?

34 rules. They are distributed across the nine problem areas (power, display,
boot/OS, performance, overheating, network, storage, memory, peripherals).
About half infer intermediate facts and the rest turn evidence into final
diagnoses, so several diagnoses require two or three inference steps.

### Q18. What determines the order in which rules fire?

Applicable rules are sorted by rule ID, which makes the firing order fully
deterministic — the same answers always produce the same session. Since facts
are only added and never retracted, this order does not affect which
diagnoses are reached, only the sequence of explanation lines.

### Q19. Why Python with only the standard library?

The assignment requires plain Python and forbids frameworks and unnecessary
dependencies. The standard library is enough because the project needs only
JSON loading, simple data structures, and command-line input/output.

### Q20. How was the system tested?

After freezing the rules and behavior, ten evaluation cases were defined
covering all nine areas plus a multiple-diagnosis case. They are stored in
`evaluation/cases.py` and run through the real questionnaire and engine with
`python3 -m evaluation.run_evaluation`. The application itself does not know
about these cases. There is also an extra case for insufficient evidence.

### Q21. What are the limitations of the system?

The diagnoses are broad rather than component-exact; questions are fixed and
Yes/No only; the rule set is static and not learned; there are no
probabilities or confidence scores; recommendations are generic; and the
knowledge base is relatively small compared to real diagnostic software.

### Q22. What would you improve in the future?

Add more rules and finer-grained diagnoses; allow dynamic question selection
based on previous answers; support multiple answers per question; add
probabilities or certainty factors; and optionally build a small GUI.

---

## القسم العربي

### س1: ما هو النظام الخبير؟

النظام الخبير هو برنامج يحاكي طريقة اتخاذ القرار عند الخبير البشري. يخزّن
المعرفة البشرية على شكل قواعد، ويستخدم محرك استدلال للتفكير بناءً على هذه
القواعد. يتكوّن من ثلاثة أجزاء رئيسية: قاعدة المعرفة، والذاكرة العاملة،
ومحرك الاستدلال.

### س2: ما هي الحقيقة (Fact) في هذا المشروع؟

الحقيقة هي قطعة صغيرة من المعلومات تُخزَّن في الذاكرة العاملة. تكون إمّا
مقدَّمة من المستخدم (مثل `screen_blank` أي الشاشة فارغة) أو مستنتَجة من
قاعدة (مثل `cooling_problem` أي وجود مشكلة تبريد). الحقائق مجرد نصوص
بمفردات موحّدة، وتُفحص كشروط للقواعد.

### س3: أين توجد قاعدة المعرفة؟

في الملف `data/knowledge_base.json`. يحتوي على جميع القواعد الـ34 من نوع
"إذا-فإن"، وأسماء التشخيصات، والشروح، والتوصيات. هي بيانات وليست كودًا.

### س4: ما هي القاعدة؟

القاعدة عبارة عن جملة "إذا-فإن". لها شروط (قائمة حقائق يجب أن تكون موجودة)
واستنتاجات (حقائق تصبح صحيحة عندما تتحقق الشروط). مثال: `إذا cooling_problem
و shuts_down_unexpectedly فإن diagnosis_overheating`. لكل قاعدة أيضًا شرح
مفهوم وتوصية اختيارية.

### س5: أين يوجد محرك الاستدلال؟

في `engine.py` — داخل كلاس `InferenceEngine`. وهو محرك عام تمامًا: يفهم
مفاهيم مثل الشروط والاستنتاجات، لكنه لا يحتوي أي منطق لتشخيص
الأعطال. كل المعرفة تُحقن فيه ككائنات `Rule` محمّلة من ملف JSON.

### س6: لماذا الاستدلال الأمامي (Forward Chaining)؟

لأننا نبدأ من حقائق معلومة (أعراض المستخدم) ونتقدّم نحو نتيجة. هذا تفكير
موجّه بالبيانات: بالنظر إلى الأدلة، ماذا يمكننا أن نستنتج؟ الاستدلال الأمامي
يناسب ذلك تمامًا، وينتج أيضًا سلسلة شرح طبيعية (حقائق ← حقيقة وسيطة ← تشخيص)
يسهل عرضها.

### س7: كيف يمكن لحقيقة مستنتَجة أن تفعّل قاعدة أخرى؟

بعد تفعيل قاعدة، تُضاف استنتاجاتها إلى الذاكرة العاملة. في الدورة التالية
يعيد المحرك فحص كل القواعد، فيمكن لحقيقة جديدة أن تجعل شروط قاعدة أخرى
متحققة. مثال: القاعدة O1 تستنتج `cooling_problem`، وهذه الحقيقة هي ما
يجعل القاعدة O3 قابلة للتفعيل. هذا هو الاستدلال الأمامي متعدد الخطوات.

### س8: كيف تُعالج القواعد القابلة للتفعيل معًا؟

يجمع المحرك كل القواعد القابلة للتفعيل وينفّذها بترتيب حتمي (مفرَّزة حسب
معرّف القاعدة)، فتكون النتيجة نفسها في كل تشغيل. هذه استراتيجية بسيطة
ومتوقعة — لا تُستخدم أولويات رقمية. وبما أن الاستنتاجات تُضاف فقط ولا
تُحذف، فإن الترتيب لا يغيّر الإجابة النهائية — بل يحدد فقط ترتيب سطور
الشرح.

### س9: لماذا فصل قاعدة المعرفة عن منطق البرنامج؟

لكي تكون المعرفة والآلية التي تفكّر بها مستقلتين. يمكنك تعديل أو توسيع
القواعد دون لمس الكود، ويمكن إعادة استخدام المحرك نفسه في مجال آخر.
هذا الفصل مطلب أكاديمي أساسي في تصميم الأنظمة الخبيرة.

### س10: كيف يشرح النظام نتيجته؟

تحمل كل قاعدة حقل `explanation` بلغة بسيطة. عندما يُنتج تشخيص، يعرض
البرنامج شرح القاعدة (أو القواعد) التي وصلت إليه، مع توصية.

### س11: كيف يتجنب المحرك الحلقات اللانهائية؟

لا تُفعَّل القاعدة إلا إذا أمكنها إضافة حقيقة غير موجودة. بمجرد وجود
استنتاجاتها في الذاكرة العاملة لا يمكن أن تُفعَّل مرة أخرى. الحقائق تُضاف
فقط ولا تُحذف، لذلك لا بدّ أن تتوقف العملية — تصل إلى "نقطة ثابتة" لا
تستطيع فيها أي قاعدة إنتاج شيء جديد.

### س12: ما هي الذاكرة العاملة؟

هي الحالة الزمنية للجلسة. تخزّن مجموعة الحقائق الحالية، وقائمة القواعد
المُفعَّلة بالترتيب (لأجل بناء الشرح). توجد فقط أثناء الجلسة ويمثلها كلاس
`WorkingMemory`.

### س13: لماذا أسئلة نعم/لا فقط؟

لإبقاء الاستبيان بسيطًا والحقائق غير ملتبسة. كل إجابة تُعطي حقيقة واحدة مباشرة
(نعم ← حقيقة أ، لا ← حقيقة ب). هذا أسهل في الشرح ويكفي لإظهار عملية الاستدلال.

### س14: لماذا يعطي النظام أحيانًا أكثر من تشخيص واحد؟

لأن الاستدلال الأمامي يفعّل كل قاعدة قابلة للتفعيل. إذا كانت الأدلة تدعم عدة
استنتاجات، تُعرض جميعها. المشروع يتجنب عمدًا اختراع نسب مئوية أو فرض إجابة
واحدة.

### س15: ماذا يحدث عندما لا تكفي الأدلة؟

إذا لم تصل أي قاعدة إلى حقيقة من نوع `diagnosis_*`، يقول البرنامج إنه لا يمكن
استخلاص أي استنتاج من الإجابات المعطاة. هذه هي نفس حالة "لا يوجد حل"
(no solution) التي يعرضها النظام الخبير البسيط عندما لا تتحقق أي قاعدة
تشخيص.

### س16: لماذا تشخيصات عامة بدلًا من تحديد الجزء المعطوب بدقة؟

نطاق المشروع عام عمدًا. تشخيص الجزء المعطوب بدقة (مثل "المكثف في اللوحة الأم
تالف") يتطلب عددًا أكبر بكثير من القواعد وقياسات دقيقة وافتراضات محفوفة
بالمخاطر. تشخيص عام مثل "مشكلة طاقة" أكثر أمانًا وبساطة وما زال مفيدًا.

### س17: كم عدد القواعد وكيف هي منظّمة؟

34 قاعدة، موزعة على مجالات المشاكل التسعة (الطاقة، العرض، الإقلاع/نظام التشغيل،
الأداء، ارتفاع الحرارة، الشبكة، التخزين، الذاكرة، الأجهزة الطرفية). نحو نصفها
يستنتج حقائق وسيطة والباقي يحوّل الأدلة إلى تشخيصات نهائية، لذلك تتطلب عدة
تشخيصات خطوتين أو ثلاث خطوات استدلال.

### س18: ما الذي يحدد ترتيب تفعيل القواعد؟

تُفرز القواعد القابلة للتفعيل حسب معرّف القاعدة، فيكون ترتيب التفعيل
حتميًا تمامًا — نفس الإجابات تُنتج دائمًا نفس الجلسة. وبما أن الحقائق
تُضاف فقط ولا تُحذف، فإن هذا الترتيب لا يؤثر على التشخيصات الناتجة، بل
يحدد فقط تسلسل سطور الشرح.

### س19: لماذا بايثون مع المكتبة القياسية فقط؟

لأن المطلوب من التكليف هو بايثون خالص، مع منع الأطر البرمجية والاعتماديات غير
الضرورية. المكتبة القياسية كافية لأن المشروع يحتاج فقط تحميل JSON وهياكل
بيانات بسيطة وإدخال/إخراج من سطر الأوامر.

### س20: كيف تم اختبار النظام؟

بعد تثبيت القواعد والسلوك، حُدّدت عشر حالات تقييم تغطي المجالات التسعة
بالإضافة إلى حالة تشخيصات متعددة. تُخزَّن في `evaluation/cases.py` وتُشغَّل
عبر الاستبيان والمحرك الحقيقيين بالأمر
`python3 -m evaluation.run_evaluation`. التطبيق نفسه لا يعرف هذه الحالات.
يوجد أيضًا حالة إضافية للأدلة غير الكافية.

### س21: ما حدود النظام؟

التشخيصات عامة وليست دقيقة على مستوى المكوّنات؛ الأسئلة ثابتة وبصيغة نعم/لا
فقط؛ مجموعة القواعد ثابتة وغير قابلة للتعلم؛ لا توجد احتمالات أو درجات ثقة؛
التوصيات عامة؛ وقاعدة المعرفة صغيرة نسبيًا مقارنة ببرامج التشخيص الحقيقية.

### س22: ما التحسينات المقترحة مستقبلًا؟

إضافة المزيد من القواعد وتشخيصات أدق؛ السماح باختيار الأسئلة ديناميكيًا بناءً
على الإجابات السابقة؛ دعم أكثر من إجابة للسؤال الواحد؛ إضافة احتمالات أو
معاملات ثقة؛ وبناء واجهة رسومية صغيرة اختياريًا.
