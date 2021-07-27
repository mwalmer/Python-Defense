#pragma once

#ifdef SPEED_EXPORTS
#define SPEED_API __declspec(dllexport)
#else
#define SPEED_API __declspec(dllimport)
#endif

extern "C" SPEED_API bool modulo_zero(int num, int divisor);

extern "C" SPEED_API void motion(double change_x, double change_y, double& self_x, double& self_y, double scale, double projectile_speed);