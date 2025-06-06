#include "pattern_skipper.h"
#include <algorithm>

PatternSkipper g_patternSkipper; // global instance
int g_forceCPUThreads = 1;      // 0 = auto

PatternSkipper::PatternSkipper() {
    limits.fill(0);
    // افتراضى: لا حد (يعنى 0 = تعطيل القاعدة)
}

void PatternSkipper::setLimit(int patternLen, int limit) {
    if (patternLen >= 1 && patternLen <= 5) {
        limits[patternLen] = limit;
    }
}

void PatternSkipper::setLimits(const std::array<int, 6>& lim) {
    limits = lim;
}

static bool exceedsRepeat(const std::string& hex, int patLen, int maxRepeat) {
    if (maxRepeat <= 0) return false; // no rule
    int consec = 1;

    for (size_t i = 0; i + patLen < hex.size(); i += patLen) {
        if (hex.compare(i, patLen, hex, i + patLen, patLen) == 0) {
            consec++;
            if (consec > maxRepeat) return true;
        } else {
            consec = 1;
        }
    }
    return false;
}

bool PatternSkipper::isInvalid(const Int& key) const {
    // Int::GetBase16() is non-const; cast away constness for read-only call
    std::string hex = const_cast<Int&>(key).GetBase16();
    for (int len = 1; len <= 5; ++len) {
        if (limits[len] > 0 && exceedsRepeat(hex, len, limits[len]))
            return true;
    }
    return false;
}

bool PatternSkipper::skipInvalid(Int& key) const {
    bool changed = false;
    while (isInvalid(key)) {
        key.AddOne();
        changed = true;
    }
    return changed;
}
