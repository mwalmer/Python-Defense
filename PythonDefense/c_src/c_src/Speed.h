#pragma once

#ifdef SPEED_EXPORTS
#define SPEED_API __declspec(dllexport)
#else
#define SPEED_API __declspec(dllimport)
#endif

extern "C" SPEED_API bool modulo_zero(int num, int divisor);