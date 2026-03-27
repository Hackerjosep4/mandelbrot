// mandelbrot.cpp
#include <complex>
#include <cstdint>
#include <vector>

#ifdef _WIN32
  #define EXPORT extern "C" __declspec(dllexport)
#else
  #define EXPORT extern "C"
#endif

int mandelbrot_iter(double a, double b, int max_iter)
{
    std::complex<double> c(a, b);
    std::complex<double> z(0, 0);

    int n = 0;
    while (std::abs(z) <= 2.0 && n < max_iter) {
        z = z*z + c;
        n++;
    }
    return n;
}

EXPORT
int* mandelbrot_grid(int amplada, int alcada, int max_iter, double x_min, double x_max, double y_min, double y_max)
{
    int* grid = new int[alcada * amplada];
    double x_step = (x_max - x_min) / amplada;
    double y_step = (y_max - y_min) / alcada;

    for (int i = 0; i < alcada; i++) {
        for (int j = 0; j < amplada; j++) {
            double a = x_min + j * x_step;
            double b = y_max - i * y_step;
            grid[i * amplada + j] = mandelbrot_iter(a, b, max_iter);
        }
    }
    return grid;
}

int julia_iter(double a, double b, double x, double y, int max_iter)
{
    std::complex<double> c(x, y);
    std::complex<double> z(a, b);

    int n = 0;
    while (std::abs(z) <= 2.0 && n < max_iter) {
        z = z*z + c;
        n++;
    }
    return n;
}

EXPORT
int* julia_grid(int amplada, int alcada, int max_iter, double x_min, double x_max, double y_min, double y_max, double px, double py)
{
    int* grid = new int[alcada * amplada];
    double x_step = (x_max - x_min) / amplada;
    double y_step = (y_max - y_min) / alcada;

    for (int i = 0; i < alcada; i++) {
        for (int j = 0; j < amplada; j++) {
            double a = x_min + j * x_step;
            double b = y_max - i * y_step;
            grid[i * amplada + j] = julia_iter(a, b, px, py, max_iter);
        }
    }
    return grid;
}

EXPORT
void free_grid(int* grid) {
    delete[] grid;
}
