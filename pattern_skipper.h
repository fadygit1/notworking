#ifndef PATTERN_SKIPPER_H
#define PATTERN_SKIPPER_H

#include "Int.h"
#include <array>

// أداة بسيطة للتحقق من تكرار الأنماط (القاعدة 1-5) وتخطّى المفاتيح غير الصالحة.
// الخوارزمية الحالية تتحقق فقط من التكرارات وتزيد المفتاح بـ1 حتى يصبح صالحًا.
// يمكن تحسينها لاحقًا بتنفيذ قفز ذكّى كما هو موصوف فى المناقشات.
class PatternSkipper {
public:
    PatternSkipper();
    // حدّ التكرار لكل طول نمط 1-5. مثلاً limits[1] = أقصى تكرار مفرد، limits[3] = أقصى تكرار ثلاثى.
    void setLimit(int patternLen, int limit);
    void setLimits(const std::array<int, 6>& lim);

    // true إذا كان المفتاح يخرق أى قاعدة
    bool isInvalid(const Int& key) const;

    // يعدّل المفتاح ليصبح صالحًا (قد يعدّل عدّة مرات). يرجع true إذا غيّر شيئًا.
    bool skipInvalid(Int& key) const;

private:
    std::array<int, 6> limits; // index 1..5
};

extern PatternSkipper g_patternSkipper;
extern int g_forceCPUThreads;

#endif // PATTERN_SKIPPER_H
