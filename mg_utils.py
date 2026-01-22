import sys

import numpy
from numpy import random, isnan, isinf

eps = sys.float_info.epsilon

# Globals set by set_format.
precision_  = None
width_      = None
f_hi_       = None
f_lo_       = None
i_hi_       = None

#-------------------------------------------------------------------------------
def set_format( p, w=0 ):
    '''
    For width w and precision p:
    - medium integers < f_hi are printed with %{v}.0f, where v = w - p - 1;
    - small or large values, x < 0.1 or x ≥ f_hi, are printed with %{w}.{p}g;
    - medium values, 0.1 ≤ x < f_hi, are printed with %{w}.{p}f.
    To ensure data fits in width, sets:
        f_hi = 10^(w - p - 1) - 10^(-p + 1)/2,
        f_lo = 10^(-1)        - 10^(-p)/2,
        w >= p + 6; if given w > p + 6, uses given w.
    The -10^(-p)/2 handles values that round to 10^(w - p - 2) or 10^(-1).
    '''
    global precision_, width_, f_hi_, f_lo_, i_hi_, i_pad_
    precision_ = p
    width_ = max( w, p + 6 )
    f_hi_ = 10**(width_ - precision_ - 2) - 0.5 * 10**(-precision_)
    f_lo_ = 0.1 - 0.5 * 10**(-precision_)
    i_pad_ = ' ' * (precision_ + 1)
    #i_hi_ = 10**(width_ - precision_ - 1)
# end

set_format( 4 )

#-------------------------------------------------------------------------------
def fmt( x ):
    abs_val = abs( x )
    if (abs_val >= f_hi_):
        # Large values print as exponent (e).
        return f'{x:#{width_}.{precision_ - 1}e}'

    elif (x == int(x)):
        # Medium integers print as int,
        # padded to align with floating point decimal point.
        return f'{x:{width_ - precision_ - 1}.0f}' + i_pad_

    elif (abs_val >= 1.0):
        # Medium values print as fixed (f).
        return f'{x:{width_}.{precision_}f}'

    else:
        # Small values print as g.
        return f'{x:#{width_}.{precision_}g}'
# end

numpy.set_printoptions( linewidth=1000, formatter={'float': fmt} )

#-------------------------------------------------------------------------------
def test():
    global delta

    seed = 0x49434c
    rng = random.Generator( random.PCG64( seed ) )

    n = 4
    A = numpy.zeros(( n, n ))
    print( f'zeros =\n{A}\n' )

    A = numpy.ones(( n, n ))
    print( f'ones =\n{A}\n' )

    A = rng.random(( n, n ))
    print( f'rand =\n{A}\n' )

    (ii, jj) = numpy.where( A <= 0.1 )
    A[ ii, jj ] = 0
    print( f'small entries set to 0.\n{A};\n' )

    for i in range( n ):
        A[ i, i ] = 1
    print( f'diagonal entries set to 1.\n{A}\n' )

    (ii, jj) = numpy.where( (0.4 <= A) * (A <= 0.6) )
    A[ ii, jj ] = numpy.round( 100*A[ ii, jj ] )
    print( f'medium entries multiplied by 100 and rounded to integer.\n{A}\n' )

    # int and float switch to g at same point.
    i_hi = round( f_hi_ )

    # small value such that 1.000 ± delta prints as 1.001 and 0.999.
    delta = 0.5000000000001 * 10**(-precision_)
    print( f'precision {10**(-precision_):.{precision_+2}f}' )
    print( f'delta     {delta:.{precision_+2}f}\n' )

    seperator = [ None, None ]

    numbers = [
        # Test near i_hi. Prints as:
        [ '-i_hi - 1',  -i_hi - 1   ],  # g
        [ '-i_hi',      -i_hi       ],  # g
        [ '-i_hi + 1',  -i_hi + 1   ],  # int
        seperator,

        # Test near f_hi. Prints as:
        [ '-f_hi_ - delta',   -f_hi_ - delta   ],  # g
        [ '-f_hi_ * (1+eps)', -f_hi_ * (1+eps) ],  # g
        [ '-f_hi_',           -f_hi_           ],  # g
        [ '-f_hi_ * (1-eps)', -f_hi_ * (1-eps) ],  # g
        [ '-f_hi_ + delta',   -f_hi_ + delta   ],  # float
        seperator,

        # Test near f_lo. Prints as:
        [ '-f_lo_ - delta',    -f_lo_ - delta    ],  # g
        [ '-f_lo_ * (1+eps)', -f_lo_ * (1+eps) ],  # g
        [ '-f_lo_',           -f_lo_           ],  # g
        [ '-f_lo_ * (1-eps)', -f_lo_ * (1-eps) ],  # g
        [ '-f_lo_ + delta',    -f_lo_ + delta    ],  # float
        seperator,
    ]

    # Test integers.
    # First several print as g because >= i_hi,
    # then rest as int.
    # (For "several", exact number depends on width and precision.)
    x = -12340000.
    for i in range( 9 ):
        numbers.append( [ f'{round( x ):18.12g}', round( x ) ] )
        x /= 10
    numbers.append( [ '0.1111', 0.1111 ] )
    numbers.append( seperator )

    # Test integers and floats.
    # First several print as g because >= i_hi,
    # then several as int,
    # then several as float,
    # then rest as g because < 0.1.
    # Of those, g prints several as fixed, then several as exponent.
    x = -12300000.
    for i in range( 15 ):
        numbers.append( [ f'{x:18.12g}', x ] )
        x /= 10
    numbers.append( seperator )

    # Test floats.
    # First several print as g because >= f_hi.
    # Then several as float.
    # Then rest as g because < 0.1.
    # Of those, g prints several as fixed, then several as exponent.
    x = -12345678.9
    for i in range( 15 ):
        numbers.append( [ f'{x:18.12g}', x ] )
        x /= 10

    # Run tests.
    for (lbl, x) in numbers:
        if lbl is None:
            print()
        else:
            print( f'{lbl:<18s}: x {x:22.16g}  f [{x:14.4f}]  g [{x:10.4g}]  e [{x:10.3e}]  fmt [{fmt(x)}]' )
# end

if __name__ == '__main__':
    set_format( 2 )
    test()

    set_format( 4 )
    test()

    set_format( 6 )
    test()

    set_format( 8 )
    test()
