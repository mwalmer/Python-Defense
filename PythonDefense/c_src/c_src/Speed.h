#pragma once

#ifdef SPEED_EXPORTS
#define SPEED_API __declspec(dllexport)
#else
#define SPEED_API __declspec(dllimport)
#endif

extern "C" SPEED_API bool modulo_zero(int num, int divisor);

extern "C" SPEED_API void motion(double change_x, double change_y, double& self_x, double& self_y, double scale, double projectile_speed);

extern "C" SPEED_API void arc_motion(double change_x, double change_y, double& self_x, double& self_y, double scale, double projectile_speed);

extern "C" SPEED_API void snake_shot(double change_x, double change_y, double& self_x, double& self_y, double scale, double projectile_speed, double self_sinval);

extern "C" SPEED_API void around_shot(double& self_x, double& self_y, double scale_x, double scale_y, int self_flip, double self_radians);