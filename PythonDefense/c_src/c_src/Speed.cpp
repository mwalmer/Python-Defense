#include "pch.h"
#include "Speed.h"
#include <math.h>

bool modulo_zero(int num, int divisor)
{
    return (num % divisor) == 0;
}

void motion(double change_x, double change_y, double& self_x, double& self_y, double scale, double projectile_speed)
{
    double x_y_components[2] = { change_x - self_x, change_y - self_y };
    if (x_y_components[0] == 0)
    {
        x_y_components[0] = .0000001;
    }
    double x_y_directions[2];
    x_y_directions[0] = cos(atan2(x_y_components[1], x_y_components[0]));
    x_y_directions[1] = sin(atan2(x_y_components[1], x_y_components[0]));

    self_x = self_x + x_y_directions[0] * scale * projectile_speed;
    self_y = self_y + x_y_directions[1] * scale * projectile_speed;
}

void arc_motion(double change_x, double change_y, double& self_x, double& self_y, double scale, double projectile_speed)
{
    double x_y_components[2] = { change_x - self_x, change_y - self_y };
    if (x_y_components[0] == 0)
    {
        x_y_components[0] = .0000001;
    }
    double x_y_directions[2];
    x_y_directions[0] = cos(atan2(x_y_components[1], x_y_components[0]));
    x_y_directions[1] = sin(atan2(x_y_components[1], x_y_components[0]));

    self_x = self_x + x_y_directions[0] * scale * projectile_speed + x_y_directions[1] * scale;
    self_y = self_y + x_y_directions[1] * scale * projectile_speed + x_y_directions[0] * scale;
}

void snake_shot(double change_x, double change_y, double& self_x, double& self_y, double scale, double projectile_speed, double self_sinval)
{
    double x_y_components[2] = { change_x - self_x, change_y - self_y };
    if (x_y_components[0] == 0)
    {
        x_y_components[0] = .0000001;
    }
    double x_y_directions[2];
    x_y_directions[0] = cos(atan2(x_y_components[1], x_y_components[0]));
    x_y_directions[1] = sin(atan2(x_y_components[1], x_y_components[0]));

    self_x = self_x + x_y_directions[0] * scale * projectile_speed * fabs(sin(self_sinval));
    self_y = self_y + x_y_directions[1] * scale * projectile_speed * fabs(cos(self_sinval));

}



void around_shot(double& self_x, double& self_y, double scale_x, double scale_y, int self_flip, double self_radians)
{
    if (self_flip < 1)
    {
        self_x = self_x + scale_x;
        self_y = self_y + scale_y;
    }
    else
    {
        self_x = self_x + cos(self_radians) * 25;
        self_y = self_y + sin(self_radians) * 25;
    }
}