# 1. مقدمة عامة عن المشروع

الهدف في المشروع ده إننا نبني وكيل ذكي (Intelligent Agent) يقدر يتعلّم لوحده إزاي يلعب لعبة Flappy Bird من غير ما نبرمجه بالقواعد بشكل مباشر. احنا بنستخدم خوارزمية جينية (Genetic Algorithm) بنسختها المطوّرة اللي اسمها NEAT، واللي بتساعدنا نطوّر الشبكات العصبية ونعدّل في تركيبها (Topology) أثناء عملية التطوّر.

## فكرة اللعبة باختصار

لعبة Flappy Bird لعبة بسيطة، فيها اللاعب بيتحكّم في طائر صغير لازم يعدّي من بين أنابيب من غير ما يخبط فيها أو في الأرض.

*   كل مرة يعدّي أنبوبة بنجاح، بيكسب نقطة.
*   اللعبة بتنتهي لو الطائر خبط في أنبوبة أو الأرض أو خرج برا حدود الشاشة.

## فكرة الذكاء الاصطناعي في المشروع

الوكيل الذكي (AI Agent) هيجرّب يلعب اللعبة مرّات كتير.

*   في كل جيل (Generation)، عندنا مجموعة شبكات عصبية (Population) بيتطوّروا عن طريق الطفرات (Mutations) والتزاوج (Crossover) على أساس أفضل الأفراد في الجيل اللي فات.
*   الهدف إن أداء الوكيل يتحسّن (عدد الأنابيب اللي بيعدّيها) مع مرور الأجيال لحد ما يوصل لأداء ممتاز أو حتى مثالي.

---

# 2. مفهوم PEAS

"**PEAS**" اختصار لأربع عناصر بتعرّف مكوّنات تصميم أي وكيل (Agent) في مجال الذكاء الاصطناعي:

## 1. Performance Measure (مقياس الأداء)

إزاي بنقيس أداء الوكيل؟

في Flappy Bird، المقياس الأساسي هو عدد الأنابيب اللي الوكيل بيعدّيها قبل ما يخبط أو يخرج برا الشاشة.

ممكن نضيف مقاييس تانية زي مدة بقاء الطائر من غير ما يخسر، بس غالبًا العدد النهائي للأنابيب هو الأهم.

## 2. Environment (البيئة)

البيئة هي العالم اللي الوكيل شغال فيه.

في حالتنا دي لعبة Flappy Bird: شاشة، أنابيب بتتحرّك، الجاذبية بتشدّ الطائر لتحت، إلخ.

البيئة بتتحدّث مع الوقت (الأنابيب بتتحرك، الطائر بيقع بفعل الجاذبية).

## 3. Actuators (الأفعال)

دي الحركات أو الأوامر اللي الوكيل بيعملها عشان يأثر على البيئة.

في Flappy Bird، الفعل الأساسي هو إن الطائر يقفز (Jump/Flap). وفيه فعل ضمني إن الطائر ما يقفزش (يكمل سقوط).

## 4. Sensors (المستشعرات)

المعلومات اللي الوكيل بياخدها من البيئة.

في Flappy Bird، أهم حاجة: موقع الطائر (Y)، مكان أقرب أنبوبة (الفتحة العلوية والسفلية)، والمسافة الأفقية للأنبوبة اللي جاية.

المعلومات دي بتتبعَت للشبكة العصبية عشان تحدد إذا كان الطائر يقفز ولا لأ.

---

# 3. خصائص البيئة (ODESDA)

"**ODESDA**" بتوصف طبيعة البيئة اللي الوكيل الذكي بيتعامل معاها:

## 1. O: Observable (ملاحظ بالكامل) أو Partially Observable (ملاحظ جزئيًا)

هل الوكيل شايف كل حاجة في البيئة ولا لأ؟

ممكن ندي الوكيل معظم المعلومات المهمة (زي موقع الطائر والأنابيب)، فلو وفّرنا كل اللي يلزم للعب تبقى البيئة شبه ملاحظَة بالكامل.

## 2. D: Deterministic (حتمية) أو Stochastic (احتمالية)

هل نفس الأفعال بتدي نفس النتايج دايمًا ولا فيه عشوائية؟

Flappy Bird غالبًا حتمية لو كل الظروف ثابتة، بس ممكن تبقى احتمالية لو أماكن الأنابيب بتتغيّر بشكل عشوائي.

## 3. E: Episodic (حلقات) أو Sequential (تتابعية)

Episodic يعني كل حلقة مستقلة عن التانية، وSequential يعني القرارات بتأثر في بعض.

اللعبة تعتبر Episodic على مستوى كل محاولة (بتبدأ وتنتهي)، لكن جوا الحلقة الواحدة القرارات مرتبطة ببعض.

## 4. S: Static (ساكنة) أو Dynamic (ديناميكية)

البيئة الديناميكية بتتغير أثناء ما الوكيل بياخد قراراته.

Flappy Bird بيئتها ديناميكية عشان الأنابيب بتتحرك والطائر بيقع بالجاذبية.

## 5. D: Discrete (منفصلة) أو Continuous (مستمرة)

هل حالات البيئة وأفعال الوكيل محدودة ولا متصلة؟

الأفعال في Flappy Bird منفصلة (قفزة أو لأ)، بس الإحداثيات ممكن تتعامل كقيم مستمرة.

## 6. A: Single agent (وكيل واحد) أو Multi-agent (متعدد الوكلاء)

عندنا وكيل واحد بس (الطائر)، فبالتالي Single Agent.

## باختصار:

*   **Observability**: شبه كاملة.
*   **Deterministic/Stochastic**: شبه حتمية مع شوية عشوائية في ترتيب الأنابيب.
*   **Episodic/Sequential**: حلقات متعددة وكل حلقة فيها تتابع قرارات.
*   **Static/Dynamic**: البيئة ديناميكية.
*   **Discrete/Continuous**: الفعل منفصل (قفزة/لا)، بس الحالة شبه مستمرة.
*   **Single/Multi-agent**: وكيل واحد.

---

# 4. آليّة عمل خوارزميّة NEAT

**NEAT** اختصار لـ **NeuroEvolution of Augmenting Topologies**، وهي خوارزمية جينية (Genetic Algorithm) مخصصة لتطوير الشبكات العصبية. مش بس بتطوّر أوزان الوصلات بين الخلايا العصبية، لكن كمان بتطوّر هيكل الشبكة نفسها (عدد الخلايا وعدد الوصلات) عن طريق الطفرات.

## المراحل الأساسية في NEAT

### 1. التهيئة (Initialization)

بننشئ مجموعة أفراد (Population)، هنا مثلًا الحجم بتاعنا (`pop_size`) = 50 شبكة عصبية في كل جيل.

كل شبكة بتبدأ بتركيب بسيط (مثلاً عدد محدود من الوصلات) و`initial_connection` في الإعدادات هنا = "full"، يعني في البداية كل المدخلات متوصلة بالمخرجات.

### 2. التقييم (Evaluation)

بنختبر كل شبكة (فرد) في لعبة Flappy Bird عشان نعرف أدائها (**Fitness**).

الـ**Fitness** بيتحسب بناءً على عدد الأنابيب اللي الطائر عدّاها، ولو الشبكة وصلت لمستوى معين (`fitness_threshold` = 100) ممكن نعتبر إننا حققنا الهدف.

### 3. الانتقاء (Selection)

بنختار أحسن الشبكات على أساس الـ**Fitness** عشان نستخدمها في الجيل الجديد.

في الإعدادات فيه حاجات زي (`elitism`=2) و(`survival_threshold`=0.2) بتحدد إزاي بنختار أفضل الأفراد.

### 4. التزاوج (Crossover)

بنخلط جينات شبكتين (أبوين) عشان نطلع شبكة جديدة (ابن) تجمع صفاتهم.

وده بيحصل بعد الانتقاء عشان ننتج الجيل الجديد.

### 5. الطفرة (Mutation)

بنضيف تغييرات عشوائية على الأوزان أو بنية الشبكة، زي (`conn_add_prob`=0.5) و(`conn_delete_prob`=0.5) اللي بتحدد احتمالية إضافة أو حذف وصلات.

فيه كمان (`node_add_prob`=0.2) و(`node_delete_prob`=0.2) عشان نتحكم في إضافة/حذف الخلايا العصبية.

كمان بنعدل في الأوزان نفسها (`weight_mutate_rate`=0.8) وبنسبة (`weight_replace_rate`=0.1) ممكن نستبدل الوزن بالكامل.

### 6. التخصّص (Speciation)

بنقسم الأفراد لمجموعات فرعية (**Species**) عشان نحافظ على التنوع ومايبقاش فيه سلالة واحدة بس مهيمنة.

(`compatibility_threshold`=3.0) بتحدد الحد اللي بنقرر عنده إن الشبكات قريبة لبعض أو مختلفة.

### 7. تكرار العملية

بنرجع نعمل تقييم للجيل الجديد، ثم انتقاء وتزاوج وطفرة... لحد ما نوصل لأداء كويس أو نوصل لعدد أجيال معين.

(`max_stagnation`=20) مثلًا بيخلينا نوقف لو الجيل مايتحسّنش لفترة طويلة.

---

# 5. أهم إعدادات ملف الـConfig 

*   `fitness_criterion = max`: **مقياس اللياقة**: بنعتمد على أعلى لياقة (أعلى أداء).
*   `fitness_threshold = 100`: **حد اللياقة**: لو وصلنا للـFitness دي أو أكتر، يبقى الوكيل حقق المطلوب.
*   `pop_size = 50`: **حجم المجتمع**: عدد الشبكات في كل جيل.
*   `activation_default = tanh`: **دالة التنشيط الافتراضية**: الدوال اللي بتفعّل الخلايا العصبية هي tanh في الوضع الافتراضي.
*   `bias_mutate_rate = 0.7`, `weight_mutate_rate = 0.8`: **معدل طفرة الانحياز والوزن**: نسب الطفرة في الـbias والأوزان.
*   `conn_add_prob = 0.5`, `conn_delete_prob = 0.5`: **احتمالية إضافة/حذف وصلة**: احتمالية إضافة أو حذف وصلات.
*   `node_add_prob = 0.2`, `node_delete_prob = 0.2`: **احتمالية إضافة/حذف خلية عصبية**: احتمالية إضافة أو حذف خلايا عصبية.
*   `compatibility_threshold = 3.0`: **حد التوافق**: الحد اللي بنقسّم على أساسه الأنواع (Speciation).
*   `elitism = 2`: **النخبوية**: عدد الأفراد اللي بنحتفظ بيهم من كل نوع (Species) من غير تغييرات.
*   `survival_threshold = 0.2`: **حد البقاء**: نسبة الأفراد اللي بنخليها تعيش من كل نوع.

---

# 6. الخاتمة

باستخدام خوارزمية NEAT مع لعبة Flappy Bird، هنقدر نشوف إزاي نعمل وكيل ذكي بيتعلم بنفسه من خلال التجارب المتكررة، وبيطوّر تركيب الشبكة العصبية بتاعته بشكل شبه التطوّر الطبيعي. مفهوم PEAS بيوضح لنا إزاي نحدد مقياس الأداء والبيئة والمستشعرات والأفعال، وODESDA بيشرح طبيعة البيئة وتأثيرها على الوكيل وطريقة تعلّمه.

أما ملف الـConfig فبيخلينا نتحكم في كل التفاصيل زي حجم المجتمع (Population) ونسب الطفرة والتزاوج وحدود التوافق بين الشبكات (Speciation). المشروع ده مثال عملي لطيف بيربط مبادئ الذكاء الاصطناعي (التعلم التطوري والشبكات العصبية) بلعبة بسيطة، وبيسهل علينا نفهم إزاي الخوارزميات دي بتشتغل في بيئة تفاعلية.
