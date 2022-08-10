import numpy
import pytest

import cupy

from cupy import testing
from cupyx.scipy.interpolate import BarycentricInterpolator

from scipy import interpolate  # NOQA


@testing.with_requires("scipy")
class TestBarycentric:

    @testing.for_all_dtypes(no_bool=True, no_complex=True)
    @testing.numpy_cupy_allclose(scipy_name='scp')
    def test_lagrange(self, xp, scp, dtype):
        if xp.dtype(dtype).kind == 'u':
            pytest.skip()
        true_poly = xp.poly1d([-2, 3, 1, 5, -4])
        test_xs = xp.linspace(-5, 5, 100, dtype=dtype)
        xs = xp.linspace(-5, 5, 5, dtype=dtype)
        ys = true_poly(xs)
        P = scp.interpolate.BarycentricInterpolator(xs, ys)
        return P(test_xs)

    @testing.for_all_dtypes(no_bool=True, no_float16=True, no_complex=True)
    @testing.numpy_cupy_allclose(scipy_name='scp', atol=1e-5, rtol=1e-5)
    def test_scalar(self, xp, scp, dtype):
        if xp.dtype(dtype).kind in 'iu':
            pytest.skip()
        true_poly = numpy.poly1d([-1, 2, 6, -3, 2])
        xs = numpy.linspace(-1, 1, 10, dtype=dtype)
        ys = true_poly(xs)
        if xp is cupy:
            xs = cupy.asarray(xs)
            ys = cupy.asarray(ys)
        P = scp.interpolate.BarycentricInterpolator(xs, ys)
        return P(xp.array(7, dtype=dtype))

    @testing.for_all_dtypes(no_bool=True, no_complex=True)
    @testing.numpy_cupy_allclose(scipy_name='scp')
    def test_delayed(self, xp, scp, dtype):
        if xp.dtype(dtype).kind == 'u':
            pytest.skip()
        true_poly = xp.poly1d([-2, 3, 1, 5, -4])
        test_xs = xp.linspace(-5, 5, 100, dtype=dtype)
        xs = xp.linspace(-5, 5, 5, dtype=dtype)
        ys = true_poly(xs)
        P = scp.interpolate.BarycentricInterpolator(xs)
        P.set_yi(ys)
        return P(test_xs)

    @testing.for_all_dtypes(no_bool=True, no_complex=True)
    @testing.numpy_cupy_allclose(scipy_name='scp')
    def test_append(self, xp, scp, dtype):
        if xp.dtype(dtype).kind == 'u':
            pytest.skip()
        true_poly = xp.poly1d([-2, 3, 1, 5, -4])
        test_xs = xp.linspace(-5, 5, 100, dtype=dtype)
        xs = xp.linspace(-5, 5, 5, dtype=dtype)
        ys = true_poly(xs)
        P = scp.interpolate.BarycentricInterpolator(xs[:3], ys[:3])
        P.add_xi(xs[3:], ys[3:])
        return P(test_xs)

    @testing.for_all_dtypes(no_bool=True, no_complex=True)
    @testing.numpy_cupy_allclose(scipy_name='scp')
    def test_vector(self, xp, scp, dtype):
        if xp.dtype(dtype).kind == 'u':
            pytest.skip()
        xs = xp.array([0, 1, 2], dtype=dtype)
        ys = xp.array([[0, 1], [1, 0], [2, 1]], dtype=dtype)
        test_xs = xp.linspace(-1, 3, 100, dtype=dtype)
        P = scp.interpolate.BarycentricInterpolator(xs, ys)
        return P(test_xs)

    @pytest.mark.parametrize('test_xs', [0, [0], [0, 1]])
    @testing.numpy_cupy_array_equal(scipy_name='scp')
    def test_shapes_scalarvalue(self, xp, scp, test_xs):
        true_poly = xp.poly1d([-2, 3, 5, 1, -3])
        xs = xp.linspace(-1, 10, 10)
        ys = true_poly(xs)
        P = scp.interpolate.BarycentricInterpolator(xs, ys)
        test_xs = xp.array(test_xs)
        return xp.shape(P(test_xs))

    @pytest.mark.parametrize('test_xs', [0, [0], [0, 1]])
    @testing.numpy_cupy_array_equal(scipy_name='scp')
    def test_shapes_vectorvalue(self, xp, scp, test_xs):
        true_poly = xp.poly1d([4, -5, 3, 2, -4])
        xs = xp.linspace(-10, 10, 20)
        ys = true_poly(xs)
        P = scp.interpolate.BarycentricInterpolator(
            xs, xp.outer(ys, xp.arange(3)))
        test_xs = xp.array(test_xs)
        return xp.shape(P(test_xs))

    @pytest.mark.parametrize('test_xs', [0, [0], [0, 1]])
    @testing.numpy_cupy_array_equal(scipy_name='scp')
    def test_shapes_1d_vectorvalue(self, xp, scp, test_xs):
        true_poly = xp.poly1d([-3, -1, 4, 9, 8])
        xs = xp.linspace(-1, 10, 10)
        ys = true_poly(xs)
        P = scp.interpolate.BarycentricInterpolator(
            xs, xp.outer(ys, xp.array([1])))
        test_xs = xp.array(test_xs)
        return xp.shape(P(test_xs))

    @testing.for_all_dtypes(no_bool=True, no_complex=True)
    @testing.numpy_cupy_allclose(scipy_name='scp')
    def test_large_chebyshev(self, xp, scp, dtype):
        n = 100
        j = xp.arange(n + 1, dtype=dtype).astype(xp.float64)
        x = xp.cos(j * xp.pi / n)

        # # The weights for Chebyshev points against SciPy counterpart
        return scp.interpolate.BarycentricInterpolator(x).wi

    @testing.numpy_cupy_allclose(scipy_name='scp')
    def test_complex(self, xp, scp):
        x = xp.array([1, 2, 3, 4])
        y = xp.array([1, 2, 1j, 3])
        xi = xp.array([0, 8, 1, 5])
        return scp.interpolate.BarycentricInterpolator(x, y)(xi)

    @testing.for_all_dtypes(no_bool=True, no_complex=True)
    @testing.numpy_cupy_allclose(scipy_name='scp', atol=1e-6, rtol=1e-6)
    def test_wrapper(self, xp, scp, dtype):
        if xp.dtype(dtype).kind == 'u':
            pytest.skip()
        true_poly = xp.poly1d([-2, 3, 1, 5, -4])
        test_xs = xp.linspace(-2, 2, 5, dtype=dtype)
        xs = xp.linspace(-2, 2, 5, dtype=dtype)
        ys = true_poly(xs)
        return scp.interpolate.barycentric_interpolate(xs, ys, test_xs)

    @testing.for_all_dtypes(no_bool=True, no_complex=True)
    @testing.numpy_cupy_allclose(scipy_name='scp')
    def test_array_input(self, xp, scp, dtype):
        x = 1000 * xp.arange(1, 11, dtype=dtype)
        y = xp.arange(1, 11, dtype=dtype)
        xi = xp.array(1000 * 9.5)
        return scp.interpolate.barycentric_interpolate(x, y, xi)
